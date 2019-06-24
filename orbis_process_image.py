import json
import boto3
import uuid 

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    rekognition = boto3.client('rekognition')
    uid = str(uuid.uuid4())
    
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    
    table = dynamodb.Table('orbis_ddb') 
    print(bucket,key)
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key,
            }
        }
    )['Labels']
    
    tags = [tag['Name'] for tag in response]

    table.put_item(
       Item={
            'uuid': uid,
            'location': "%s/%s" % (bucket,key),
            'tags':str(tags)
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
