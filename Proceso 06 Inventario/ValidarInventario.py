import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

INVENTORY_TABLE = 'tbl_inventario'
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:859248659685:XDelInventoryUpdates'


def lambda_handler(event, context):
    # Check if the event is from API Gateway
    if 'body' in event:
        request_body = json.loads(event['body'])
    else:
        # For testing purposes or direct Lambda invocation
        request_body = event
    
    print(request_body)
    
    print(request_body['tenant_id'])
    
    tenant_id = request_body['tenant_id']
    product_id = request_body['product_id']
    quantity = request_body['quantity']
    order_id = request_body['order_id']
    
    # Validate inventory
    table = dynamodb.Table(INVENTORY_TABLE)
    response = table.get_item(Key={'tenant_id': tenant_id, 'product_id': product_id})
    
    if 'Item' in response and response['Item']['quantity'] >= quantity:
        # Update inventory and send SNS notification
        #table.update_item(
        #    Key={'tenant_id': tenant_id, 'product_id': product_id},
        #    UpdateExpression='SET quantity = quantity - :val',
        #    ExpressionAttributeValues={':val': quantity}
        #)
        
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=json.dumps({'tenant_id': tenant_id, 'product_id': product_id, 'quantity': quantity, 'order_id': order_id}),
            Subject='Inventory Update'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Inventory updated successfully')
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Insufficient inventory')
        }
