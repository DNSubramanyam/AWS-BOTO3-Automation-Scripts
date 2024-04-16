import boto3
from pprint import pprint
import csv

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


def fetch():
    final_data = []    
    elb = boto3.client('elbv2',  region_name='us-east-1')
    response = elb.describe_load_balancers()['LoadBalancers']
    for lb in response:
        fetched_data = {}
        tg_grp_dict = {}
        targets = []
        albarn = lb['LoadBalancerArn']
        for tg in elb.describe_target_groups(LoadBalancerArn=albarn)['TargetGroups']:
            tg_grp_dict.setdefault(tg['TargetGroupName'], '')
            tg_grp_dict[tg['TargetGroupName']] = tg['TargetGroupArn']
        for tggrp in tg_grp_dict:
            response2 = elb.describe_target_health(TargetGroupArn=tg_grp_dict[tggrp])
            targets.extend(response2['TargetHealthDescriptions'])
        if len(targets) == 0:               
            fetched_data.setdefault('Name', 'null')
            fetched_data.setdefault('CreationTime', 'null')
            fetched_data.setdefault('State', 'null')
            fetched_data.setdefault('Scheme', 'null')
            fetched_data.setdefault('Type', 'null')
            fetched_data.setdefault('TargetGroupName', 'null')
            fetched_data.setdefault('VPCId', 'null')
            fetched_data.setdefault('DNSName', 'null')
            fetched_data['Name'] = lb['LoadBalancerName'] 
            fetched_data['CreationTime'] = lb['CreatedTime'].strftime("%Y-%m-%d %H:%M:%S %Z") 
            fetched_data['State'] = lb['State']['Code']
            fetched_data['Scheme'] = lb['Scheme']
            fetched_data['Type'] = lb['Type']
            fetched_data['TargetGroupName'] = ','.join(tg_grp_dict.keys())
            fetched_data['VPCId'] = lb['VpcId']
            fetched_data['DNSName'] = lb['DNSName']
            response3 = elb.describe_tags(ResourceType='volume')['TagDescriptions']
            for kv in response3:
                if len(kv['Tags']) > 0:
                    for kvp in kv['Tags']:
                        fetched_data.setdefault(kvp['Key'], 'null')
                        fetched_data[kvp['Key']] = kvp['Value']
            final_data.append(fetched_data)
    return final_data

            



if __name__ == '__main__':
    if len(fetch()) > 0:
        create_file(fetch())
    else:
        print('No unused Load balancers!')
