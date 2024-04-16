import boto3
import csv
from datetime import datetime, timedelta, timezone

def create_file(file_data):
    header_data = []
    for dataset in file_data:
        for keys in dataset:
            header_data.append(keys)
    header_data = list(dict.fromkeys(header_data))
    filename = 'output.csv'
    try:
        with open(filename, 'w', encoding='UTF8', newline='') as outputfile:
            writer = csv.DictWriter(outputfile, fieldnames=header_data, restval='N/A')
            writer.writeheader()
            writer.writerows(file_data)
        print(f'Details parked in file : {filename}')
    except Exception as error:
        print(error)


def unused_vol(threshold):
    unused_vol_list = {}
    ebs = boto3.client('ec2', region_name='us-east-1')
    #response = ebs.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    #response = ebs.describe_volumes(VolumeIds=['vol-018337974b79718e8'])
    response = ebs.describe_volumes()
    for vol in response['Volumes']:
        #print(vol['VolumeId'])
        if time_differ_check(vol['CreateTime']) < threshold:
            unused_vol_list.setdefault(vol['VolumeId'], '')
            unused_vol_list[vol['VolumeId']] = vol['CreateTime']
    #print(unused_vol_list)
    if len(unused_vol_list) > 0:
        print(f'Count of all volumes in available state: {len(unused_vol_list)}')
        detach_time_check(unused_vol_list, threshold)
    else:
        print('No volumes are in available state.')


def detach_time_check(vol_dict, days_old):
    final_data = []
    exception_list = []
    final_vol_list = [i for i in vol_dict]
    delta_date_obj = datetime.now() - timedelta(days=90)
    event_start_date = datetime(delta_date_obj.year, delta_date_obj.month, delta_date_obj.day)
    datetime_today = datetime.now(timezone.utc)
    #event_end_date = datetime(datetime_today.year, datetime_today.month, datetime_today.day)
    event_end_date = datetime(datetime_today.year, datetime_today.month, datetime_today.day, datetime_today.hour, datetime_today.minute)
    ct = boto3.client('cloudtrail')
    for each_vol in final_vol_list:
        to_write = {}
        to_write.setdefault('VolumeId', '')
        to_write.setdefault('CreationTime', '')
        to_write.setdefault('NoOfDaysSinceCreation', 0)
        to_write.setdefault('NoOfDaysSinceDetached', 'NA')
        to_write['VolumeId'] = each_vol
        to_write['CreationTime'] = vol_dict[each_vol].strftime("%d/%m/%Y_%H:%M:%S_%Z")
        to_write['NoOfDaysSinceCreation'] = time_differ_check(time_obj= vol_dict[each_vol])
        ct_response = ct.lookup_events(LookupAttributes=[{'AttributeKey': 'ResourceName','AttributeValue':each_vol}], StartTime=event_start_date, EndTime=event_end_date)
        for event in ct_response['Events']:  
            if event['EventName'] == "DetachVolume":
                to_write['NoOfDaysSinceDetached'] = time_differ_check(event['EventTime'])
                if time_differ_check(event['EventTime']) > days_old:
                    to_write = {}
                    exception_list.append(each_vol)
                    final_vol_list.remove(each_vol)
                break
        if len(to_write) > 0:
            final_data.append(to_write)
    print(f'Count of ignored volumes: {len(exception_list)}')
    print(f'Count of volumes which can be removed: {len(final_vol_list)}\n')
    #pprint(final_data)
    #pprint(final_unused_vol_data)
    if len(final_data) > 0:
        create_file(final_data)

def time_differ_check(time_obj):
    dt_obj_today = datetime.now(timezone.utc)
    differ =  dt_obj_today - time_obj
    diff_in_days = str(differ).split()
    if len(diff_in_days) < 3:
        diff_in_days = 0
    else:
        diff_in_days = int(diff_in_days[0])
    return diff_in_days

if __name__ == '__main__':
    days_old = 60
    unused_vol(days_old)