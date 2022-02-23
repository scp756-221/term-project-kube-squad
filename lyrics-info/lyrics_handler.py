from urllib import response
import boto3
import csv
import uuid
import os
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from decouple import config

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
REGION_NAME = config("REGION_NAME")
import uuid

client = boto3.client(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)

resource = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)

LyricsTable = resource.Table('lyrics_info')

def get_lyrics_info(music_id):

    try:
        resp = LyricsTable.query(
            KeyConditionExpression=Key('music_id').eq(music_id)
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return resp['Items'][0]

def create_table_lyrics_info():
    client.create_table(
        AttributeDefinitions=[
        {
            "AttributeName": "music_id",
            "AttributeType": "S"
        }
        ],
        TableName = 'lyrics_info',
        KeySchema = [
        {
            "AttributeName": "music_id",
            "KeyType": "HASH"
        }                      
        ],
        BillingMode='PAY_PER_REQUEST'        
    )                      

def populate_lyrics_info_table():
    with open('music_info.csv', 'r') as inp:
        rdr = csv.reader(inp)
        next(rdr)  # Skip header
        for music_id, lyrics, num_sales, record_company, release_date in rdr:
            resp = LyricsTable.put_item(
                Item = {
                    'music_id': str(music_id),
                    'lyrics': lyrics,
                    'num_sales': str(num_sales),
                    'record_company': str(record_company),
                    'release_date': str(release_date)
                })
            print(resp)     