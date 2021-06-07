import json
import boto3

def lambda_handler(event, context):
    db = boto3.resource('dynamodb')
    table = db.Table('locations')
    cities = json.loads(event['body'])
    if type(cities) == type([]):
        for i in cities:
            table.put_item(
                Item=i
            )
            
        return {
            'statusCode': 201,
            'body': json.dumps('Added successfully')
        }
        
    else:
        return {
        'statusCode': 400,
        'body': json.dumps('Request not in required format')
    }
    
    
