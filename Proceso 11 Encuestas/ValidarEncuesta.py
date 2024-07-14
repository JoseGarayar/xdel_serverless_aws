import json
import boto3

sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/940812169740/sqs-encuestas'

def lambda_handler(event, context):
    
    # Realizar validaciones específicas
    required_fields = ["cliente_id", "comentarios", "tenant_id", "encuesta_id"]
    for field in required_fields:
        if field not in event:
            return {
                'statusCode': 400,
                'body': json.dumps(f'Falta el campo requerido: {field}')
            }
    
    # Enviar encuesta validada a SQS
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(event)
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Encuesta validada y enviada a SQS correctamente.'),
        'messageId': response['MessageId']
    }