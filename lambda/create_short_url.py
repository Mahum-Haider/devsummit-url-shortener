import json
import boto3
import random
import string
from boto3.dynamodb.conditions import Key

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('devsummit-links')

def generate_short_code():
    # Creates a random 6-character code like "abc123"
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

def lambda_handler(event, context):
    try:
        # Get the original URL from the request
        body = json.loads(event['body'])
        original_url = body['url']

        # Check if this URL was already shortened (GSI lookup)
        existing = table.query(
            IndexName='original-url-index',
            KeyConditionExpression=Key('original_url').eq(original_url)
        )

        # If it exists, return the existing short code
        if existing['Items']:
            short_code = existing['Items'][0]['short_code']
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'short_code': short_code,
                    'message': 'URL already shortened'
                })
            }

        # Generate a new short code and save to DynamoDB
        short_code = generate_short_code()
        table.put_item(Item={
            'short_code': short_code,
            'original_url': original_url,
            'click_count': 0
        })

        return {
            'statusCode': 201,
            'body': json.dumps({
                'short_code': short_code,
                'message': 'Short URL created successfully'
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
