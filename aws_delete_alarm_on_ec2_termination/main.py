import boto3
from pprint import pprint
from datetime import datetime, timezone


def rem_alarms(alarm, instance_id, list_of_alarms):
    try:
        if len(list_of_alarms) > 0:
            print(f'\nDeleting fetched alarms for instance "{instance_id}"  ..!')
            alarm.delete_alarms(AlarmNames=list_of_alarms)
            execution_time = datetime.now(timezone.utc)
            print(
                f'\nSuccessfully deleted all alarms associated with instance "{instance_id}" at "{execution_time.strftime("%Y-%m-%d %H:%M:%S %Z")}" ...!')
        else:
            print(f'\nSkipping deletion process as there are no alarms associated with instance "{instance_id}" ..!')
    except Exception as error:
        print(f'\nDeletion of alarms failed with exception: "{error}')


def lambda_handler(event, context):
    alarm = boto3.client('cloudwatch', region_name='ap-south-1')
    metrics = {}
    metrics_count = 0
    associated_alarms = []
    instance_id = event['detail']['instance-id']
    termination_time = datetime.fromisoformat(event['time'][:-1] + '+00:00')
    print(
        f"Instance with ID '{instance_id}' is terminated at '{termination_time.strftime('%Y-%m-%d %H:%M:%S %Z')}' in region '{event['region']}'\n")
    try:
        response = alarm.list_metrics(Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}])['Metrics']
        for count, each in enumerate(response):
            metrics.setdefault(each['Namespace'], [])
            metrics[each['Namespace']].append(each['MetricName'])
            metrics_count = count
            r = alarm.describe_alarms_for_metric(MetricName=each['MetricName'], Namespace=each['Namespace'],
                                                 Dimensions=each['Dimensions'])
            for i in r['MetricAlarms']:
                associated_alarms.append(i['AlarmName'])
        print(f'\nFound "{metrics_count}" Metrics associated with "{len(metrics.keys())}" namespaces for the instance "{instance_id}", ')
        pprint(metrics)
        print(f'\nFound "{len(associated_alarms)}" alarms associated with metrics for instance "{instance_id}" : ')
        if len(associated_alarms) > 0:
            pprint(associated_alarms)
    except Exception as error:
        print(f'\nFetching of alarms and metrics failed with exception: "{error}"')
        return

    rem_alarms(alarm, instance_id, associated_alarms)
