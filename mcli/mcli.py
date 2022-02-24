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
        'port2',
        type=int,
        help="Port number of music server"
        )
    return argp.parse_args()


def get_url(name, port):
    return "http://{}:{}/api/v1/music/".format(name, port)

def get_auth_url(name, port):
    return "http://{}:{}/api/v1/auth/".format(name, port)

def get_auth_url_hard(name, port):
    return "http://0.0.0.0:3000/api/v1/auth/".format(name, port)


def get_music_url(name, port):
    return "http://{}:{}/api/v1/music/".format(name, port)    

def get_music_url_hard(name, port):
    return "http://0.0.0.0:5000/api/v1/music/"


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


class Auth(cmd.Cmd):
    def __init__(self, args):
        self.name = args.name
        self.port = args.port
        cmd.Cmd.__init__(self)
        self.prompt = 'mql: '
        self.intro = ""

    def do_register(self, arg):
        """
        """
        name = utils.validate_name()
        email = utils.validate_email()
        passw, passw2 = utils.validate_pwd_and_c_pwd()

        # For test
        # print({
        #     "name": name,
        #     "email": email,
        #     "password": passw,
        # })
        url = get_auth_url_hard(self.name, self.port)
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
            f = open("local-storage.txt", 'w+')
            f.write(token)
            f.close()
            print("\n")
            name, email = utils.decode_jwt(res['token'])
            print("\n")
            print(
                f"Welcome {name}. Please run 'help' to see options related to music app.")
            Mcli(args).cmdloop()
        # print(r.json())

    def do_login(self, arg):
        """
        """
        email = utils.validate_email()
        passw = utils.validate_pwd()


        # For test
        url = get_auth_url_hard(self.name, self.port)
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
        # print(res)



class Mcli(cmd.Cmd):
    def __init__(self, args):
        self.name = args.name
        self.port = args.port
        self.port2 = args.port2
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
        url = get_music_url_hard(self.name, self.port2)

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
            url = get_music_url_hard(self.name,self.port2)
            done_message = utils.add_song_by_song_id(playlist_name, song_list, url)
            print(done_message)

        else:
            print("You entered No - not creating a new plalist")
            is_yes_or_no = utils.ask_to_view_existing_playlist()

            if is_yes_or_no:
                print("\nYou should now see the playlist here: ")
                print("functionailty not added: ")
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

        url = get_auth_url(self.name, self.port2)
        payload = {
            "email": email,
            "subcription": subcribe,
            "subcription_type": sub_type,
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
        print(res)
        if res['status']:
            print("*** Payment sucessfull and subcribed***")
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

        url = get_auth_url(self.name, self.port2)
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
