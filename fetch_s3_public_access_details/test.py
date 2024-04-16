import boto3
from pprint import pprint
from botocore.exceptions import ClientError

each_dict = {}
final_data = []
con = boto3.session.Session(profile_name='subbu')
st = con.client('s3')

response = st.list_buckets()
for buck in response['Buckets']:
    try:
        response = st.get_public_access_block(Bucket=buck['Name'])
        if response['PublicAccessBlockConfiguration']['BlockPublicAcls'] == True and response['PublicAccessBlockConfiguration']['BlockPublicPolicy'] == True:
            #pprint('Bucket and objects not public')
            output = 'Bucket and objects not public'
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
            #print('Objects can be public')
            output = 'Objects can be public'
        else:
            #print(e.response['Error']['Code'])
            output = e.response['Error']['Code']
    print(f"{buck['Name']} : {output}")
