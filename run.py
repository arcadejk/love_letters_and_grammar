import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_letters and grammar')

def get_username():
    """
    User may enter their username. 
    the function will return the entered username.
    """
    username = input("Please enter your username: ")
    return username

user_name = get_username()
print(f"Hello, {user_name}! Welcome to this challenge.")
print("You are about to start a game of 3 steps.")
print("Soon you will start the Hangman game to guess the right word.")

