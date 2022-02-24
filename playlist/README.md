# CMPT 756 User service

The user service maintains a list of users and passwords.  In a more complete version of the application, users would have to first log in to this service, authenticate with a password, be assigned a session, then present that session token to the music service for any requests.

## Installation

```bash
pip install virtualenv (if you don't already have virtualenv installed)
virtualenv venv to create your new environment (called 'venv' here)
source venv/bin/activate to enter the virtual environment
pip install -r requirements.txt
```

## APIs

1. Create table user

```bash
Method type: GET
http://127.0.0.1:5000/api/v1/auth/cuser
```

2. user login

```bash
Method type: POST
http://127.0.0.1:5000/api/v1/auth/login

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
http://127.0.0.1:5000/api/v1/auth/register

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

### Premium song info APIs

1. Song Lyrics

```bash
Method type: GET
http://127.0.0.1:5000/api/v1/music/<music_id>/lyrics

Success response:

{
    "message": "song lyrics will be here"
}

If song does not exist:

{
    "message": ""
}

Enhancements to follow: 
1. check whether user has an active subscription before retrieving the lyrics
2. add lyrics option to MCLI
```

### References

##### ref: https://medium.com/featurepreneur/crud-operations-on-dynamodb-with-flask-apis-916f6cae992
##### ref: https://hackernoon.com/using-aws-dynamodb-with-flask-9086c541e001




