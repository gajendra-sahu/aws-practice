import boto3
import gzip
import json
import time
from datetime import datetime

# Initialize AWS SDK clients
logs_client = boto3.client('logs')
s3_client = boto3.client('s3')

# S3 bucket name (update with your S3 bucket name)
S3_BUCKET_NAME = 'asdfghjknk'

# CloudWatch Log Group and Log Stream
LOG_GROUP = 'devops-veera'
LOG_STREAM = 'devops'

def lambda_handler(event, context):
    # Get the current timestamp for the file name
    timestamp = time.time()
    file_name = f'logs-{int(timestamp)}.json.gz'
    
    # Get log events from CloudWatch
    log_events = []
    response = logs_client.get_log_events(
        logGroupName=LOG_GROUP,
        logStreamName=LOG_STREAM,
        startTime=int(time.time() - 86400) * 1000,  # Get logs from the last 24 hours (in milliseconds)
        endTime=int(time.time()) * 1000,
        limit=10000  # Adjust based on the number of logs you want to fetch
    )
    
    # Loop through the response to collect log events
    for event in response['events']:
        log_events.append(event)
    
    # Compress logs to gzip format
    log_data = json.dumps(log_events, default=str)
    compressed_log_data = gzip.compress(log_data.encode('utf-8'))
    
    # Upload to S3
    s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=f'cloudwatch-logs/{file_name}',
        Body=compressed_log_data,
        ContentType='application/gzip'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Logs exported successfully')
    }
