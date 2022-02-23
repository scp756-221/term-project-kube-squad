import boto3

# aws dynamodb create-table --cli-input-json file://create-table.json
# aws dynamodb batch-write-item --request-items file://batch-write.json

# def get_items():
#     return dynamo_client.scan(
#         TableName=''
#     )

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

# BookTable = resource.Table('Book')
PlaylistTable = resource.Table('playlist')
MusicTable = resource.Table('music')



def CreateTablePlaylist():
    client.create_table(
        AttributeDefinitions=[
        {
            "AttributeName": "playlist_uuid",
            "AttributeType": "S"
        },
        {
            "AttributeName": "playlist_name",
            "AttributeType": "S"
        },
        # {
        #     "AttributeName": "user_id",
        #     "AttributeType": "S"
        # },
        ],
        TableName='playlist',
        KeySchema=[
            {
                "AttributeName": "playlist_uuid",
                "KeyType": "HASH"
            },
             { 
                 "AttributeName": "playlist_name", 
                "KeyType": "RANGE" 
             }
        ],
        # ref: https://highlandsolutions.com/blog/hands-on-examples-for-working-with-dynamodb-boto3-and-python
        # LocalSecondaryIndexes=[
        #     {
        #         'IndexName': 'user_name_subject',
        #         'KeySchema': [
        #             {
        #                 'AttributeName': 'user_id',
        #                 'KeyType': 'HASH'
        #             },
        #             {
        #                 'AttributeName': 'playlist_name',
        #                 'KeyType': 'RANGE'
        #             },
        #         ],
        #         'Projection': {
        #             'ProjectionType': 'ALL'
        #         },
        #     }
        # ],
    #     GlobalSecondaryIndexUpdates=[
    #     {
    #         'Create': {
    #             'IndexName': 'user_data',
    #             'KeySchema': [
    #                 {
    #                     'AttributeName': 'user_id',
    #                     'KeyType': 'HASH'
    #                 },
    #                 {
    #                     'AttributeName': 'playlist_name',
    #                     'KeyType': 'HASH'
    #                 }
    #             ],
    #             'Projection': {
    #                 'ProjectionType': 'ALL'
    #             },
    #             'ProvisionedThroughput': {
    #                 'ReadCapacityUnits': 1,
    #                 'WriteCapacityUnits': 1
    #             }
    #         }
    #     },
    # ],
        BillingMode='PAY_PER_REQUEST',
    )


def get_music_list():
    return client.scan(
        TableName='music'
    )


def addMusicToPlayList(data):
    response = PlaylistTable.put_item(
        Item={
            'playlist_uuid': str(uuid.uuid4()),
            'music_uuid': data['uuid'],
            'artist_name': data['artist_name'],
            'track_name': data['track_name'],
            'genre': data['genre'],
            'lyrics': data['lyrics'],
            'topic': data['topic'],
            'playlist_name':data['playlist_name'],
            'email': data['email'],
            'name': data['name'],
            'playlist_name': data['playlist_name']
        }
    )
    return response



# def addUserToUserTable(name, email, password):
#     response = UserTable.put_item(
#         Item={
#             'name': name,
#             'email': email,
#             'password': password,
#             'subscribe': 0,
#             'subscription_type': 0
#         }
#     )
#     return response

# def GetUserFromTable(email):
#     response = UserTable.get_item(
#         Key={
#             'email': email
#         },
#         AttributesToGet=[
#             'email', 'name', 'password'
#         ]
#     )
#     return response