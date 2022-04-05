"""
Simple command-line interface to music service
"""

# Standard library modules
import argparse
import cmd
import re
import jwt

# Installed packages
import requests
import utils
import os.path
from os import path


# The services check only that we pass an authorization,
# not whether it's valid
DEFAULT_AUTH = 'Bearer A'


def parse_args():
    argp = argparse.ArgumentParser(
        'mcli',
        description='Command-line query interface to music service'
        )
    argp.add_argument(
        'name',
        help="DNS name or IP address of music server"
        )
    argp.add_argument(
        'port',
        type=int,
        help="Port number of music server"
        )
    argp.add_argument(
        'dpl_type',
        help="Deployment Type of music server"
    )
    return argp.parse_args()

def get_auth_url(name='localhost', port=80, deploymentType='k8s'):
    if deploymentType == 'k8s':
        return "http://{}:{}/api/v1/auth/".format(name, port)
    else:
        return "http://auth:3000/api/v1/auth/"

def get_subscription_url(name='localhost', port=80, deploymentType='k8s'):
    if deploymentType == 'k8s':
        return "http://{}:{}/api/v1/subscribe/".format(name, port)
    else:
        return "http://subscription:4000/api/v1/subscribe/"

def get_music_url(name='localhost', port=80, deploymentType='k8s'):
    if deploymentType == 'k8s':
        return "http://{}:{}/api/v1/music/".format(name, port)
    else:
        return "http://playlist:6000/api/v1/music/"


def parse_quoted_strings(arg):
    """
    Parse a line that includes words and '-, and "-quoted strings.
    This is a simple parser that can be easily thrown off by odd
    arguments, such as entries with mismatched quotes.  It's good
    enough for simple use, parsing "-quoted names with apostrophes.
    """
    mre = re.compile(r'''(\w+)|'([^']*)'|"([^"]*)"''')
    args = mre.findall(arg)
    return [''.join(a) for a in args]

def view_song_info(url, info_type):
    """
    CLI option to view song info. 
    """
    song_id = utils.validate_song_id()
    with open("local-storage.txt", "r") as file:
        token = file.readline()
    name, email = utils.decode_jwt(token)
    payload = {
        "email": email
    }      
    url = url+str(song_id)+"/"+info_type
    r = requests.get(url,            
        json=payload,
        headers={
            'Content-Type': 'application/json'
        })
    res = r.json()
    print(f"*** {res['message']} ***")

class Auth(cmd.Cmd):
    def __init__(self, args):
        self.name = args.name
        self.port = args.port
        self.dpl_type = args.dpl_type
        cmd.Cmd.__init__(self)
        self.prompt = 'mql: '
        self.intro = ""

    def do_register(self, arg):
        """
        """
        name = utils.validate_name()
        email = utils.validate_email()
        passw, passw2 = utils.validate_pwd_and_c_pwd()

        url = get_auth_url(self.name, self.port, self.dpl_type)

        payload = {
            "name": name,
            "email": email,
            "password": passw,
        }
        r = requests.post(
            f"{url}register",
            json=payload,
            headers={
                'Content-Type': 'application/json'
            }
        )
        res = r.json()

        print("\n")
        print(res['message'])
        if res['status']:
            if 'token' in res:
                token = res['token']
                f = open("local-storage.txt", 'w+')
                f.write(token)
                f.close()
                print("\n")
                name, email = utils.decode_jwt(res['token'])
                print("\n")
                print(f"Welcome {name}. Please run 'help' to see options related to music app.")
                Mcli(args).cmdloop()
        # print(r.json())

    def do_login(self, arg):
        """
        """
        email = utils.validate_email()
        passw = utils.validate_pwd()

        # For test
        url = get_auth_url(self.name, self.port, self.dpl_type)

        payload = {
            'email': email,
            'password': passw,
        }

        r = requests.post(
            f"{url}login",
            json=payload,
            headers={
                'Content-Type': 'application/json'
            }
        )
        res = r.json()
        print("\n")
        print(res['message'])

        if 'token' in res:
            token = res['token']
            if res['status']:
                f = open("local-storage.txt", 'w+')
                f.write(token)
                f.close()
                print("\n")
                name, email = utils.decode_jwt(token)
                print("\n")
                print(f"Welcome {name}. Please run 'help' to see options related to music app.")
                Mcli(args).cmdloop()



