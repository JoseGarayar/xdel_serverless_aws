import json
import boto3
import random

sns_client = boto3.client('sns')

def lambda_handler(event, context):
    tenant_id = event['tenant_id']
    payment_info = event['payment_info']
    
    # Simulando el procesamiento de pago
    success_rate = 0.9999999
    payment_successful = random.random() <  success_rate
    
    if payment_successful:
        # Enviar notificación a SNS
        message = {
            'tenant_id': tenant_id,
            'status': 'Pago exitoso',
            'payment_info': payment_info
        }
        print(message)
        response = sns_client.publish(
            TopicArn='arn:aws:sns:us-east-1:056169544678:TemaProcesarPago',
            Subject = 'Nueva Factura añadida',
            Message = json.dumps(message)
        )
        
        return {
            'statusCode': 200,
            'body': response
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Error en el procesamiento del pago')
        }
