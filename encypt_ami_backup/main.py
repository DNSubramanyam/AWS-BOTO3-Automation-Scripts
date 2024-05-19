import boto3
from pprint import pprint

ec2 = boto3.client('ec2', region_name='us-east-1')

paginator = ec2.get_paginator('describe_images')

response_iterator = paginator.paginate(Owners=['self'],
    Filters=[
        {
            'Name': 'block-device-mapping.encrypted',
            'Values': ['true']
        }])

for i in response_iterator:
    for image in i['Images']:
        pprint(image['ImageId'])
