import boto3
from datetime import  date
from pprint import pprint

ec2 = boto3.client('ec2')

def main_handle():
    #file_name = input("Enter the file name : ")
    file_name = 'input.csv'
    try:
        with open(file_name, 'r') as file:
            input_data = file.read().strip()
        input_list = input_data.split('\n')
        input_list = [i for i in input_list if i]
        initiate_ami(input_list)
    except Exception as error:
        print(error)

def initiate_ami(ins_id_list):
    #print(f'initiating ami backup for the servers: {ins_id_list}')
    for each in ins_id_list:
        image_response = ec2.create_image(
            InstanceId=each,
            #Name=f'{each}_{date.today().strftime("%d_%b_%Y_%H_%M")}',
            Name=f'{each}_29-09-2024', 
            NoReboot=True, 
            TagSpecifications=[
                {'ResourceType': 'image', 
                 'Tags': [ 
                    { 'Key': 'Env',
                     'Value': 'T1' }
                 ]
             }
         ]
      )
        print(f"{each}:{image_response['ImageId']}")

main_handle()