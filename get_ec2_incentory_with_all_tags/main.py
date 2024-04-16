import boto3
import csv
from pprint import pprint
disp = """Here are the options available for "Parameters"..!
1. private-ip-address
2. instance-state-name - The state of the instance ( pending | running | shutting-down | terminated | stopping | stopped ).
3. subnet-id
4. platform (Only works for 'windows')"""
options = {'1':'private-ip-address', '2':'instance-state-name', '3':'subnet-id', '4':'platform'}
final_data = []
volume_list = []
verify_vol_list = []
filter = []
is_on = True
con = boto3.session.Session(profile_name='subbu', region_name='ap-south-1')
ins = con.client('ec2')


def volume_data(input_vol):
    vol_filter = [{'Name': 'block-device-mapping.volume-id', 'Values': input_list}]
    ins_data(Filters=vol_filter)

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
    create_file(final_data)


def create_file(file_data):
    header_data = []
    for dataset in file_data:
        for keys in dataset:
            header_data.append(keys)
    header_data = list(dict.fromkeys(header_data))
    # filename =  datetime.now().strftime('details_%y-%m-%d-%H_%M.csv')
    filename = 'output.csv'
    try:
        # pprint(header_data)
        with open(filename, 'w', encoding='UTF8', newline='') as outputfile:
            writer = csv.DictWriter(outputfile, fieldnames=header_data, restval='N/A')
            writer.writeheader()
            writer.writerows(file_data)
        print(f'Details parked in file : {filename}')
    except Exception as error:
        print(error)


while is_on:
    choice = input(
        "Select the data parked in input file ..!\nA. InstanceId's\nB. VolumeId's\nC. Tags\nD. Parameters(please check above options!)\n\nSelect the data provided in input file :  ").lower()
    with open('input.csv', 'r') as file:
        input_data = file.read()
    input_list = input_data.split('\n')
    try:
        if choice == 'a':
            is_on = False
            ins_data(InstanceIds=input_list)
        elif choice == 'b':
            is_on = False
            volume_list = input_list
            volume_data(input_list)
        elif choice == 'c':
            is_on = False
            name = input('Please enter the Key of Tag: ')
            key_name = 'tag:' + name
            filter = [{'Name': key_name, 'Values': input_list}]
            ins_data(Filters=filter)
        elif choice == 'd':
            is_on = False
            print('=' * 50)
            print(disp)
            print('=' * 50)
            para = input('Please select one of the options for "Parameter": ')
            filter = [{'Name': options[para], 'Values': input_list}]
            ins_data(Filters=filter)
        else:
            print('Please choose correct option..!!\n')
    except Exception as error:
        print(error)
