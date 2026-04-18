import json
import boto3
from boto3.dynamodb.conditions import Key

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('devsummit-links')

def lambda_handler(event, context):
    try:
        # Get the short code from the URL path
        short_code = event['pathParameters']['short_code']

        # Look up the short code in DynamoDB
        response = table.get_item(
            Key={'short_code': short_code}
        )

        # If code doesn't exist, return 404
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Short code not found'})
            }

        # Get the original URL
        original_url = response['Item']['original_url']

        # Increment the click counter by 1
        table.update_item(
            Key={'short_code': short_code},
            UpdateExpression='SET click_count = click_count + :val',
            ExpressionAttributeValues={':val': 1}
        )

        # Redirect the attendee to the original URL
        return {
            'statusCode': 301,
            'headers': {
                'Location': original_url
            },
            'body': ''
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
