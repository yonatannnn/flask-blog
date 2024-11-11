import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dummy_secret_key')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

    # Local DynamoDB configuration
    if os.getenv("USE_LOCAL_DYNAMODB"):
        DYNAMODB_ENDPOINT = "http://localhost:8000"
        AWS_ACCESS_KEY_ID = "local"
        AWS_SECRET_ACCESS_KEY = "local"
    else:
        DYNAMODB_ENDPOINT = None
        AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
