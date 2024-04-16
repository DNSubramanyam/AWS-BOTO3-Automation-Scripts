import boto3
from pprint import pprint
import csv

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

def verify(vol_list):
    write_data = []
    ebs = boto3.client('ec2', region_name='us-east-1')
    ver_response = ebs.describe_volumes(VolumeIds=vol_list)
    for a in ver_response['Volumes']:
        verify_data = {}
        verify_data.setdefault('VolumeId', 'null')
        verify_data.setdefault('VolumeType', 'null')
        verify_data['VolumeId'] = a['VolumeId']
        verify_data['VolumeType'] = a['VolumeType']
        write_data.append(verify_data)
    create_file('verify_response.csv', write_data)


def modify(vol_list):
    to_write = []
    file_name= 'modify_response.csv'
    ec2 = boto3.client('ec2', region_name='us-east-1')
    for vol in vol_list:
        modify_data = {}
        response = ec2.modify_volume(VolumeId=vol, VolumeType='gp3')['VolumeModification']
        modify_data.setdefault('VolumeId', 'null')
        modify_data.setdefault('OriginalVolumeType', 'null')
        modify_data.setdefault('TargetVolumeType', 'null')
        modify_data.setdefault('ModificationState', 'null')
        modify_data['VolumeId'] = response['VolumeId']
        modify_data['OriginalVolumeType'] = response['OriginalVolumeType']
        modify_data['TargetVolumeType'] = response['TargetVolumeType']
        modify_data['ModificationState'] = response['ModificationState']
        to_write.append(modify_data)
    create_file(file_name,to_write)


if __name__ == '__main__':
    with open('input.csv', 'r') as file:
        input_data = file.read().strip()
        input_list = input_data.split('\n')
        input_list = [i for i in input_list if i]
    choice = input("1. Modify\n2. verify\n\nchoice: ")
    if choice == '1':
        modify(input_list)
    else:
        verify(input_list)