import json
import boto3

sns = boto3.client('sns')
topic_arn = 'arn:aws:sns:us-east-1:940812169740:Encuestas'

def lambda_handler(event, context):
    # Obtener el mensaje de la encuesta desde SQS
    records = event.get('Records', [])
    if not records:
        return {
            'statusCode': 400,
            'body': json.dumps('No se recibió ninguna encuesta para procesar.')
        }
    
    for record in records:
        encuesta = json.loads(record['body'])
        
        # Procesar datos de la encuesta (ejemplo de transformación de datos)
        encuesta_procesada = {
            'cliente_id': encuesta['cliente_id'],
            'comentarios': encuesta['comentarios'].upper(),  # Ejemplo de procesamiento
            'tenant_id': encuesta['tenant_id'],
            'encuesta_id': encuesta['encuesta_id'],
            'fecha': encuesta.get('fecha', 'Fecha no proporcionada')
        }
        
        # Publicar la encuesta procesada en SNS
        response = sns.publish(
            TopicArn=topic_arn,
            Message=json.dumps(encuesta_procesada),
            Subject='Encuesta Procesada'
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Encuesta procesada y enviada a SNS correctamente.')
    }