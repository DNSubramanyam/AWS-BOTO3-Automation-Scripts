import boto3
# from pprint import pprint
# from datetime import datetime

instance_id = "i-04694e9d68852903c"
metric_name = 'CPUUtilization'
Statistic = 'Average'
Threshold = 80
EvaluationPeriods = 3
DatapointsToAlarm = 2
Period = 30
Tags = [{'Key': 'Environment', 'Value': 'Prod'}]
ComparisonOperator = 'GreaterThanOrEqualToThreshold'
comp = '>='
metrics = {}
con = boto3.session.Session(profile_name='subbu')
alarm = con.client('cloudwatch', region_name='ap-south-1')

alarm_name = '_'.join([instance_id, metric_name, Statistic, comp+str(Threshold)+'%'])
response = alarm.list_metrics(MetricName=metric_name, Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}])
alarm.put_metric_alarm(Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}], Namespace=response['Metrics'][0]['Namespace'],  AlarmName = alarm_name, MetricName=metric_name, Statistic=Statistic, Period=Period, EvaluationPeriods=EvaluationPeriods, DatapointsToAlarm=DatapointsToAlarm, Threshold=Threshold, ComparisonOperator=ComparisonOperator, Tags=Tags)
waiter = alarm.get_waiter('alarm_exists')
waiter.wait(AlarmNames=[alarm_name])
print(f'Alarm {alarm_name} successfully created!')