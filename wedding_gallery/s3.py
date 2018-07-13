import uuid
from os import path

import boto3
from decouple import config

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
REGION = 'sa-east-1'
BUCKET_NAME = config('BUCKET_NAME')
IMAGES = 'static/images'

s3 = boto3.client('s3', region_name=REGION,
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


class S3Sevice:
    @classmethod
    def save(cls, file_obj, filename):
        print("Save photo")
        _, extension = filename.split('.')
        u2id = f"{str(uuid.uuid4())}.{extension}"
        try:
            img_path = path.join(IMAGES, u2id)
            resp = s3.upload_fileobj(file_obj, BUCKET_NAME, img_path, ExtraArgs={
                                     'ACL': 'public-read'})
        except s3.exceptions.NoSuchBucket as nobucket:
            print("No bucket")
        return u2id
