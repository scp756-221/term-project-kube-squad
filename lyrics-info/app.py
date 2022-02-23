"""
SFU CMPT 756
Sample application---lyrics info service.
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
from flask import Flask, jsonify
from flask import request
from prometheus_flask_exporter import PrometheusMetrics
from middleware import handle_all_exceptions

# Standard library modules
import lyrics_handler as dynamodb

# The application

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Lyrics info process')

bp = Blueprint('app', __name__)

@bp.route('/lyricsinfo/create', methods=['GET'])
def create_user_table():
    dynamodb.create_table_lyrics_info()
    return 'lyrics info table is now created!'

@bp.route('/lyricsinfo/populate', methods=['GET'])
def populate_table():
    dynamodb.populate_lyrics_info_table()
    return 'lyrics info table is now populated!'

@bp.route('/<music_id>', methods=['GET'])
@handle_all_exceptions
def get_lyrics_info(music_id):
    res = dynamodb.get_lyrics_info(music_id)
    return jsonify(res)

app.register_blueprint(bp, url_prefix='/api/v1/music/info/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: app.py <service-port>")
        sys.exit(-1)

    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True, debug=True)