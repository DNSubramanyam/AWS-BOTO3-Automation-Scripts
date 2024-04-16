import boto3
filter = []
import csv
from pprint import pprint

final_data = []
instance_list = []
ins_para_list = []
volume_list = []
verify_vol_list = []
con = boto3.session.Session(profile_name='subbu', region_name='ap-south-1')
ins = con.client('ec2')

# def ins_data(**kwargs):
#     k = kwargs
#     for i in ins.describe_instances(**k)['Reservations']:
#         for j in i['Instances']:
#             print(j['InstanceId'])

def ins_data(**kwargs):
    k = kwargs
    for i in ins.describe_instances(**k)['Reservations']:
        for j in i['Instances']:
            batch_data = {}
            tag_dict = {}
            attached_vol = []
            voldes = j['BlockDeviceMappings']
            taglist = j['Tags']
            for blck in voldes:
                attached_vol.append(blck['Ebs']['VolumeId'])
                verify_vol_list.append(blck['Ebs']['VolumeId'])
            for k in taglist:
                tag_dict.setdefault(k['Key'], 'null')
                tag_dict[k['Key']] = k['Value']
            batch_data.setdefault('InstanceId', "null")
            batch_data.setdefault('VolumeId', "null")
            batch_data.setdefault('LaunchTime', 'null')
            batch_data.setdefault('PrivateIpAddress', 'null')
            batch_data.setdefault('State', 'null')
            batch_data.setdefault('VpcId', 'null')
            batch_data.setdefault('PlatformDetails', 'null')
            batch_data.setdefault('SubnetId', 'null')
            batch_data.setdefault('InstanceType', 'null')
            batch_data.setdefault('ImageId', 'null')
            batch_data['InstanceId'] = j['InstanceId']
            batch_data['PrivateIpAddress'] = j['PrivateIpAddress']
            batch_data['SubnetId'] = j['SubnetId']
            batch_data['VpcId'] = j['VpcId']
            batch_data['InstanceType'] = j['InstanceType']
            batch_data['ImageId'] = j['ImageId']
            batch_data['PlatformDetails'] = j['PlatformDetails']
            batch_data['State'] = j['State']['Name']
            batch_data['VolumeId'] = ','.join(attached_vol)
            batch_data['LaunchTime'] = j['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S %Z')
            batch_data.update(tag_dict)
            final_data.append(batch_data)
    for each_vol_id in volume_list:
        if each_vol_id not in verify_vol_list:
            final_data.append({'InstanceId': 'No Attached instance', 'VolumeId': each_vol_id})
    pprint(final_data)

with open('input.csv', 'r') as file:
    input_data = file.read()
input_list = input_data.split('\n')

filter = [{'Name':'instance-state-name', 'Values':['stopped']}]

ins_data(Filters=filter)
