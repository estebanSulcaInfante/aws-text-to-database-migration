# GuardarEnDB.py
import boto3
import json
import os

# Cliente de DynamoDB para guardar datos.
dynamodb_client = boto3.client('dynamodb')

def handler(event, context):
    for record in event['Records']:
        sns_message = json.loads(record['Sns']['Message'])
        job_id = sns_message['JobId']

        # Recuperar tenant_id y email asociados con job_id de DynamoDB.
        response = dynamodb_client.get_item(
            TableName=os.environ['DYNAMODB_TABLE'],
            Key={'jobId': {'S': job_id}}
        )

        tenant_id = response['Item']['tenant_id']['S']
        email = response['Item']['email']['S']
        file_name = response['Item']['file_name']['S']

        # Procesar los resultados de Textract aquí y transformarlos si es necesario.

        # Guardar los datos procesados en la tabla DynamoDB.
        processed_data = {
            'jobId': {'S': job_id},
            'tenant_id': {'S': tenant_id},
            'email': {'S': email},
            'file_name': {'S': file_name},
            'document_analysis': {'S': json.dumps(sns_message['DocumentAnalysis'])}, # Suponiendo que 'DocumentAnalysis' está en el mensaje.
            'status': {'S': 'COMPLETED'}
        }

        dynamodb_client.put_item(
            TableName=os.environ['DYNAMODB_TABLE_PROCESSED'],
            Item=processed_data
        )

        # Opcional: Aquí podrías invocar la función de notificación por correo electrónico
        # o simplemente dejar que el trigger de DynamoDB se haga cargo de ello.
        # ...

        # Devolver una respuesta de éxito.
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Datos procesados y guardados en DynamoDB'
            })
        }
