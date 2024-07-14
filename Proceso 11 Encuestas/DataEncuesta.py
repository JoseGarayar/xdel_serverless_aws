import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'tbl_encuestas'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Obtener el mensaje de la encuesta desde SNS
    record = json.loads(event['Records'][0]['Sns']['Message'])
    if not record:
        return {
            'statusCode': 400,
            'body': json.dumps('No se recibió ninguna encuesta para almacenar en DynamoDB.')
        }

    # Insertar encuesta en DynamoDB
    table.put_item(Item=record)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Encuesta almacenada en DynamoDB correctamente.')
    }