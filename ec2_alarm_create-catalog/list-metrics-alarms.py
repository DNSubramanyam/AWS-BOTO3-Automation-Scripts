import boto3
from pprint import pprint
from datetime import datetime

con = boto3.session.Session(profile_name='subbu')
alarm = con.client('cloudwatch', region_name='ap-south-1')
metrics = {}
metrics_count = 0
associated_alarms = []
instance_id = 'i-02d110d25e24294fe'
print(f'Fetching all metrics and alarms for instance "{instance_id} ...!')
response = alarm.list_metrics(Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}])['Metrics']
for count, each in enumerate(response):
    metrics.setdefault(each['Namespace'], [])
    metrics[each['Namespace']].append(each['MetricName'])
    metrics_count = count
    r = alarm.describe_alarms_for_metric(MetricName=each['MetricName'], Namespace=each['Namespace'], Dimensions=each['Dimensions'])
    for i in r['MetricAlarms']:
        associated_alarms.append(i['AlarmName'])
print(f'\nFound "{metrics_count}" Metrics associated with "{len(metrics.keys())}" namespaces for the instance "{instance_id}", ')
pprint(metrics)
print(f'\nFound "{len(associated_alarms)}" alarms associated with metrics for instance "{instance_id}" : ')
if len(associated_alarms) > 0:
    pprint(associated_alarms)
