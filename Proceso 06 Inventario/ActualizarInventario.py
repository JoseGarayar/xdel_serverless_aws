import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tbl_inventario')

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
    
    table.update_item(
            Key={'tenant_id': tenant_id, 'product_id': product_id},
            UpdateExpression='SET quantity = quantity - :val',
            ExpressionAttributeValues={':val': quantity}
        )
        
    