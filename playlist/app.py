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
from flask import Flask, jsonify
from flask import request
from prometheus_flask_exporter import PrometheusMetrics
from middleware import handle_all_exceptions

# Standard library modules
import playlist_handler as dynamodb

# The application

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'User process')

bp = Blueprint('app', __name__)

subscribe_req_msg = "Please purchase a subscription to use this feature"
song_detail_map = {
    'lyrics': 'lyrics',
    'artist': 'artist_name',
    'genre': 'genre',
    'release-date': 'release_date',
    'topic': 'topic'
}

@bp.route('/cplaylist', methods=['GET'])
def create_user_table():
    dynamodb.CreateTablePlaylist()
    return 'playlist table is now created!'



@bp.route('/getMusicList', methods=['GET'])
@handle_all_exceptions
def get_music_list():
    res = dynamodb.get_music_list()
    return jsonify(res)

@bp.route('/view_playlist_names', methods=['POST'])
def view_playlist_names():
    username = request.json.get('username', None)
    email = request.json.get('email', None)

    playListNames = dynamodb.get_playlist_names(username, email)

    if len(playListNames) > 0:
        return {
            'status': True,
            'message': 'Retrieved Playlists',
            'item':list(playListNames)
        }
    else:
        return {
            'status': False,
            'message': 'You Have No Playlists',
        }

@bp.route('/delete_song_from_playlist', methods=['POST'])
def delete_song_from_playlist():
    songsToDelete = request.json.get('songsToDelete', None)

    for song in songsToDelete:
        response = dynamodb.remove_song_from_playlist(song)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            return {'status': False, 'message': 'Failed to delete'}

    return {'status': True, 'message': 'Deleted'}


@bp.route('/view_playlist', methods=['POST'])
def view_playlist():
    username = request.json.get('username', None)
    email = request.json.get('email', None)
    playlistName = request.json.get('playlistName', None)

    playList = dynamodb.get_playlist(username, email, playlistName)

    if len(playList) > 0:
        return {
            'status': True,
            'message': 'Retrieved Playlists',
            'item':playList
        }
    else:
        return {
            'status': False,
            'message': 'You Have No Playlists',
        }




@bp.route('/addToPlaylist', methods=['POST'])
def add_music_to_playlist():


    uuid = request.json.get('uuid', None)
    artist_name = request.json.get('artist_name', None)
    track_name  = request.json.get('track_name', None)
    genre  = request.json.get('genre', None)
    lyrics  = request.json.get('lyrics', None)
    topic = request.json.get('topic', None)
    email = request.json.get('email', None)
    username = request.json.get('username', None)
    playlist_name = request.json.get('playlist_name', None)
    orderNum = request.json.get('orderNum', None)


    if not uuid or not artist_name or not track_name or not genre or not lyrics or not topic or not email or not username or not playlist_name:
        return {
                'status': False,
                'message': "Please provide uuid, artist_name, track_name, genre, lyrics, topic"
            }

    data = {
        "uuid" : uuid,
        "artist_name" : artist_name,
        "track_name" : track_name,
        "genre" : genre,
        "lyrics" : lyrics,
        "topic" : topic ,
        "email": email,
        "name" : username,
        "playlist_name": playlist_name,
        "orderNum": orderNum
    }


    reg_res = dynamodb.addMusicToPlayList(data)        

    if (reg_res['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
                'status': True,
                'message': 'Music track added to playlist successfully',
            }
    else: 
        return {
            'status': True,
            'message': "Somthing went wrong!"
        }

"""
PREMIUM MUSIC SERVICES
1. Song Lyrics
2. Artist Name
3. Song Genre
4. Song Release Date
5. Song Topic
"""

@bp.route('<song_id>/<detail_type>', methods=['GET'])
@handle_all_exceptions
def get_music_detail(song_id, detail_type):
    response = {}
    resp_code = 200
    if dynamodb.checkUserIsSubscribed(request.json.get('email', None)):    
        res = dynamodb.getSongDetail(song_id, song_detail_map[detail_type])
        if res == "":
            resp_code = 404
        response['message'] = res
    else:
        resp_code = 403
        response['message'] = subscribe_req_msg
    return jsonify(response), resp_code        

app.register_blueprint(bp, url_prefix='/api/v1/music/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: app.py <service-port>")
        sys.exit(-1)

    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True, debug=True)
