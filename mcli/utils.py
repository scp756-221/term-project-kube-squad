import re
import jwt
import getpass
from datetime import date
import requests



def validate_name(type='your'):
    print("*** Set Name ***")
    name = input(f"Please enter {type} name: ")
    if name == '':
        print("\n")
        print("Name cannot be empty.")
        name = validate_name('valid')
    return name


def validate_email(type='your'):
    print("*** Set Email ***")
    email = input(f"Please enter {type} email: ")
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, email):
        print("\n")
        email = validate_email('valid')
    return email


def validate_pwd_and_c_pwd(type='your'):
    print("*** Set Password ***")
    passw = getpass.getpass(f"Please enter {type} password: ")
    passw2 = getpass.getpass("Please enter your confirm password: ")

    if passw == '':
        print("\n")
        print("Password cannot be empty.")
        passw, passw2 = validate_pwd_and_c_pwd('valid')

    if passw2 == '':
        print("\n")
        print("Confirm password cannot be empty.")
        passw, passw2 = validate_pwd_and_c_pwd('valid')

    if passw != passw2:
        print("\n")
        print("Password and confirm password are not matching.")
        passw, passw2 = validate_pwd_and_c_pwd('valid')
    return passw, passw2

def validate_pwd(type='your'):
    print("*** Set Password ***")
    passw = getpass.getpass(f"Please enter {type} password: ")

    if passw == '':
        print("\n")
        print("Password cannot be empty.")
        passw, passw2 = validate_pwd('valid')
    return passw

def decode_jwt(token=''):
    decoded = jwt.decode(token, options={"verify_signature": False})
    return decoded['name'], decoded['email']


def validate_subcription(type='your'):
    print("*** Press 1 for subscription or any other character to cancel ***")
    subcription = input(f"Please enter {type} choice: ")

    if subcription == '':
        print("\n")
        print("Choice cannot be empty, either 1 or any other character or number.")
        subcription = validate_subcription('valid')
    return subcription


def validate_type(type='your'):
    print("\n")
    print("*** There are 3 options ***")
    print("*** 1 Monthly  $10      ***")
    print("*** 2 6 Months $25      ***")
    print("*** 3 Yearly   $40      ***")
    subcription_type = input(f"Please enter {type} choice: ")

    try:
        subcription_type = int(subcription_type)
    except:
        print("\n")
        subcription_type = validate_type('valid')
 
    if subcription_type not in (1,2,3):
        print("\n")
        print("Choice cannot be empty, either 1 2 or 3")
        subcription_type = validate_type('valid')
    return subcription_type


def validate_card(type='your'):
    print("\n")
    card_no = input(f"Please enter {type} card number: ")

    if str(card_no).isdecimal() and len(card_no) == 9:
        return card_no
    else:
        card_no = validate_card('valid')


def validate_cvv(type='your'):
    print("\n")
    cvv_no = input(f"Please enter {type} cvv number: ")

    if str(cvv_no).isdecimal() and len(cvv_no) == 3:
        return cvv_no
    else:
        cvv_no = validate_cvv('valid')


def validate_year(type='your'):

    todays_date = date.today()

    print("\n")
    year = input(f"Please enter {type} expiry year of the card: ")
    try:
        year = int(year)
    except:
        year = validate_year('valid')

    if year >= todays_date.year:
        return year
    else:
        year = validate_year('valid')


def validate_month(year, type='your'):

    todays_date = date.today()

    print("\n")
    month = input(f"Please enter {type} expiry month of the card: ")

    try:
        month = int(month)
    except:
        month = validate_month(year, 'valid')

    if year == todays_date.year and month > 0 and month < 13:
        if month >= todays_date.month:
            return month
        else:
            month = validate_month(year, 'valid')

    if month > 0 and month < 13:
        return month
    else:
        month = validate_month(year, 'valid')



