import boto3
import csv
from pprint import pprint
from datetime import datetime

con = boto3.session.Session()
ld = con.client('lambda', region_name='ap-south-1')

output_file = 'fetchoutput.csv'
# response = ld.get_function(FunctionName='runtimechange')['Configuration']
# print(f"{response['FunctionName'].ljust(20)}:{response['Runtime']}    {response['FunctionArn']}")

def fetch(input_data, op_file):
    with open(op_file, 'w', newline='') as writefile:
        writer = csv.writer(writefile)
        writer.writerow(['FunctionName' , 'RunTime', 'FunctionARN'])
        for each in input_list:
            response = ld.get_function(FunctionName=each.strip())['Configuration']
            #print(f"{response['FunctionName'].ljust(30)}:{response['Runtime']}    {response['FunctionArn']}")
            writer.writerow([response['FunctionName'], response['Runtime'], response['FunctionArn']])

with open('input.csv', 'r') as file:
    input_data = file.read().strip()
input_list = input_data.split('\n')
#print(input_list)
current_datetime = datetime.now().strftime("%y-%m-%d_%H-%M")
output_file = 'fetchoutput_' + current_datetime + '.csv'
fetch(input_list, output_file)
    

