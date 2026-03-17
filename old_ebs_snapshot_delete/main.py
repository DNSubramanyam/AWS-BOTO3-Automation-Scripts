import boto3
import logging
from datetime import datetime
from botocore.exceptions import ClientError
import csv

logging.basicConfig(
    filename='delete_operations.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def create_input_file(ids, filename="input.csv"):
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for snapshot in ids:
                writer.writerow([snapshot])
        s_msg = f"Successfully created {filename} with {len(ids)} Snapshot iDs.."
        print(s_msg)
        logging.info(s_msg)
    except Exception as e:
        f_msg = f"Error creating file: {e}"
        print(f_msg)
        logging.error = f_msg


def fetch(ec2_client, account_id, days_thr):
    paginator = ec2_client.get_paginator('describe_snapshots')
    snapshots_older = []
    response_iterator = paginator.paginate(OwnerIds=[account_id])
    for each in response_iterator:
        for snapshot in each['Snapshots']:
            a= snapshot['StartTime']
            b=a.date()
            c=datetime.now().date()
            d=(c-b).days
            if d >= days_thr:
                snapshots_older.append(snapshot['SnapshotId'])
    if len(snapshots_older):
        create_input_file(snapshots_older)
    else:
        skip_msg = f"No snapshots found older than {days_thr} in account {account_id}"
        print(skip_msg)
        logging.info(skip_msg)


def delete(ec2_client):
    with open('input.csv', 'r') as file:
        reader = csv.reader(file)
        input_list = [row[0].strip() for row in reader if row]
    for each_snap in input_list:
        try:
            ec2_client.delete_snapshot(SnapshotId=each_snap)
            del_msg = f"Successfully deleted: {each_snap}"
            print(del_msg)
            logging.info(del_msg)
        except ClientError as e:
            del_err_msg = f"Could not delete {each_snap}: {e.response['Error']['Message']}"
            print(del_err_msg)
            logging.error(del_err_msg)


if __name__ == '__main__':
    ec2 = boto3.client('ec2', region_name='us-east-1')
    choice = input("1. Fetch\n2. Delete\n\nchoice: ")
    if choice == '1':
        target_account = input("Enter the AWS Account ID: ")
        days_threshold = int(input("Enter days threshold (e.g., 30): "))
        fetch(ec2, target_account, days_threshold)
    else:
        delete(ec2)