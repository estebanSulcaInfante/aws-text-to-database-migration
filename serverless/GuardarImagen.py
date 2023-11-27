#GuardarImagen.py
import boto3
import json
import base64
import uuid
import os

s3_client = boto3.client('s3')
sqs_client = boto3.client('sqs')

def handler(event, context):
    body = json.loads(event['body'])
    tenant_id = body['tenant_id']
    email = body['email']
    image_data = base64.b64decode(body['image'])
    image_uuid = str(uuid.uuid4())
    file_name = f"{tenant_id}/{image_uuid}.jpg"

    try:
        # Guardar la imagen en S3
        s3_client.put_object(
            Bucket=os.environ['IMAGES_BUCKET'],
            Key=file_name,
            Body=image_data
        )

        # Enviar mensaje a SQS para procesar la imagen con Textract
        sqs_client.send_message(
            QueueUrl=os.environ['SQS_EXTRAER_TABLAS_URL'],
            MessageBody=json.dumps({
                'tenant_id': tenant_id,
                'email': email,
                'file_name': file_name
            })
        )
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Content-Type'},
            'body': json.dumps({
                'message': 'Imagen cargada y mensaje enviado a SQS',
                'file_name': file_name
            })
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': 'Error al procesar la imagen'})
        }
