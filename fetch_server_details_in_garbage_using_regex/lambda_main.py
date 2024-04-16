import boto3
from time import time
from re import compile
import csv

output_bucket = 'download-test-v64'

def lambda_handler(event, context):
    s3client = boto3.client('s3', region_name='ap-south-1')
    input_bucket = event['Records'][0]['s3']['bucket']['name']
    input_key = event['Records'][0]['s3']['object']['key']
    output_key = 'server_details_' + str(round(time())) + '.csv'
    file_name = '/tmp/' + 'server_details_' + str(round(time())) + '.csv'
    print('bucket = {}, key = {}'.format(input_bucket, input_key))
    response = s3client.get_object(Bucket=input_bucket, Key=input_key)
    data = response['Body'].read().decode('utf-8')
    sub = compile(r'(?:([a-zA-Z0-9]+?)(?:\s+)((?:\d+(?:\.?)){4}))')
    mo = sub.findall(data)
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Server', 'IP Address'])
        for each in mo:
            print('writing to output csv file in tmp !')
            writer.writerow([each[0], each[1]])
    try:
        s3client.upload_file(file_name, Bucket=output_bucket, Key=output_key)
        print('Upload Successful !')
    except Exception as e:
        print('Upoad faild with error {}'.format(e))
