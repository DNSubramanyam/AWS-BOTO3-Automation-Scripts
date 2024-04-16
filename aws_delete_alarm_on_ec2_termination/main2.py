import boto3
from pprint import pprint
from datetime import datetime

def lambda_handler(event, context):
    alarm = boto3.client('cloudwatch', region_name='ap-south-1')
    metrics = {}
    metrics_count = 0
    associated_alarms = []
    instance_id = event['detail']['instance-id']
    termination_time = datetime.fromisoformat(event['time'][:-1] + '+00:00')
    print(f"Instance with ID '{instance_id}' is terminated at '{termination_time.strftime('%Y-%m-%d' '%-H:%M:%S %Z')}' in region '{event['region']}'\n")
    try:
        print(f'\nFetching all the metrics associated with instance "{instance_id}" ....!')
        for count, each in enumerate(alarm.list_metrics(Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}])[
                                         'Metrics'], 1):
            metrics.setdefault(each['Namespace'], [])
            metrics[each['Namespace']].append(each['MetricName'])
            metrics_count = count
        print(
            f'\nFound "{metrics_count}" Metrics associated with "{len(metrics.keys())}" namespaces for the instance "{instance_id}", ')
        # pprint(metrics)
    except Exception as error:
        print(f'\nFetching of metrics failed with exception: "{error}')

    try:
        print('\nFetching all the alarms associated with metrics ....!')
        for namespaces in metrics.keys():
            for each_metric in metrics[namespaces]:
                for alarms in alarm.describe_alarms_for_metric(MetricName=each_metric, Namespace=namespaces,
                                                               Dimensions=[
                                                                   {'Name': 'InstanceId', 'Value': instance_id}])[
                    'MetricAlarms']:
                    associated_alarms.append(alarms['AlarmName'])
        print(f'\nFound "{len(associated_alarms)}" alarms associated with metrics for instance {instance_id} : ')
        if len(associated_alarms) > 0:
            pprint(associated_alarms)
    except Exception as error:
        print(f'\nFetching of alarms failed with exception: "{error}')

    try:
        if len(associated_alarms) > 0:
            print(f'\nDeleting fetched alarms for instance "{instance_id}"  ..!')
            alarm.delete_alarms(AlarmNames=associated_alarms)
            print(f'\nSuccessfully deleted all alarms associated with instance "{instance_id}" ...!')
        else:
            print(f'\nSkipping deletion process as there are no alarms associated with instance "{instance_id}" ..!')
    except Exception as error:
        print(f'\nDeletion of alarms failed with exception: "{error}')
