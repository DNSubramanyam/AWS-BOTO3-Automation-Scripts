import boto3
import copy
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

base_config = {
    'Rules': [
        {
            'ID': 'MoveToIntelligentTiering',
            'Filter': {
                'Prefix': ''  # Apply to all objects
            },
            'Status': 'Enabled',
            'Transitions': [
                {
                    'Days': 30,  # Move to Intelligent-Tiering immediately
                    'StorageClass': 'INTELLIGENT_TIERING'
                }
            ]
        }
    ]
}

def put_block(buck, lfconfig):
        response = s3.put_bucket_lifecycle_configuration(
            Bucket=buck,
            LifecycleConfiguration=lfconfig
        )
        print(f"BucketName: {buck}, StatusCode: {response['ResponseMetadata']['HTTPStatusCode']}")


def config_prep(input_list):
    for buck in input_list:
        lifecycle_configuration = copy.deepcopy(base_config)
        try:
            response = s3.get_bucket_lifecycle_configuration(Bucket=buck)
            lifecycle_configuration['Rules'].extend(response['Rules'])

            seen_ids = set()
            duplicates = set()

            for rule in lifecycle_configuration['Rules']:
                rule_id = rule['ID']
                if rule_id in seen_ids:
                    duplicates.add(rule_id)
                else:
                    seen_ids.add(rule_id)
            if duplicates:
                print(f"BucketName: {buck}, Duplicate IDs found: {duplicates}")
                continue
            else:
                put_block(buck, lifecycle_configuration)
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchLifecycleConfiguration":
                put_block(buck, lifecycle_configuration)

def main_handler():
    file_name = input("Enter the file name : ")
    try:
        with open(file_name, 'r') as file:
            input_data = file.read().strip()
        input_list = input_data.split('\n')
        input_list = [i for i in input_list if i]
        print(f"Number of buckets: {len(input_list)}")
        config_prep(input_list)
    except Exception as error:
        print(error)

if __name__ == '__main__':
    main_handler()

