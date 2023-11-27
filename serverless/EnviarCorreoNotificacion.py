# EnviarCorreoNotificacion.py
import boto3
from botocore.exceptions import ClientError
import json

ses_client = boto3.client('ses')

def handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            new_image = record['dynamodb']['NewImage']
            email = new_image['email']['S']
            tenant_id = new_image['tenant_id']['S']
            file_name = new_image['file_name']['S']

            SENDER = "sender@example.com"
            RECIPIENT = email
            SUBJECT = "Notificación de Procesamiento Completo"
            BODY_TEXT = (f"El procesamiento del documento para el tenant {tenant_id} "
                         f"ha sido completado con éxito. Archivo procesado: {file_name}")

            try:
                response = ses_client.send_email(
                    Source=SENDER,
                    Destination={'ToAddresses': [RECIPIENT]},
                    Message={
                        'Body': {'Text': {'Data': BODY_TEXT}},
                        'Subject': {'Data': SUBJECT}
                    }
                )
            except ClientError as e:
                print(e.response['Error']['Message'])
            else:
                print(f"Email sent! Message ID: {response['MessageId']}")

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Notificaciones por correo enviadas'})
    }
