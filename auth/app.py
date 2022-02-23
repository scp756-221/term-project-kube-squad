"""
SFU CMPT 756
Sample application---user service.
"""
# # pip install virtualenv (if you don't already have virtualenv installed)
# virtualenv venv to create your new environment (called 'venv' here)
# source venv/bin/activate to enter the virtual environment
# pip install -r requirements.txt

import logging
import sys

import bcrypt
import jwt
# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request
# from prometheus_flask_exporter import PrometheusMetrics
from middleware import handle_all_exceptions

# Standard library modules
import auth_handler as dynamodb

# The application

app = Flask(__name__)

# metrics = PrometheusMetrics(app)
# metrics.info('app_info', 'User process')

bp = Blueprint('app', __name__)


@bp.route('/cuser', methods=['GET'])
@handle_all_exceptions
def create_user_table():
    dynamodb.CreateTableUser()
    return 'User table is now created!'


@bp.route('/register', methods=['POST'])
@handle_all_exceptions
def register_user():
    name = request.json.get('name', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not name or not email or not password:
        return {
                'status': False,
                'message': "Please provide name, email and password"
            }

    user_found_res = dynamodb.GetUserFromTable(email)

    if (user_found_res['ResponseMetadata']['HTTPStatusCode'] == 200):

        if ('Item' in user_found_res):
            return {
                'status': False,
                'message': "Seems you are already registered",
            }

        hashed = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        reg_res = dynamodb.addUserToUserTable(name,
                                              email, hashed)

        if (reg_res['ResponseMetadata']['HTTPStatusCode'] == 200):
            encoded = jwt.encode({'name': name, 'email': email},
                                 'music-app-an2t-secret',
                                 algorithm='HS256')
            return {
                'status': True,
                'message': 'User registered successfully',
                'token': encoded
            }

        return {
            'status': False,
            'message': 'Some error occurred',
        }

    return {
        'status': False,
        'message': 'Some error occurred',
    }


@bp.route('/login', methods=['POST'])
@handle_all_exceptions
def login_user():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email or not password:
        return {
                'status': False,
                'message': "Please provide name, email and password"
            }

    user_found_res = dynamodb.GetUserFromTable(email)

    if (user_found_res['ResponseMetadata']['HTTPStatusCode'] == 200):

        if 'Item' in user_found_res:
            pwd = user_found_res['Item']['password']
            name = user_found_res['Item']['name']
            if bcrypt.checkpw(password.encode('utf8'), pwd.value):
                encoded = jwt.encode({'name': name, 'email': email},
                                     'music-app-an2t-secret',
                                     algorithm='HS256')
                return {
                    'status': True,
                    'message': "User logged in successfully!",
                    'token': encoded
                }
            else:
                return {
                    'status': False,
                    'message': "Wrong credentials entered. Please try again.",
                }

        else:
            return {
                'status': False,
                'message': "User not found. Please sign-up.",
            }
    else:
        return {
            'status': False,
            'message': 'Some error occurred',
        }


@bp.route('/logout', methods=['GET'])
@handle_all_exceptions
def logout_user():
    return {
        'status': True,
        'message': 'User logged out!',
    }

app.register_blueprint(bp, url_prefix='/api/v1/auth/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: app.py <service-port>")
        sys.exit(-1)

    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True, debug=True)
