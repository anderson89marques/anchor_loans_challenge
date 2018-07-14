"""settings"""
from decouple import config

IMAGES = "static/images"
STATIC_URL = f"https://s3-{config('REGION')}.amazonaws.com/{config('BUCKET_NAME')}/{IMAGES}"
