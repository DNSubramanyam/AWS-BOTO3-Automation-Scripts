import boto3
from pprint import pprint
import csv

con = boto3.session.Session()
s3 = con.client('s3')


response = s3.list_buckets()

with open("op_file.csv", 'w', newline='') as writefile: 
        writer = csv.writer(writefile)
        writer.writerow(['BucketName' , 'Size(KiB)', 'Rules', 'RuleCount'])
        for buck in response['Buckets']:
            #pprint(buck['Name'])
            rules = []
            resp = ''
            total_size = 0
            size_round = 0
            try:
                  response1 = s3.get_bucket_lifecycle_configuration(Bucket=buck['Name'])
                  for each in response1['Rules']:
                        rules.append(each['ID'])
            except:
                  rules.append('No Lifecycle Rules')
            resp = s3.list_objects_v2(Bucket=buck['Name'])
            total_size = sum([obj.get('Size') for obj in resp.get('Contents')])
            while resp.get('NextContinuationToken'):
                resp = s3.list_objects_v2(Bucket=buck['Name'], ContinuationToken=resp.get('NextContinuationToken'))
                total_size += sum([obj.get('Size') for obj in resp.get('Contents')])
            size_round = round((total_size/1024),2)
            writer.writerow([buck['Name'], size_round, ','.join(rules), len(rules)])