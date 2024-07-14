import json
import boto3


s3 = boto3.client('s3')
BUCKET_NAME = 'rr-xdel'

def lambda_handler(event, context):
    
    record = eval(json.loads(event['Records'][0]['body'])['Message'])
    print(record)
    
    tenant_id = record['tenant_id']
    order_id = record['order_id']
    
    json_content = generate_json(record)
    file_name = f"{tenant_id}_{order_id}.json"
    
    s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=json_content)
    
    return {
        'statusCode': 200,
        'body': json.dumps('JSON files generated and uploaded successfully.')
    }
    
    
def generate_json(data):
    return json.dumps(data, indent=4)
    