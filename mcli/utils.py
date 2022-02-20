import re
import getpass

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