import boto3

def get_textract_job_status(job_id):
    # Cliente de Textract
    textract_client = boto3.client('textract')

    # Llamar a la API correcta dependiendo del tipo de trabajo que se haya iniciado.
    # Para análisis de documentos:
    response = textract_client.get_document_analysis(JobId=job_id)
    
    # Para detección de texto:
    # response = textract_client.get_document_text_detection(JobId=job_id)

    # El estado del trabajo
    status = response['JobStatus']
    print(f"Job Status: {status}")

    # Aquí puedes agregar lógica adicional basada en el estado del trabajo
    # Por ejemplo, manejar el estado 'SUCCEEDED', 'FAILED', etc.

    return status

# Reemplaza 'your_job_id' con el ID real de tu trabajo
job_id = '49d7258a2b633151b181f01346ed802e0d99de74478926a74a44ec7b60e74ea4'
get_textract_job_status(job_id)
