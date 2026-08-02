import boto3
import json

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'site781fe43f26b9eba3'
    
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        files = [obj['Key'] for obj in response.get('Contents', [])]
        
        flag_content = {}
        for f in files:
            try:
                obj = s3.get_object(Bucket=bucket_name, Key=f)
                flag_content[f] = obj['Body'].read().decode('utf-8')
            except Exception as e:
                flag_content[f] = str(e)
                
        return {
            'statusCode': 200,
            'body': json.dumps({'files': files, 'content': flag_content})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
