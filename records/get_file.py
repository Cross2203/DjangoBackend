import boto3
from django.conf import settings

# Configura las credenciales de AWS
s3 = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)
 
print(s3)

def get_s3_file_url(object_name, folder_name):
    object_key = f"{folder_name}/{object_name}"
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': settings.S3_BUCKET_NAME, 'Key': object_key},
        ExpiresIn=3600  
    )
    return url
