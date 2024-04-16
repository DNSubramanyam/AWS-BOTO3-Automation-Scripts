import json
import boto3
import csv
import os
from datetime import datetime

s3 = boto3.client("s3")
ssm = boto3.client('ssm')

def upload_to_results(filename, bucket, cmdid):
    upload_key = f'lambda-results/{cmdid}_output.csv'
    s3.upload_file(filename, bucket, upload_key)

def list_obj (bucket, pref):
    response = s3.list_objects_v2(Bucket= bucket, Prefix=pref)
    out_list = [each['Key'] for each in response['Contents']]
    return out_list

def create_file(file_data):
    header_data = ['date', 'command_id', 'instance_id', 'status', 'stderr', 'stdout']
    filename = '/tmp/output.csv'
    try:
        with open(filename, 'w', encoding='UTF8', newline='') as outputfile:
            writer = csv.DictWriter(outputfile, fieldnames=header_data, restval='N/A')
            writer.writeheader()
            writer.writerows(file_data)
    except Exception as error:
        print(error)


def lambda_handler(event, context):
    # TODO implement
    final_data = []
    buck_name = event['Bucket']
    commandid = event['CommandId']
    extra_path = 'awsrunShellScript/0.awsrunShellScript'
    date = datetime.now()
    file_path = '/tmp/output.csv'
    instance_list = list(set([each.split('/')[1] for each in list_obj(bucket=buck_name, pref=commandid)]))
    for ins in instance_list:
        to_write = {}
        to_write.setdefault('status', None)
        to_write.setdefault('stdout', None)
        to_write.setdefault('stderr', None)
        to_write.setdefault('command_id', None)
        to_write.setdefault('instance_id', None)
        to_write.setdefault('date', None)
        to_write['command_id'] = commandid
        to_write['instance_id'] = ins
        to_write['date'] = date.strftime("%d-%m-%Y")
        ssm_response = ssm.get_command_invocation(CommandId=commandid, InstanceId=ins)
        to_write['status'] = ssm_response['Status']
        obj_list = [each.split('/')[4] for each in list_obj(bucket=buck_name, pref=f'{commandid}/{ins}/{extra_path}')]
        for obj in obj_list:
            obj_response = s3.get_object(Bucket=buck_name, Key=f'{commandid}/{ins}/{extra_path}/{obj}')
            to_write[obj] = obj_response["Body"].read().decode("utf-8").strip()
        final_data.append(to_write)
    create_file(final_data)
    upload_to_results(filename = file_path, bucket=buck_name, cmdid=commandid)
    os.remove(file_path)
    target_path = f's3://{buck_name}/lambda-results'
    return {
        'statusCode': 200,
        'body': json.dumps('Results parked in s3'),
        's3-path': target_path

    }



if __name__ == "__main__":
    event = {'Bucket': 'run-command-logs-v64', 'CommandId': 'ba064d69-4d7a-467f-988a-742e8e46d2b2'}
    lambda_handler(event=event, context=None)