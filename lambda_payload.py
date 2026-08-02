import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'site781fe43f26b9eba3'
    
    # Try to list objects or read a flag file from the bucket
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        files = [obj['Key'] for obj in response.get('Contents', [])]
        
        # If there's a flag file or index, read it
        flag_content = ""
        for file in files:
            if 'flag' in file.lower() or 'txt' in file.lower():
                obj = s3.get_object(Bucket=bucket_name, Key=file)
                flag_content += f"\n--- {file} ---\n" + obj['Body'].read().decode('utf-8')
                
        result_data = {
            "files": files,
            "flag_content": flag_content
        }
    except Exception as e:
        result_data = {"error": str(e)}

    return {
        "statusCode": 200,
        "body": json.dumps(result_data)
    }
