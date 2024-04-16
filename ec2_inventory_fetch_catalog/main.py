import boto3
import csv
from pprint import pprint

ec2 = boto3.client('ec2')
vol_list = []
total_vol = []
total_ins = []

with open('output.csv', 'w', newline='') as opfile:
    writer = csv.writer(opfile)
    writer.writerow(['Name', 'InstanceID', 'PrivateIp', 'AttachedVolumeIds' ])
    for i in ec2.describe_instances()['Reservations']:
        vol_list = []
        for j in i['Instances']:
            ins = j['InstanceId']
            ip = j['PrivateIpAddress']
            for tag in j['Tags']:
                if tag['Key'] == 'Name':
                    name = tag['Value']
            for k in j['BlockDeviceMappings']:
                vol_list.append(k['Ebs']['VolumeId'])
                vols = ','.join(vol_list)
            total_vol.extend(vol_list)
            total_ins.append(ins)
        writer.writerow([name,ins,ip,vols])
    print(f'TotalIns: {len(total_ins)}\nTotalVol: {len(total_vol)}')





