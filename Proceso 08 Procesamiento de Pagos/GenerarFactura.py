import json
import boto3

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    payload= eval(json.loads(event['Records'][0]['body'])['Message'])
    tenant_id = payload['tenant_id']
    payment_info = payload['payment_info']
    
    json_file_content = json.dumps(payment_info, indent=4)
    json_file_path = f"/tmp/factura_{payment_info['payment_id']}.json"
    
    with open(json_file_path, 'w') as json_file:
        json_file.write(json_file_content)
    
    bucket_name = 'xdel-project'
    s3_key = f"facturas/factura_{payment_info['payment_id']}.json"
    
    try:
        s3_client.upload_file(json_file_path, bucket_name, s3_key)
        print(f"Factura subida a {s3_key} en el bucket {bucket_name}")
        return {
            'statusCode': 200,
            'body': json.dumps('Factura generada y guardada en S3')
        }
    except Exception as e:
        print(f"Error subiendo la factura a S3: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error subiendo la factura a S3: {e}")
        }