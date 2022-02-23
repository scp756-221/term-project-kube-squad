import re
import jwt
import getpass
from datetime import date


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
    print("*** Press 1 for subcription or any other character to cancel ***")
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
    y_and_n = input("Do you want to create a new playlist. Press Y or N\n ")

    if y_and_n.lower() == 'y' or y_and_n.lower() == 'yes':
        return True
    elif y_and_n.lower() == 'n' or y_and_n.lower() == 'no':        
        return False
    else: 
        print("Please enter valid input")        
        ask_to_add_m_to_playlist()


def validate_playlist_name(type='your'):
    print("*** Set Name ***")
    name = input(f"Please enter {type} playlist name: ")
    if name == '':
        print("\n")
        print("Playlist name cannot be empty.")
        name = validate_name('valid')
    return name

def validate_song_id():
    print("*** Set Name ***")
    id = input(f"enter song id or press q to end: ")
    regex = '^[0-9]+$'
    if not re.fullmatch(regex, id):
        print("\n")
        id = validate_song_id()
    return id