class Mcli(cmd.Cmd):
    def __init__(self, args):
        self.name = args.name
        self.port = args.port
        self.dpl_type = args.dpl_type
        cmd.Cmd.__init__(self)
        self.prompt = 'mql: '
        self.intro = """
                        Command-line interface to music service.
                        Enter 'help' for command list.
                        'Tab' character autocompletes commands.
                     """

    def show_music_list(self):
        """
        """
        url = get_music_url(self.name, self.port, self.dpl_type)

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

    def do_add_music_to_playlist(self, arg):
        """
        """
        is_yes_or_no = utils.ask_to_add_m_to_playlist()

        if is_yes_or_no:
            print("You entered Yes")
            playlist_name = utils.validate_playlist_name(type='your')
            print("Select songs from below or press Q to end")
            song_list = self.show_music_list()
            url = get_music_url(self.name,self.port, self.dpl_type)
            orderNum = 0
            done_message = utils.add_song_by_song_id(playlist_name, song_list, url, orderNum)

        else:
            print("You entered No - not creating a new playlist")
            viewPlaylist = utils.ask_to_view_existing_playlist()

            if viewPlaylist:
                url = get_music_url(self.name, self.port, self.dpl_type)

                res, playlistNames = utils.view_playlist_names(url)

                # Keep going if we have at least one playlist
                if res:

                    # Getting the playlist name
                    playlist_name = utils.validate_current_playlist_name(playlistNames, type='your')

                    # Priting the playlist to terminal
                    getPlaylist, playlist = utils.view_playlist(playlist_name, url)

                    # If there was an error, back out
                    if not getPlaylist:
                        print("\nError - exiting the playlist microservice ")
                        return ''

                    # Asking if use wants to edit playlist
                    is_yes_or_no = utils.ask_to_edit_existing_playlist()

                    # If yes, continue
                    if is_yes_or_no:
                        utils.edit_existing_playlist(playlist_name, url)
                    else:
                        print("\nYou entered N - exiting the playlist microservice ")
                else:
                    print("\nPlease create a playlist first")

            else:
                print("\nYou entered N - exiting the playlist microservice ")



    def do_subcribe(self, arg):
        """
        """
        subcribe = utils.validate_subcription()
        sub_type = utils.validate_type()
        card_no = utils.validate_card()
        cvv = utils.validate_cvv()
        exp_year = utils.validate_year()
        exp_month = utils.validate_month(exp_year)

        with open("local-storage.txt", "r") as file:
            token = file.readline()

        name, email = utils.decode_jwt(token)

        url = get_subscription_url(self.name, self.port, self.dpl_type)

        payload = {
            "email": email,
            "subscription": subcribe,
            "subscription_type": sub_type,
            "card_no": card_no,
            "cvv": cvv,
            "exp_month": exp_month,
            "exp_year": exp_year
        } 
        r = requests.post(
            f"{url}subcribe",
            json=payload,
            headers={
                'Content-Type': 'application/json'
            }
        )
        res = r.json()

        if res['status']:
            print("*** Payment successful and subscribed***")
        else:
           print(f"*** {res['message']} ***")


    def do_add_card(self, arg):
        """
        """
        card_no = utils.validate_card()
        cvv = utils.validate_cvv()
        exp_year = utils.validate_year()
        exp_month = utils.validate_month(exp_year)

        with open("local-storage.txt", "r") as file:
            token = file.readline()

        name, email = utils.decode_jwt(token)

        url = get_subscription_url(self.name, self.port, self.dpl_type)
        payload = {
            "card_no": card_no,
            "cvv": cvv,
            "exp_month": exp_month,
            "exp_year": exp_year
        } 
        r = requests.post(
            f"{url}addcard",
            json=payload,
            headers={
                'Content-Type': 'application/json'
            }
        )
        res = r.json()
        if res['status']:
            print(f"*** {res['message']} ***")
        else:
            print(f"*** {res['message']} ***")

    def do_view_song_lyrics(self, arg):
        """
        CLI option to view lyrics.
        """
        view_song_info(get_music_url(self.name, self.port, self.dpl_type),'lyrics')

    def do_find_artist(self, arg):
        """
        CLI option to view artist name
        """
        view_song_info(get_music_url(self.name,self.port, self.dpl_type),'artist')

    def do_view_song_genre(self, arg):
        """
        CLI option to view song genre
        """
        view_song_info(get_music_url(self.name,self.port, self.dpl_type),'genre')

    def do_get_song_release_date(self, arg):
        """
        CLI option to get song release date
        """
        view_song_info(get_music_url(self.name,self.port, self.dpl_type),'release-date')

    def do_find_song_topic(self, arg):
        """
        CLI option to find song topic
        """
        view_song_info(get_music_url(self.name, self.port, self.dpl_type),'topic')

    def do_logout(self, arg):
        """
        """
        f = open("local-storage.txt", 'w+')
        f.write("")
        f.close()

        print("\n")
        print(
            f"See you!. Please run 'help' to see login and register options.")
        print("\n")
        Auth(args).cmdloop()


if __name__ == '__main__':
    args = parse_args()
    token = ''

    if not path.exists("local-storage.txt"):
        f = open("local-storage.txt", "w+")
        
    f = open("local-storage.txt", "r")
    token = f.read()

    if token != '':
        Mcli(args).cmdloop()
    else:
        Auth(args).cmdloop()
