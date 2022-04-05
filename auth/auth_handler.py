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
UserTable = resource.Table('User')


def CreateTableUser():
    client.create_table(AttributeDefinitions=[
        {
            "AttributeName": "email",
            "AttributeType": "S"
        }],
        TableName='User',
        KeySchema=[
            {
                "AttributeName": "email",
                "KeyType": "HASH"
            }
    ],
        BillingMode='PAY_PER_REQUEST',
    )



def addUserToUserTable(name, email, password):
    response = UserTable.put_item(
        Item={
            'name': name,
            'email': email,
            'password': password,
            'subscribe': 0,
            'subscription_type': 0
        }
    )
    return response

def GetUserFromTable(email):
    response = UserTable.get_item(
        Key={
            'email': email
        },
        AttributesToGet=[
            'email', 'name', 'password'
        ]
    )
    return response
