import boto3
from pprint import pprint
from datetime import datetime

#con = boto3.session.Session()
ec2 = boto3.client('ec2', region_name='ap-south-1')
paginator = ec2.get_paginator('describe_snapshots')

snapshots_older = []

response_iterator = paginator.paginate(OwnerIds=['366951018568'])

for each in response_iterator:
    for snapshot in each['Snapshots']:
        a= snapshot['StartTime']
        b=a.date()
        c=datetime.now().date()
        d=(c-b).days
        if d >= 30:
            snapshots_older.append(snapshot['SnapshotId'])

pprint(snapshots_older)

for each_snap in snapshots_older:
    ec2.delete_snapshot(SnapshotId=each_snap)

