import boto3
from flask import current_app

def get_dynamo_client():
    return boto3.resource(
        'dynamodb',
        endpoint_url=current_app.config['DYNAMODB_ENDPOINT'],
        region_name=current_app.config['AWS_REGION'],
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
    )

def create_user_table():
    dynamodb = get_dynamo_client()
    table = dynamodb.create_table(
        TableName='Users',
        KeySchema=[
            {
                'AttributeName': 'username',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'username',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    return table

def create_post_table():
    dynamodb = get_dynamo_client()
    table = dynamodb.create_table(
        TableName='BlogPosts',
        KeySchema=[
            {
                'AttributeName': 'post_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'post_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    return table
