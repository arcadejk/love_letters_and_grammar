import sys
import random
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

def choose_to_continue(user_name):
    """
    Create loop to ask and return user choice,
    if he wants or not to start the game.
    """
    while True:
        choice = input("Would you like to enter your username? (y/n): ").lower()
        if choice == 'y':
            print(f"Let's start, {user_name}!")
            return True
        elif choice == 'n':
            print("No problem, you can come back anytime.")
            sys.exit()
        else:
            print("Invalid choice. Please enter 'y' for yes or 'n' for no.")

def choose_category():
    """
    User choose an option to start playing
    """
    print("Choose a category:")
    print("1. Politics")
    print("2. Society")
    print("3. Hobbies")
    
    while True:
        choice = input("Enter the number of your choice (1/2/3): ")
        if choice in ['1', '2', '3']:
            if choice == '1':
                return "Politics"
            elif choice == '2':
                return "Society"
            elif choice == '3':
                return "Hobbies"
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def get_random_word(categories):
    """
    Access the worksheet based on the selected category.
    Get all values in the worksheet and choose a random cell.
    """
    categories = SHEET.worksheet("categories")
    words_list = categories.col_values(2)
    return random.choice(words_list)

def main():
    """
    Run all program functions
    """
    user_name = get_username()
    print(f"Hello, {user_name}! Welcome to this challenge.")
    print("You are about to start a game of 3 steps.")
    print("Soon you will start the Hangman game to guess the right word.")

    if choose_to_continue(user_name):
        selected_category = choose_category()
        print("Selected category:", selected_category)
        random_word = get_random_word(selected_category)
        print(f"The word to guess is: {random_word}")

print("Welcome to the letters and Grammar game!")
main()