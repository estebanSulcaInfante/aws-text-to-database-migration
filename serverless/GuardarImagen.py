# GuardarImagen.py
import boto3
import json
import base64
import uuid
import os
from datetime import datetime
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

def handler(event, context):
    body = json.loads(event['body'])
    tenant_id = body['tenant_id']
    email = body['email']
    image_data = base64.b64decode(body['image'])
    image_uuid = str(uuid.uuid4())
    file_name = f"{tenant_id}/{image_uuid}.jpg"
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    try:
        # Guardar la imagen en S3
        s3_client.put_object(
            Bucket=os.environ['IMAGES_BUCKET'],
            Key=file_name,
            Body=image_data
        )

        # Enviar mensaje a SNS sobre la carga exitosa de la imagen
        sns_client.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Message=json.dumps({
                'tenant_id': tenant_id,
                'email': email,
                'file_name': file_name,
                'fecha': fecha_actual  # Incluir la fecha en el mensaje
            }),
            Subject='Imagen Guardada'
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Content-Type'},
            'body': json.dumps({
                'message': 'Imagen cargada y notificación enviada',
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

