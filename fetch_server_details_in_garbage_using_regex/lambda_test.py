import boto3
import csv
from re import compile
from pprint import pprint

# bucket = dict['Records'][0]['s3']['bucket']['name']
# key = dict['Records'][0]['s3']['object']['key']
bucket = 'regex-input-bucket'
key = 'inputfile.txt'


def lambda_handler():
    con = boto3.session.Session(profile_name='subbu')
    s3client = con.client('s3', region_name='ap-south-1')
    response = s3client.get_object(Bucket=bucket, Key=key)
    data = response['Body'].read().decode('utf-8')
    sub = compile(r'(?:([a-zA-Z0-9]+?)(?:\s+)((?:\d+(?:\.?)){4}))')
    mo = sub.findall(data)
    with open('server_ip_details.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Server', 'IP Address'])
        for each in mo:
            print([each[0], each[1]])
            writer.writerow([each[0], each[1]])

lambda_handler()