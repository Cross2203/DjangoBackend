import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from uuid import uuid4

s3 = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

def upload_file_to_s3(file, folder_name):
    try:
        unique_filename = f"{uuid4()}-{file.name}"
        object_key = f"{folder_name}/{unique_filename}"

        s3.upload_fileobj(
            file,
            settings.S3_BUCKET_NAME,
            object_key,
            ExtraArgs={'ACL': 'public-read'}
        )

        file_url = f"https://{settings.S3_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{object_key}"
        return file_url

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"Error al subir el archivo a S3: {error_code} - {error_message}")
        raise e
    except Exception as e:
        print(f"Error inesperado al subir el archivo a S3: {e}")
        raise e