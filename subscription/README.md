# CMPT 756 User service

The user service maintains a list of users and passwords.  In a more complete version of the application, users would have to first log in to this service, authenticate with a password, be assigned a session, then present that session token to the music service for any requests.

## Installation

See Repository README for deployment instructions

## APIs

1. Add Credit Card

```bash
Method type: POST
http://<CLUSTER_INGRESS_IP_ADDRESS>/api/v1/subscribe/addcard

Body: 

{
    "card_no": "123123123",
    "cvv": "132",
    "exp_month": "10",
    "exp_year": "2022"
}

Success Response:

{
    'status': True,
    'message': 'Card added successfully',
}
```

2. Add Subscription

```bash
Method type: POST
http://<CLUSTER_INGRESS_IP_ADDRESS>/api/v1/subscribe/subcribe

Body: 

{
    "email": "test@sfu.ca",
    "subscription": "True",
    "subscription_type": "1",
    "card_no": "123123123",
    "cvv": "132",
    "exp_month": "10",
    "exp_year": "2022"
}

Success Response:

{
    'status': True,
    'message': 'Payment was succesfull and subscription updated successfully',
}
```



### References

##### ref: https://medium.com/featurepreneur/crud-operations-on-dynamodb-with-flask-apis-916f6cae992
##### ref: https://hackernoon.com/using-aws-dynamodb-with-flask-9086c541e001




