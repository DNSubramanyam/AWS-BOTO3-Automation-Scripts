import boto3
import time
from datetime import  date

def notify(value):
    sns = boto3.client('sns', region_name='us-east-1')
    sns_arn= "arn:aws:sns:us-east-1:366951018568:jenkins-ip-update-notification"
    subject = "DNS updated in R53 || Jenkins server"
    msg = f'New public IP {value} updated in R53 for jenkins server'
    today = date.today().strftime("%b-%d-%Y")
    sns.publish(TopicArn=sns_arn, Subject=subject+'_'+today, Message=msg)


def poll_change_status(change_id, ip):
    client = boto3.client('route53')

    while True:
        response = client.get_change(Id=change_id)
        status = response['ChangeInfo']['Status']
        print(f"Change status: {status}")

        if status == 'INSYNC':
            print("Change is complete.")
            notify(ip)
            break

        time.sleep(15) 

def update_dns_record(hosted_zone_id, record_name, new_value):
    
    client = boto3.client('route53')
 
    response = client.list_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        StartRecordName=record_name,
        StartRecordType='A',
        MaxItems='1'
    )
   
    existing_record = response['ResourceRecordSets'][0]
  
    changes = [
        {
            'Action': 'UPSERT',
            'ResourceRecordSet': {
                'Name': existing_record['Name'],
                'Type': existing_record['Type'],
                'TTL': existing_record['TTL'],
                'ResourceRecords': [{'Value': new_value}]
            }
        }
    ]
   
    response = client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': changes
        }
    )

    return response['ChangeInfo']

def lambda_handler(event, context):
    # TODO implement
    hosted_zone_id = 'Z0400132321GG1WNTEYB4'
    record_name = 'jenkins.subbu98.xyz'

    ec2 = boto3.client('ec2', region_name='us-east-1')

    ec2_response = ec2.describe_instances(InstanceIds=event['detail']['instance-id'])['Reservations']
    for b in ec2_response:
        for c in b['Instances']:
            new_value = c['PublicIpAddress']
    poll_change_status(change_id=update_dns_record(hosted_zone_id, record_name, new_value)['Id'], ip=new_value)

    return {
        'statusCode': 200,
        'new-value': new_value
    }



if __name__ == "__main__":
    event ={
          "detail": {
    "state": ["running"],
    "instance-id": ["i-05285367ff9fe7477"]

  }
    }
    print(lambda_handler(event, context=None))
