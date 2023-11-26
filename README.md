# Multi-Tenant Data Processing with AWS Textract

## Descripción General
Este proyecto implementa una solución serverless en AWS para procesar imágenes de tablas con datos de producción diaria. Utiliza AWS Textract para el reconocimiento óptico de caracteres (OCR) y almacena los resultados en una base de datos DynamoDB siguiendo una arquitectura multi-tenant.

## Arquitectura
- **AWS Lambda**: Funciones para el procesamiento de imágenes y manejo de eventos.
- **Amazon S3**: Almacenamiento de imágenes subidas.
- **Amazon DynamoDB**: Almacenamiento de datos procesados en tablas multi-tenant.
- **Amazon SNS y SQS**: Enrutamiento y manejo de eventos.
- **EventBridge** (opcional): Para tareas programadas y simulación de eventos.

## Requisitos
- Cuenta AWS con acceso a Lambda, S3, DynamoDB, SNS, SQS, y (opcionalmente) EventBridge.
- AWS CLI configurado en tu máquina local.
- Conocimientos en Python para el desarrollo de funciones Lambda.

## Instalación y Configuración
1. Clona el repositorio a tu máquina local.
2. Configura tus credenciales AWS y la región preferida.
3. Despliega las funciones Lambda utilizando AWS CLI o AWS SAM.
4. Crea las tablas necesarias en DynamoDB siguiendo el esquema multi-tenant.
5. Configura los buckets de S3 y los temas de SNS según sea necesario.
6. (Opcional) Configura EventBridge para la generación de eventos simulados.

## Uso
1. Sube las imágenes de las tablas a S3.
2. Las funciones Lambda procesarán automáticamente las imágenes y extraerán los datos utilizando Textract.
3. Los datos procesados se almacenarán en DynamoDB.
4. Monitorea y gestiona los eventos a través de SNS y SQS.

## Contribuir
Este proyecto está abierto a contribuciones. Si deseas mejorar la funcionalidad o añadir nuevas características, no dudes en crear un fork y enviar tus pull requests.

## Licencia
Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo LICENSE en el repositorio para más detalles.
