import boto3
import csv
from pprint import pprint
from datetime import datetime


def create_file(filename, file_data):
    header_data = []
    for dataset in file_data:
        for keys in dataset:
            header_data.append(keys)
    header_data = list(dict.fromkeys(header_data))
    try:
        with open(filename, 'w', encoding='UTF8', newline='') as outputfile:
            writer = csv.DictWriter(outputfile, fieldnames=header_data, restval='N/A')
            writer.writeheader()
            writer.writerows(file_data)
        print(f'Details parked in file : {filename}')
    except Exception as error:
        print(error)


def fetch(fn):
    ec2 = boto3.client('ec2')
    final_data = []
    current_date = datetime.utcnow().date()
    required_tags = ['Name', 'Environment', 'ApplicationName', 'Owner', 'Hostname']
    ec2_response = ec2.describe_instances()
    for each in ec2_response['Reservations']:
        for ins in each ['Instances']:
            fetch = {}
            instance_id = ins['InstanceId']
            platform = ins['PlatformDetails']
            ip = ins['PrivateIpAddress']
            root_device = ins['RootDeviceName']
            tags = {tag['Key']: tag['Value'] for tag in ins.get('Tags', [])}
            ext_tags = {tag: tags.get(tag, "Null") for tag in required_tags}
            vol_response = ec2.describe_volumes(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance_id]}, {'Name': 'attachment.device', 'Values': [root_device]}])
            for vol in vol_response['Volumes']:
                creation_date = vol['CreateTime'].date()
                diff =  (current_date - creation_date).days
        #pprint(f'{ins_name}:{instance_id}:{volume_id}:{creation_date}: {diff}')
            fetch.setdefault('InstanceId', 'Null')
            fetch.setdefault('IP', 'Null')
            fetch.setdefault('OS Type', 'null')
            fetch.setdefault('Last AMI Rotation Date', 'Null')
            fetch.setdefault('Age', 'Null')
            fetch['InstanceId'] = instance_id
            fetch['IP'] = ip
            fetch['OS Type'] = platform
            fetch['Last AMI Rotation Date'] = creation_date.strftime("%d-%m-%Y")
            fetch['Age'] = diff
            fetch = fetch | ext_tags
            final_data.append(fetch)
    #pprint(final_data)
    create_file(fn, final_data)


if __name__ == "__main__":
    file_name = input("enter your custom output file name (without '.csv'): ")
    fetch(f'{file_name}.csv')
            



