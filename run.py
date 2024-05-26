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
    username = input("Please enter your username: \n")
    return username

def choose_to_continue(user_name):
    """
    Create loop to ask and return user choice,
    if he wants or not to start the game.
    """
    while True:
        choice = input("Would you like your username to be considered? (y/n): ").lower()
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
    categories = SHEET.worksheet("categories")
    while True:
        choice = input("Enter the number of your choice (1/2/3): \n")
        if choice in ['1', '2', '3']:
            if choice == '1':
                words_list = categories.col_values(1)[1:]
                category_name = "Politics"
            elif choice == '2':
                words_list = categories.col_values(2)[1:]
                category_name = "Society"
            elif choice == '3':
                words_list = categories.col_values(3)[1:]
                category_name = "Hobbies"
            
            return category_name, random.choice(words_list)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def play(word):
    """
    Contains the setting to start the Hangman game.
    """
    print("You will have 6 tries before loose.")
    print("When you loose the first step, you won't be allow to continue the game.")
    print("You should then start over, from the beginning ! :-D")

    word_construction = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6
    print("Let's play Hangman!")
    print(display_hangman(tries))
    print(word_construction)
    print("\n")
    while not guessed and tries > 0:
        guess = input("Please guess a letter or word: \n").upper()
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You already guessed the letter", guess)
            elif guess not in word:
                print(guess, "is not in the word.")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print("Good job,", guess, "is in the word!")
                guessed_letters.append(guess)
                word_as_list = list(word_construction)
                indices = [i for i, letter in enumerate(word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                word_construction = "".join(word_as_list)
                if "_" not in word_construction:
                    guessed = True
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print("You already guessed the word", guess)
            elif guess != word:
                print(guess, "is not the word.")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_construction = word
        else:
            print("Not a valid guess.")
        print(display_hangman(tries))
        print(word_construction)
        print("\n")
    if guessed:
        print("Congratulations, you guessed the word! You win!")
    else:
        print("Sorry, you ran out of tries. The word was " + word + ". Maybe next time!")


def display_hangman(tries):
    """
    Contains parts of the hangman and the stages.
    """
    stages = [  # final state: head, torso, both arms, and both legs
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
                # head, torso, both arms, and one leg
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """,
                # head, torso, and both arms
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """,
                # head, torso, and one arm
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """,
                # head and torso
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
                # head
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
                # initial empty state
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """
    ]
    return stages[tries]

def scrambled_sentence():
    """
    This function allows the user to select a category, 
    retrieves a random sentence from the selected category,
    scrambles the words in that sentence, and then asks the user to unscramble it.
    """
    sentences = SHEET.worksheet("sentences")
    while True:
        print("Do you want to change the category?")
        choice = input("Choose one more time - 1: Politics, 2: Society, 3: Hobbies: \n")
        if choice in ['1', '2', '3']:
            if choice == '1':
                words_list = sentences.col_values(1)[1:]
            elif choice == '2':
                words_list = sentences.col_values(2)[1:]
            elif choice == '3':
                words_list = sentences.col_values(3)[1:]
            
            chosen_sentence = random.choice(words_list)
            sentence_elements = chosen_sentence.split()
            random.shuffle(sentence_elements)
            jumbled_sentence = " ".join(sentence_elements)
            
            print("Unscramble this sentence: " + jumbled_sentence)
            
            while True:
                guess = input("Guess: ")
                if guess.lower().strip() != chosen_sentence.lower():
                    print("Incorrect, try again!")
                else:
                    print("Congratulations! You rocked it again !!!")
                    break                    
            return chosen_sentence
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def convert_to_plural(chosen_sentence):
    """
    This function prompts the user to convert 
    a given sentence to its plural form.
    It then records the user's answer along 
    with their username in a Google Sheets worksheet named 'answers'.
    """
    print("For the last step of this game, you will...")
    print(f"Convert the sentence you've just unscrambled to the plural.")
    print(f"The sentence to take into consideration is: {chosen_sentence}")
    print(chosen_sentence)
    user_plural = input("Enter the plural form of the sentence: \n")
    return user_plural

    print("Your response has been recorded. Thank you!")

def update_worksheet(user_name, selected_category, user_plural):
    """
    This function will update each column of the worksheet.
    """
    answers_worksheet = SHEET.worksheet('answers')
    answers_worksheet.append_row([user_name, selected_category, user_plural]) 

def main():
    """
    Run all program functions
    """
    user_name = get_username()
    print(f"Hello, {user_name}! Welcome to this challenge.")
    print("You are about to start a game of 3 steps.")
    print("Soon you will start the Hangman game to guess the right word.")

    if choose_to_continue(user_name):
        selected_category, random_word = choose_category()
        print("Selected category:", selected_category)

    word = random_word.upper()
    play(word)
    while input("Play Again? (Y/N) Press 'N' to continue with the next challenge.").upper() == "Y":
        selected_category, random_word = choose_category()
        play(random_word.upper())
    
    random_sentence = scrambled_sentence()
    print(random_sentence)

    sentence_plural = convert_to_plural(random_sentence)
    print(sentence_plural)

    update_worksheet(user_name, selected_category, sentence_plural) 

print("Welcome to the letters and Grammar game!")
if __name__ == "__main__":
    main()