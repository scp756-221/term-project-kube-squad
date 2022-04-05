"""
SFU CMPT 756
Sample application---user service.
"""
# # pip install virtualenv (if you don't already have virtualenv installed)
# virtualenv venv to create your new environment (called 'venv' here)
# source venv/bin/activate to enter the virtual environment
# pip install -r requirements.txt

import jwt
import sys
import bcrypt
import logging

# Installed packages
from flask import Flask
from flask import request
from flask import Blueprint

from middleware import handle_all_exceptions
# from prometheus_flask_exporter import PrometheusMetrics

# Standard library modules
import sub_handler as dynamodb

# The application

app = Flask(__name__)

# metrics = PrometheusMetrics(app)
# metrics.info('app_info', 'User process')

bp = Blueprint('app', __name__)



@bp.route('/cred', methods=['GET'])
@handle_all_exceptions
def music_credit_cards():
    dynamodb.CreateTableCredit()
    return 'Music credit card table is now created!'



@bp.route('/addcard', methods=['POST'])
# @handle_all_exceptions
def add_card():

    card_no = request.json.get('card_no', None)
    cvv = request.json.get('cvv', None)
    exp_month = request.json.get('exp_month', None)
    exp_year = request.json.get('exp_year', None)


    if not card_no or not cvv or not exp_month or not exp_year:
        return {
                'status': False,
                'message': "Please provide all the required fields card_no, cvv, exp_month, exp_year"
            }

    # hashed_cvv_no = bcrypt.hashpw(str(cvv).encode('utf-8'),bcrypt.gensalt())

    card_found_res = dynamodb.GetCardFromTable(card_no)

    if (card_found_res['ResponseMetadata']['HTTPStatusCode'] == 200):

        if ('Item' in card_found_res):
            return {
                'status': False,
                'message': "Card already exists",
            }

        card_res = dynamodb.Createcard(card_no, cvv, exp_month, exp_year)

        if (card_res['ResponseMetadata']['HTTPStatusCode'] == 200):
            return {
                'status': True,
                'message': 'Card added successfully',
            }

        return {
            'status': False,
            'message': 'Some error occurred',
        }
        return {
            'status': False,
            'message': 'Some error occurred',
        }



@bp.route('/subcribe', methods=['POST'])
def update_subscription():
    email =  request.json.get('email', None)
    subcribe = request.json.get('subscription', None)
    subcribe_type = request.json.get('subscription_type', None)
    card_no = request.json.get('card_no', None)
    cvv = request.json.get('cvv', None)
    exp_month = request.json.get('exp_month', None)
    exp_year = request.json.get('exp_year', None)

    if not subcribe:
        return {
                'status': False,
                'message': "Please provide all subscription field"
            }

    # if subcribe != 1:
    #         return {
    #             'status': True,
    #             'message': "You can subcribe later when you wish"
    #         }

    if not subcribe_type or not email or not card_no or not cvv or not exp_month or not exp_year:
        return {
                'status': False,
                'message': "Please provide all required fields email, subcription_type, card_no, cvv, exp_month, exp_year"
            }

    user_found_res = dynamodb.GetUserFromTable(email)

    if (user_found_res['ResponseMetadata']['HTTPStatusCode'] == 200):
        if 'Item' in user_found_res:

            card_found_res = dynamodb.GetCardFromTable(card_no)

            if (card_found_res['ResponseMetadata']['HTTPStatusCode'] == 200):

                if 'Item' in card_found_res:
                    card_no = card_found_res['Item']['card_no']
                    cvv_fth = card_found_res['Item']['cvv']
                    expiry_mnt = card_found_res['Item']['exp_month']
                    expiry_yr = card_found_res['Item']['exp_year']

                    if str(cvv_fth) == str(cvv) and str(expiry_mnt) == str(exp_month) and str(expiry_yr) == str(exp_year):

                        sub_done = dynamodb.SubcribeUser(email, subcribe, subcribe_type)

                        if (sub_done['ResponseMetadata']['HTTPStatusCode'] == 200):
                            return {
                                'status': True,
                                'message': 'Payment was succesfull and subscription updated successfully',
                            }
                        else:
                            return {
                                'status': False,
                                'message': 'Some error occurred',
                            }
                    else:
                        return {
                            'status': False,
                            'message': 'Card is invalid',
                            }

    return {
        'status': False,
        'message': 'Some errors occured',
    }



app.register_blueprint(bp, url_prefix='/api/v1/subscribe/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: app.py <service-port>")
        sys.exit(-1)

    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True, debug=True)
