# GuardarEnDB.py
import json
import boto3
import os

def handler(event, context):
    # Cliente de DynamoDB
    dynamodb_client = boto3.client('dynamodb')

    # Iterar sobre cada mensaje en la cola SQS
    for record in event['Records']:
        try:
            # Parsear el mensaje de SNS
            sns_message = json.loads(record['Sns']['Message'])
            job_id = sns_message['JobId']

            # Obtener tenant_id y fecha del job_id de la tabla de relación
            relation_response = dynamodb_client.get_item(
                TableName=os.environ['DYNAMODB_TABLE_RELACION'],
                Key={'job_id': {'S': job_id}}
            )
            tenant_id = relation_response['Item']['tenant_id']['S']
            fecha = relation_response['Item']['fecha']['S']

            # Guardar los resultados de Textract y la información asociada en DynamoDB
            dynamodb_client.put_item(
                TableName=os.environ['DYNAMODB_TABLE_REGISTROS'],
                Item={
                    'tenant_id': {'S': tenant_id},
                    'fecha': {'S': fecha},
                    'jobId': {'S': job_id},
                    'document_analysis': {'S': json.dumps(sns_message.get('DocumentAnalysis', {}))},
                    'status': {'S': 'COMPLETED'}
                }
            )

        except Exception as e:
            print(f"Error processing record {record}: {e}")
            # Aquí podrías agregar lógica adicional para manejar el error.

    # Devolver una respuesta de éxito
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Procesamiento completado'})
    }
