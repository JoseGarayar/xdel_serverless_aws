import json
import boto3

s3 = boto3.client('s3')
bucket_name = 'encuestas'

def lambda_handler(event, context):
    record = json.loads(event['Records'][0]['Sns']['Message'])
    if not record:
        return {
            'statusCode': 400,
            'body': json.dumps('No se recibió ninguna encuesta para generar documento.')
        }
        
    # Generar documento (ejemplo simple en JSON)
    documento = json.dumps(record, indent=4)
    file_name = f"documentos/{record['tenant_id']}/encuesta_{record['encuesta_id']}.json"
    
    # Guardar documento en S3
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=documento
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Documento generado y guardado en S3: {file_name}')
    }