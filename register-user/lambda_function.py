import json
import hashlib
import boto3
from boto3.dynamodb.conditions import Key


def email_exists(table, email):
    record = table.query(
        KeyConditionExpression=Key('email').eq(email)
    )
    items = record['Items']
    if items:
        return items[0]
    return False
    
    
def put_item(table, email, username, password):
    pass_hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
    table.put_item(
        Item={
            'email': email,
            'username': username,
            'password': pass_hashed
        }
    )
    

def lambda_handler(event, context):
    db = boto3.resource('dynamodb')
    table = db.Table('users')
    
    body = json.loads(str(event['body']))
    
    if body['email'].strip() == '':
        return {
            'statusCode': 400,
            'body': 'Email required for registration'
        }
        
    elif body['username'].strip() == '':
        return {
            'statusCode': 400,
            'body': 'Username required for registration'
        }
        
    elif body['password'].strip() == '':
        return {
            'statusCode': 400,
            'body': 'Password required for registration'
        }
        
    response = email_exists(table, body['email'])
    if response != False:
        return {
            'statusCode': 409,
            'body': 'Email already exists: ' + response['email'],
        }
        
    else:
        put_item(table, body['email'], body['username'], body['password'])
        return {
            'statusCode': 201,
            'body': 'User created successfully'
        }
    