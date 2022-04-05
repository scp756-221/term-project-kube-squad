import boto3

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
CardTable = resource.Table('Cards')


def CreateTableCredit():
    client.create_table(AttributeDefinitions=[
        {
            "AttributeName": "card_no",
            "AttributeType": "S"
        }],
        TableName='Cards',
        KeySchema=[
            {
                "AttributeName": "card_no",
                "KeyType": "HASH"
            }
    ],
        BillingMode='PAY_PER_REQUEST',
    )



def Createcard(card_no, cvv, exp_month, exp_year):
    response = CardTable.put_item(
        Item={
            'card_no': card_no,
            'cvv': cvv,
            'exp_month': exp_month,
            'exp_year': exp_year}
    )
    return response



def GetCardFromTable(card_no):
    response = CardTable.get_item(
        Key={
            'card_no': card_no
        },
        AttributesToGet=[
            'card_no', 'cvv', 'exp_month', 'exp_year'
        ]
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



def SubcribeUser(email, sub, sub_type):

    response = UserTable.update_item(
        Key = {
            'email': email
        },
        AttributeUpdates={
            'subscribe': {
                    'Value'  : sub,
                    'Action' : 'PUT'
                },
            'subscription_type': {
                    'Value'  : sub_type,
                    'Action' : 'PUT'
                }
        },
        ReturnValues = "UPDATED_NEW"
    )
    return response
