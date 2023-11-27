# ExtraerTablas.py
import boto3
import json
import os

# Cliente de Textract y DynamoDB para invocar el análisis de documentos y guardar datos.
textract_client = boto3.client('textract')
dynamodb_client = boto3.client('dynamodb')

def handler(event, context):
    # Procesar cada mensaje de la cola SQS.
    for record in event['Records']:
        message_body = json.loads(record['body'])
        file_name = message_body['s3_key']
        tenant_id = message_body['tenant_id']
        email = message_body['email']

        # Invocar a Textract para procesar la imagen.
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
                'SNSTopicArn': os.environ['SNS_TOPIC_ARN']
            }
        )

        # Guardar el jobId, tenant_id y email en DynamoDB.
        dynamodb_client.put_item(
            TableName=os.environ['DYNAMODB_TABLE'],
            Item={
                'jobId': {'S': response['JobId']},
                'tenant_id': {'S': tenant_id},
                'email': {'S': email},
                'file_name': {'S': file_name},
                'status': {'S': 'PROCESSING'}  # Agregar un estado para el seguimiento.
            }
        )

        # Devolver una respuesta para indicar que el proceso ha comenzado.
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Inicio del análisis de Textract solicitado',
                'jobId': response['JobId']
            })
        }
