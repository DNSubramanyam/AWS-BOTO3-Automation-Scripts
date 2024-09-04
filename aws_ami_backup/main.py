import boto3
import os
from pprint import pprint

ec2 = boto3.client('ec2', region_name='us-east-1')

def ip_block(ip_list):
    id_list = []
    print(f'IP list is {ip_list}')
    response = ec2.describe_instances(
    Filters=[
        {
            'Name': 'private-ip-address',
            'Values': ip_list
        }
    ])
    for i in response['Reservations']:
        for j in i['Instances']:
            id_list.append(j['InstanceId'])
    pprint(id_list)
    if len(id_list) > 0:
        initiate_ami(id_list)


def tag_block(tag_key, tag_value):
    id_list = []
    print(f'choosen tag = {tag_key}: {tag_value}')
    response = ec2.describe_instances(
    Filters=[
        {
            'Name': f'tag:{tag_key}',
            'Values': [tag_value]
        }
    ])
    for i in response['Reservations']:
        for j in i['Instances']:
            id_list.append(j['InstanceId'])
    pprint(id_list)
    if len(id_list) > 0:
        initiate_ami(id_list)

def initiate_ami(ins_id_list):
    print(f'initiating ami backup for the servers: {ins_id_list}')


print("""
    ************************
    * Choose your input : *
    * a. IP address       *
    * b. InstanceId       *
    * c. Tag              * 
    ************************
    \n""")

file_name = ''
input_list = []
choice = input("Enter your choice : ")
if choice == 'a' or choice == 'b':
    file_name = input("Enter the file name : ")
    try:
        with open(file_name, 'r') as file:
            input_data = file.read().strip()
        input_list = input_data.split('\n')
        input_list = [i for i in input_list if i]
    except Exception as error:
        print(error)

if choice == 'a' and len(input_list) > 0:
    ip_block(input_list)
elif choice == 'b' and len(input_list) > 0:
    initiate_ami(input_list)
elif choice == 'c':
    tag_key = input("Enter the tag key: ")
    tag_value = input("Enter the tag value: ")
    tag_block(tag_key, tag_value)
else:
    print('Invalid option selected or input file is empty!!')




            
        