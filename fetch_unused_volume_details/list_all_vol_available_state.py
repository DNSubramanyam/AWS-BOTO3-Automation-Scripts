import boto3
import csv
from pprint import pprint

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


def unused_vol():
    final_data = []
    ebs = boto3.client('ec2', region_name='us-east-1')
    response = ebs.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    for vol in response['Volumes']:
        fetched_data = {}
        fetched_data.setdefault('VolumeId', 'null')
        fetched_data.setdefault('CreateTime', 'null')
        fetched_data.setdefault('Size', 'null')
        fetched_data['VolumeId'] = vol['VolumeId']
        fetched_data['CreateTime'] = vol['CreateTime'].strftime("%Y-%m-%d %H:%M:%S %Z") 
        fetched_data['Size'] = vol['Size']
        if len(vol['Tags']) > 0:
            for kv in vol['Tags']:
                    fetched_data.setdefault(kv['Key'], 'null')
                    fetched_data[kv['Key']] = kv['Value']
        final_data.append(fetched_data)
    return final_data

if __name__ == "__main__":
    pprint(unused_vol())
    create_file(unused_vol())