def ask_to_add_m_to_playlist():
    print("\n")
    y_and_n = input("Do you want to create a new playlist. Press Y or N\n[Y|N]:  ")

    if y_and_n.lower() == 'y' or y_and_n.lower() == 'yes':
        return True
    elif y_and_n.lower() == 'n' or y_and_n.lower() == 'no':        
        return False
    else: 
        print("Please enter valid input")        
        ask_to_add_m_to_playlist()


def ask_to_view_existing_playlist():
    print("\n")
    y_and_n = input("Enter Y to view existing playlist or N to exit playlist microservice\n[Y|N]:  ")

    if y_and_n.lower() == 'y' or y_and_n.lower() == 'yes':
        return True
    elif y_and_n.lower() == 'n' or y_and_n.lower() == 'no':
        return False
    else:
        print("Please enter valid input")
        ask_to_view_existing_playlist()

def ask_to_edit_existing_playlist():
    print("\n")
    y_and_n = input("Enter Y to edit the playlist or N to exit playlist microservice\n[Y|N]:  ")

    if y_and_n.lower() == 'y' or y_and_n.lower() == 'yes':
        return True
    elif y_and_n.lower() == 'n' or y_and_n.lower() == 'no':
        return False
    else:
        print("Please enter valid input")
        ask_to_view_existing_playlist()

def get_song_number(songNumbers, type="valid "):
    songNumber = input(f"Please enter {type}\"Song Number\" to remove it from the playlist or press Q to exit: ")
    regex = '^[0-9]+$'
    if songNumber.lower() == 'q':
        return False
    elif (not re.fullmatch(regex, songNumber)) and (int(songNumber) not in songNumbers):
        print("\n")
        print("Invalid input")
        songNumber = get_song_number(songNumbers)
    return songNumber

def delete_playlist_songs(playlist_name, url):
    status, playList = view_playlist(playlist_name, url)
    if status:
        songNumbers = [song['orderNum'] for song in playList]
        songNumber = get_song_number(songNumbers, type="")

        # If do not want to delete song from playlist
        if not songNumber:
            return False
        else:
            songsToDelete = [song for song in playList if song['orderNum'] == int(songNumber)]

            payload = {'songsToDelete': songsToDelete}

            r = requests.post(
                f"{url}delete_song_from_playlist",
                json=payload,
                headers={
                    'Content-Type': 'application/json'
                }
            )
            # print(r.content)
            res = r.json()
            if res['status']:
                print('Song removed from playlist')
                delete_playlist_songs(playlist_name, url)
            else:
                print('Error')
                return False
    else:
        return ''


def show_music_list(url):
    url = f"{url}getMusicList"

    r = requests.get(
        url,
        headers={
            'Content-Type': 'application/json'
        }
    )
    res = r.json()
    song_list = []
    print("uuid track_name genre")
    for _item in res['Items']:
        uuid = _item['uuid']['S']
        track_name = _item['track_name']['S']
        genre = _item['genre']['S']

        song_list.append({
            "uuid": _item['uuid']['S'],
            "artist_name": _item['artist_name']['S'],
            "track_name": _item['track_name']['S'],
            "release_date": _item['release_date']['S'],
            "genre": _item['genre']['S'],
            "lyrics": _item['lyrics']['S'],
            "topic": _item['topic']['S']
        })
        print(f"{uuid} {track_name} {genre}")
    return song_list

def add_to_playlist(playlist_name, url):
    # Printing the music list to the screen
    song_list = show_music_list(url)

    # Extracting the songs currently in the playlist
    status, playList = view_playlist(playlist_name, url, False)

    songNumbers = [song['orderNum'] for song in playList]
    if len(songNumbers) == 0:
        maxSongNumber = 0
    else:
        maxSongNumber = max(songNumbers) + 1
    done_message = add_song_by_song_id(playlist_name, song_list, url, maxSongNumber)
    print(done_message)


