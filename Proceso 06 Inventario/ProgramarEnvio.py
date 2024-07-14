import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tbl_envios')

def lambda_handler(event, context):
    
    record = eval(json.loads(event['Records'][0]['body'])['Message'])
    print(record)
    if not record:
        return {
            'statusCode': 400,
            'body': json.dumps('No se recibió ninguna encuesta para generar documento.')
        }

    tenant_id = record['tenant_id']
    product_id = record['product_id']
    quantity = record['quantity']
        
    order_id = record.get('order_id', str(uuid.uuid4()))
        
    table.put_item(
            Item={
                'tenant_id': tenant_id,
                'order_id': order_id,
                'product_id': product_id,
                'quantity': quantity,
                'status': 'scheduled'
            }
        )
    
   