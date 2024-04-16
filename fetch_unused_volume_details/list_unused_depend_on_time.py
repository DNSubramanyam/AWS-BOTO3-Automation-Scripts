import boto3
from pprint import pprint
from datetime import datetime, timedelta, timezone

def unused_vol(threshold):
    unused_vol_list = []
    ebs = boto3.client('ec2', region_name='us-east-1')
    response = ebs.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    #response = ebs.describe_volumes(VolumeIds=['vol-018337974b79718e8'])
    #response = ebs.describe_volumes()
    for vol in response['Volumes']:
        #print(vol['VolumeId'])
        if time_differ_check(vol['CreateTime']) < threshold:
            unused_vol_list.append(vol['VolumeId'])
    pprint(unused_vol_list)
    pprint(detach_time_check(unused_vol_list, threshold))
        


def detach_time_check(vol_list, days_old):
    final_unused_vol_data = vol_list.copy()
    delta_date_obj = datetime.now() - timedelta(days=90)
    event_start_date = datetime(delta_date_obj.year, delta_date_obj.month, delta_date_obj.day)
    datetime_today = datetime.now(timezone.utc)
    #event_end_date = datetime(datetime_today.year, datetime_today.month, datetime_today.day)
    event_end_date = datetime(datetime_today.year, datetime_today.month, datetime_today.day, datetime_today.hour, datetime_today.minute)
    ct = boto3.client('cloudtrail')
    for each_vol in vol_list:
            ct_response = ct.lookup_events(LookupAttributes=[{'AttributeKey': 'ResourceName','AttributeValue':each_vol}], StartTime=event_start_date, EndTime=event_end_date)
            for event in ct_response['Events']:
                #print(f"{event['EventName']}, {event['EventTime']}")
                if event['EventName'] == "DetachVolume" and time_differ_check(event['EventTime']) < days_old:
                    print(event['EventTime'])
                    final_unused_vol_data.remove(each_vol)
                break
    return final_unused_vol_data

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
    days_older = 30
    unused_vol(days_older)