def edit_existing_playlist(playlist_name, url):
    while True:
        addTo, DeleteFrom = ask_to_addto_deletefrom_playlist()
        if addTo and not DeleteFrom:
            add_to_playlist(playlist_name, url)
        elif not addTo and DeleteFrom:
            status = delete_playlist_songs(playlist_name, url)
        else:
            print("\nYou entered N - exiting the playlist microservice ")
            return ''

def ask_to_addto_deletefrom_playlist():
    print("\n")
    y_and_n = input("Enter A to add songs, D to delete songs or N to exit playlist microservice\n[A|D|N]:  ")

    if y_and_n.lower() == 'a':
        return True, False
    elif y_and_n.lower() == 'd':
        return False, True
    elif y_and_n.lower() == 'n' or y_and_n.lower() == 'no':
        return False, False
    else:
        print("Please enter valid input")
        ask_to_view_existing_playlist()


def validate_playlist_name(type='your'):
    name = input(f"Please enter {type} playlist name: ")
    if name == '':
        print("\n")
        print("Playlist name cannot be empty.")
        name = validate_name('valid')
    return name

def validate_current_playlist_name(playlists, type='your'):
    name = input(f"Please enter {type} playlist name: ")
    if name == '':
        print("\n")
        print("Playlist name cannot be empty.")
        name = validate_name(playlists, 'valid')
    elif name not in playlists:
        print("\n")
        print("Playlist name cannot not exist.")
        name = validate_current_playlist_name(playlists, 'valid')
    return name

def validate_song_id():
    id = input(f"enter song id or press q to end: ")
    regex = '^[0-9]+$'

    if id.lower() == 'q':
        return id
    elif (not re.fullmatch(regex, id)):
        print("\n")
        print("Invalid input")
        id = validate_song_id()
    return id

def view_playlist_names(url):
    f = open("local-storage.txt", "r")
    token = f.read()
    name, email = decode_jwt(str(token))
    payload = {}
    payload['username'] = name
    payload['email'] = email

    r = requests.post(
        f"{url}view_playlist_names",
        json=payload,
        headers={
            'Content-Type': 'application/json'
        }
    )
    res = r.json()
    if res['status']:
        print('Your Current Playlists:')
        for playlistName in res['item']:
            print(f"- {playlistName}")

        return True, res['item']
    else:
        print(res['message'])
        return False, []

def view_playlist(playlistName, url, printPlayListSongs=True):
    f = open("local-storage.txt", "r")
    token = f.read()
    name, email = decode_jwt(str(token))

    payload = {}
    payload['username'] = name
    payload['email'] = email
    payload['playlistName'] = playlistName

    r = requests.post(
        f"{url}view_playlist",
        json=payload,
        headers={
            'Content-Type': 'application/json'
        }
    )
    res = r.json()
    if res['status']:
        if printPlayListSongs:
            print('Playlist Songs:')
            for song in res['item']['Items']:
                print(f"Song Number: {song['orderNum']} - Song: {song['track_name']} - Artist: {song['artist_name']}")
        return True, res['item']['Items']
    else:
        print('Playlist Empty')
        return False, []



def add_song_by_song_id(playlist_name, song_list, url, orderNum=0):
    id = validate_song_id()

    if id == 'q':
        return 'All songs added to playlist.'

    filtered_song = filter(lambda s: s['uuid'] == id, song_list)

    songs = list(filtered_song)

    if len(songs) > 0:

        f = open("local-storage.txt", "r")
        token = f.read()
        name, email = decode_jwt(str(token))
        
        payload = songs[0]
        payload['username'] = name
        payload['email'] = email
        payload['playlist_name'] = playlist_name
        payload['orderNum'] = orderNum

        # call api to add song to the playlist
        r = requests.post(
            f"{url}addToPlaylist",
            json=payload,
            headers={
                'Content-Type': 'application/json'
            }
        )

        res = r.json()
        print(f"*** {res['message']} ***")    

        if id.lower() != 'q':
            add_song_by_song_id(playlist_name, song_list, url, orderNum+1)
        else:     
            return 'All songs added to playlist.'
