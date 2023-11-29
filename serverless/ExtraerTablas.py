# ExtraerTablas.py
import boto3
import json
import os
textract_client = boto3.client('textract')
dynamodb_client = boto3.client('dynamodb')

def handler(event, context):
    # Fecha actual para la clave de ordenación

    for record in event['Records']:
        message_body = json.loads(record['body'])
        sns_message = json.loads(message_body['Message'])
        file_name = sns_message['file_name']
        tenant_id = sns_message['tenant_id']
        email = sns_message['email']
        print("Mensaje recibido de SNS:", sns_message)  # Imprimir el mensaje para depuración
        fecha = sns_message.get('fecha')
        if fecha is None:
            print("Error: El mensaje no contiene 'fecha'.", sns_message)
            continue  # S
        
        # Iniciar el análisis del documento con Textract.
        response = textract_client.start_document_analysis(
            DocumentLocation={
                'S3Object': {
                    'Bucket': os.environ['IMAGES_BUCKET'],
                    'Name': file_name
                }
            },
            FeatureTypes=['TABLES'],
            NotificationChannel={
                'RoleArn': os.environ['TEXTRACT_ROLE_ARN'],
                'SNSTopicArn': os.environ['TEXTRACT_SNS_TOPIC_ARN']
            }
        )

        print("Respuesta de Textract:", response)  # Imprimir la respuesta para depuración
        job_id = response['JobId']
        
        # Guardar la relación job_id con tenant_id y fecha
        dynamodb_client.put_item(
            TableName=os.environ['DYNAMODB_TABLE_RELACION'],
            Item={
                'job_id': {'S': job_id},
                'tenant_id': {'S': tenant_id},
                'fecha': {'S': fecha}
            }
        )
        
        # Guardar la información relevante en DynamoDB.
        dynamodb_client.put_item(
            TableName=os.environ['DYNAMODB_TABLE_REGISTROS'],  # Asegúrate de que esta es la tabla correcta
            Item={
                'tenant_id': {'S': tenant_id},  # Clave de partición
                'fecha': {'S': fecha},  # Usar la fecha del mensaje                'jobId': {'S': response['JobId']},
                'email': {'S': email},
                'file_name': {'S': file_name},
                'status': {'S': 'PROCESSING'}
            }
        )
        
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Proceso de Textract iniciado'})
    }
