# CMPT 756 User service

The user service maintains a list of users and passwords.  In a more complete version of the application, users would have to first log in to this service, authenticate with a password, be assigned a session, then present that session token to the music service for any requests.

## Installation

See Repository README for deployment instructions

## APIs

1. Create table user

```bash
Method type: GET
http://127.0.0.1:5000/api/v1/auth/cuser
```

2. user login

```bash
Method type: POST
http://<CLUSTER_INGRESS_IP_ADDRESS>/api/v1/auth/login

Body: 

{
    "password": "123123123",
    "name": "aa",
    "email": "bbb@g.com"
}

Success Response:

{
    "message": "User logged in successfully!",
    "status": true,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiYWEiLCJlbWFpbCI6ImJiYkBnLmNvbSJ9.vBJ3i_rMvjGq_nENVJyQQWdkQgfQQwiPMCmAxoCQOkk"
}
```

2. user register

```bash
Method type: POST
http://<CLUSTER_INGRESS_IP_ADDRESS>/api/v1/auth/register

Body: 

{
    "name": "aa",
    "email": "bbb@g.com",
    "password": "123123123"
}

Success Response: 

{
    "message": "User registered successfully",
    "status": true
}
```
Password will be encrypted before getting added to the table.


### References

##### ref: https://medium.com/featurepreneur/crud-operations-on-dynamodb-with-flask-apis-916f6cae992
##### ref: https://hackernoon.com/using-aws-dynamodb-with-flask-9086c541e001




