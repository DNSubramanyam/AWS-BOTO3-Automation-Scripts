import boto3
from pprint import pprint
import csv


def create_file(file_data):
    header_data = []
    for dataset in file_data:
        for keys in dataset:
            header_data.append(keys)
    header_data = list(dict.fromkeys(header_data))
    filename = 'output5.csv'
    try:
        with open(filename, 'w', encoding='UTF8', newline='') as outputfile:
            writer = csv.DictWriter(outputfile, fieldnames=header_data, restval='N/A')
            writer.writeheader()
            writer.writerows(file_data)
        print(f'Details parked in file : {filename}')
    except Exception as error:
        print(error)

def fetch_data():
    to_write = []
    gp2_vol = []
    f = {'Name': 'platform', 'Values': ['windows']}
    #f = {}
    ins_name = {}
    vol_list = []
    ec2 = boto3.client('ec2', region_name='us-east-1')
    for i in ec2.describe_instances(Filters = [f])['Reservations']:
        for j in i['Instances']:  
            ins = j['InstanceId']
            for tag in j['Tags']:
                if tag['Key'] == 'Name':
                    ins_name.setdefault(ins, '')
                    ins_name[ins] = tag['Value']
            for k in j['BlockDeviceMappings']:
                vol_list.append(k['Ebs']['VolumeId'])
    response = ec2.describe_volumes(VolumeIds=vol_list)
    for a in response['Volumes']:
        final_data = {}
        if a['VolumeType'] == 'gp2':
            gp2_vol.append(a['VolumeId'])
            final_data.setdefault('VolumeId', 'null')
            final_data.setdefault('VolumeType', 'null')
            final_data.setdefault('InstanceId', 'null')
            final_data.setdefault('InstanceName', 'null')
            final_data['VolumeId'] = a['VolumeId']
            final_data['VolumeType'] = a['VolumeType']
            for b in a['Attachments']:
                final_data['InstanceId'] = b['InstanceId']
                final_data['InstanceName'] = ins_name[b['InstanceId']]
            to_write.append(final_data)
    print(f'instancecount: {len(ins_name)}, VolumeCount: {len(vol_list)}, gp2_vol_count: {len(gp2_vol)}')
    return to_write



if __name__ == '__main__':
    data = fetch_data()
    if len(data) > 0:
        create_file(data)
    else:
        print('No gp2 type volumes!')
