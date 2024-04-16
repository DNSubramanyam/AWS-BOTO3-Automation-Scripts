import boto3
from datetime import datetime

con = boto3.session.Session()
ec2 = con.client('ec2', region_name='ap-south-1')
sns = boto3.client('sns', region_name='ap-south-1')

sns_arn = 'arn:aws:sns:ap-south-1:366951018568:sample-testing-topic'
subject = "IDPS server pathching || Root-volume-backup"


patch_tag = [{'Key': 'BAU', 'Value': 'Patching'}]
#current_datetime = datetime.now().strftime("%y-%m-%d_%H-%M-%S")
current_datetime = datetime.now().strftime("%d-%b-%y_%H.%M")
snapshot_id = []
row = []
ins_list = ['i-0627896df652ff056']
if len(ins_list) > 0:
    try:
        ec2_response = ec2.describe_instances(InstanceIds=ins_list)
        for each in ec2_response['Reservations']:
            for ins in each ['Instances']:
                instance_id = ins['InstanceId']
                root_device = ins['RootDeviceName']
                instance_state = ins['State']['Name']
                vol_response = ec2.describe_volumes(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance_id]}, {'Name': 'attachment.device', 'Values': [root_device]}])
                for vol in vol_response['Volumes']:
                    volume_id = vol['VolumeId']
                    volume_tags = vol['Tags']
                    volume_tags.extend(patch_tag)
                    TagSpecs=[{'ResourceType': 'snapshot', 'Tags': volume_tags}]
                    for tag in volume_tags:
                        if tag['Key'] == 'Name':
                            description = tag['Value'] + '_for_patching_' + current_datetime
                            tag['Value'] = tag['Value']+ "_" + current_datetime
                    snap_response = ec2.create_snapshot(Description = description, VolumeId = volume_id, TagSpecifications=TagSpecs)
                    snapshot_id.append(snap_response['SnapshotId'])
        if len(snapshot_id) > 0:
            for ind in range(0, len(ins_list)):
                row.append((ins_list[ind]).ljust(20, ' ') + '\t==>\t' + snapshot_id[ind])
            data1 = '\n'.join(row) 
            message = f'\nExecution is successful..!\n\nServers actioned [Total = {len(ins_list)}] :\n\n{data1}'          
    except Exception as e:
        message = f'\nExecution failed..!\n\nServers actioned [Total = {len(ins_list)}]\n\nError: {e}'
        
    sns.publish(TopicArn=sns_arn, Subject=subject, Message=message)