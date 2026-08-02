import subprocess
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'site781fe43f26b9eba3'

    # List files and read them
    response = s3.list_objects_v2(Bucket=bucket_name)
    logger.info("S3 Objects: %s", response)

    for obj in response.get('Contents', []):
        key = obj['Key']
        try:
            file_obj = s3.get_object(Bucket=bucket_name, Key=key)
            logger.info("FILE CONTENT [%s]:\n%s", key, file_obj['Body'].read().decode('utf-8'))
        except Exception as e:
            logger.error("Error reading %s: %s", key, e)

    return {"statusCode": 200, "body": "Done"}
