# CMPT 756 User service

The user service maintains a list of users and passwords.  In a more complete version of the application, users would have to first log in to this service, authenticate with a password, be assigned a session, then present that session token to the music service for any requests.

## Installation

See Repository README for deployment instructions

## APIs

1. Get Songs

```bash
Method type: GET
http://<CLUSTER_INGRESS_IP_ADDRESS>/api/v1/music/getMusicList

Body:
{
  "Count": 100,
  "Items": [{
      "artist_name": {
        "S": "t. m. soundararajan"
      },
      "genre": {
        "S": "pop"
      },
      "lyrics": {
        "S": "watch world surround inside phone booth begin astound try couth say sunday cause rybody tellin truth monday yeah monday cause rybody drinkin vermouth lend hand kiss stand give away free acid joke smoke barely drive dusk headlights headphones tomorrow plan shop spree love hard like billboard grin toast life beauty head begin spin press cheek rainwashed streets weep reincarnation come december thirtyfirst worst time year think people like share beer have january explanations appear"
      },
      "release_date": {
        "S": "1953"
      },
      "topic": {
        "S": "world/life"
      },
      "track_name": {
        "S": "ethanai periya"
      },
      "uuid": {
        "S": "99"
      }},...,
      {
      "artist_name": {
        "S": "a. m. rajah"
      },
      "genre": {
        "S": "pop"
      },
      "lyrics": {
        "S": "deal pharmaceuticals sell pills yesterday sister call tell kill respectable doctor hill shoot heart feel thing poor deal pharmaceuticals sell expensive drug give money hell think medicine prescription fill come goodbye sorry die come finish pay come finish pay come finish pay come finish pay deal pharmaceuticals sell pills yesterday sister call tell kill medicine prescription fill come goodbye sorry die come finish pay come finish pay come finish pay come finish pay"
      },
      "release_date": {
        "S": "1954"
      },
      "topic": {
        "S": "obscene"
      },
      "track_name": {
        "S": "gopiparivrito"
      },
      "uuid": {
        "S": "138"
      }}]
  "ScannedCount": 100
}
```

2. Get Playlists

```bash
Method type: POST
http://<CLUSTER_INGRESS_IP_ADDRESS>/api/v1/music/view_playlist_names

Body: 

{
    "username": "aa",
    "email": "bbb@g.com"
}

Success Response:

{
    'status': True,
    'message': 'Retrieved Playlists',
    'item':list(playListNames)
}
```

3. Delete Songs From Paylist

```bash
Method type: POST
http://<CLUSTER_INGRESS_IP_ADDRESS>/api/v1/music/delete_song_from_playlist

Body: 

{
    "songsToDelete": [1,2,3,4,...,10],
}

Success Response: 

{
    'status': True, 'message': 'Deleted'
}
```

4. View Playlist

```bash
Method type: POST
http://<CLUSTER_INGRESS_IP_ADDRESS>/api/v1/music/view_playlist

Body: 

{
    "username": "aa",
    "email": "bbb@g.com",
    "playlistName": "test"
}

Success Response: 

{
    'status': True,
    'message': 'Retrieved Playlists',
    'item':playList
}
```

5. Add To Playlist

```bash
Method type: POST
http://<CLUSTER_INGRESS_IP_ADDRESS>/api/v1/music/addToPlaylist

Body: 

{
    "uuid": "124",
    "artist_name": "artist_name",
    "track_name": "track_name",
    "genre": "genre",
    "lyrics": "lyrics",
    "topic": "topic",
    "username": "aa",
    "email": "bbb@g.com",
    "playlistName": "test",
    "orderNum": 1
}

Success Response: 

{
    'status': True,
    'message': 'Music track added to playlist successfully',
}

```

### Premium song info APIs

1. Song Lyrics
2. Artist name
3. Genre
4. Topic
5. Release date

```bash
Method type: GET
http://<CLUSTER_INGRESS_IP_ADDRESS>/api/v1/music/<music_id>/<detail_type>

Url parameters:
<music_id> - must be a positive integer
<detail_type> - one of 'lyrics','artist','genre','pop','release-date' (currently MCLI options use only 'lyrics' and 'artist')

If user has an active subscription:
Success response:

{
    "message": "song info here"
}

If song does not exist:

{
    "message": ""
}

If user is not subscribed:

{
    "message": "Please purchase a subscription to use this feature"
}

```

### References

##### ref: https://medium.com/featurepreneur/crud-operations-on-dynamodb-with-flask-apis-916f6cae992
##### ref: https://hackernoon.com/using-aws-dynamodb-with-flask-9086c541e001




