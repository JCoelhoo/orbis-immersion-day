import json
import boto3

ddb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = ddb.Table('orbis_ddb')
    
    response = table.scan()
    data = response['Items']
    
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
