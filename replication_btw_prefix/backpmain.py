import boto3

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']
    filename = source_key.split('/')[-1]
    
    destination_bucket = 'ssm-distributer-storeroom'
    destination_key = 'target/data/' + filename
    
    copy_source = {
        'Bucket': source_bucket,
        'Key': source_key
    }
    s3_client.copy_object(
        Bucket=destination_bucket,
        Key=destination_key,
        CopySource=copy_source
    )