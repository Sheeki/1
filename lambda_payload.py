import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'site781fe43f26b9eba3'
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        files = [obj['Key'] for obj in response.get('Contents', [])]
        
        flag_content = ""
        for file in files:
            obj = s3.get_object(Bucket=bucket_name, Key=file)
            try:
                content = obj['Body'].read().decode('utf-8')
                flag_content += f"\n=== {file} ===\n{content}\n"
            except Exception:
                pass
                
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
