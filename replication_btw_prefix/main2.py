import boto3
import os

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']
    filename = source_key.split('/')[-1]
    
    destination_bucket = os.environ['DESTINATION_BUCKET']
    destination_key = os.environ['DESTINATION_PREFIX'] + filename
    
    copy_source = {
        'Bucket': source_bucket,
        'Key': source_key
    }
    try:
        s3_client.copy_object(
            Bucket=destination_bucket,
            Key=destination_key,
            CopySource=copy_source
        )
        print(f'successfully copied {source_key} from {source_bucket} to {destination_bucket}')
    except Exception as e:
        print(f'Error Copying Object: {str(e)}')
        raise e

if __name__ == '__main__':
    lambda_handler()