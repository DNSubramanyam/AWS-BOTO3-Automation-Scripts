from pprint import pprint
data = """
{'Records': [{'awsRegion': 'us-east-1',
'eventName': 'ObjectCreated:Put',
'eventSource': 'aws:s3',
'eventTime': '2025-09-05T04:51:48.462Z',
'eventVersion': '2.1',
'requestParameters': {'sourceIPAddress': '49.205.104.200'},
'responseElements': {'x-amz-id-2': 'H6zKEBp15BRxJx4e/30PzhGq0wYnaPwQUoswBKJbMjlyDJ7mf/lih9OEz/PbCmOK+0v1Y981fddQLnKqseDNmng26Kn2YuFAjdZSm/dfUbU=',
'x-amz-request-id': 'SRFVKK5DQTBDVH4C'},
's3': {'bucket': {'arn': 'arn:aws:s3:::run-command-logs-v64',
'name': 'run-command-logs-v64',
'ownerIdentity': {'principalId': 'A2KAA569ZQDBPQ'}},
'configurationId': 'replic-btw-prefix',
'object': {'eTag': '60adc29be40ead763b0ef4bf6ebbd947',
'key': 'source/data/test.txt',
'sequencer': '0068BA6C646BC2BCB3',
'size': 7916},
's3SchemaVersion': '1.0'},
'userIdentity': {'principalId': 'AWS:AIDAVK374GBEKZLNMVADP'}}]}

"""

pprint(data)