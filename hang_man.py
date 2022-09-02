import os
import random
import re

main_menu = [
    "Welcome to HangMan!\nPlease choose one or more categories to generate words from:",
    "(a) Movies",
    "(b) Games",
    "(c) TV-Shows",
    "(d) Anime\n"
]


def run_menu():
    movies = open("lists/movies list.txt", "r")  # Open word files in read mode
    games = open("lists/games list.txt", "r")
    tv = open("lists/tv list.txt", "r")
    anime = open("lists/anime list.txt", "r")
    for row in main_menu:
        print(row)
    categories = ""
    answer = input()
    answer = answer.lower()
    answer = answer.replace(" ", "")
    file = open("temp.txt", "a+")  # File which will contain words from chosen categories (reading and appending mode)
    if not re.findall("[e-z]", answer) and answer.isalpha():  # answer only contains the letters "abcd"
        if "a" in answer:
            categories += "Movies + "
            for line in movies.readlines():  # Read file and split new lines on "\n"
                file.write(line)
            movies.close()  # Close word files
        if "b" in answer:
            categories += "Games + "
            for line in games.readlines():
                file.write(line)
            games.close()
        if "c" in answer:
            categories += "TV-Shows + "
            for line in tv.readlines():
                file.write(line)
            tv.close()
        if "d" in answer:
            categories += "Anime + "
            for line in anime.readlines():
                file.write(line)
            anime.close()
        categories = categories[0:-3]  # Remove final " + " (which is added manually)
        file.close()
        print("\nA game of HangMan (" + categories + ") will begin:\n")
        return True
    else:
        print("MENU RESET. Enter one or more of the categories below (a, b, c or d).\n", end='')
        return False


def get_word(random_number):
    f = open("temp.txt", "r")
    lines = f.read().splitlines()  # Remove the break new line ("\n") at the end of line
    ret = lines[random_number - 1]
    return ret


def get_lines_count(file):
    return sum(1 for _ in file)  # Count 1 for each line


def get_chars_count(count_chars):
    counter = 0
    for index in count_chars:
        if index != " ":
            counter += 1
    return counter


def hide_word(word):
    hidden = ""
    for hide in range(len(word)):  # for 0 in (x-1)
        if word[hide] == " ":
            hidden += " "
        else:
            hidden += "_"
    return hidden


def play(hidden, word, count):
    under_lines = list(hidden)  # Will make it easier to change chars in string
    answer = list(word)  # When done, do - "".join(list to join as string)
    upper_word = word.upper()
    upper_word_list = list(upper_word)
    playing = True
    guesses = 5
    count_check = 0
    chars_bank = ""
    print(hidden)
    while playing:
        bank_check = True
        user_guess = input("\n\nEnter a character: \n")
        while re.findall("[^a-z0-9]", user_guess.lower()) or len(user_guess) != 1:
            print("Illegal input, please enter a character in the range of (a-z) and (0-9):")
            user_guess = input()
        while bank_check:
            if user_guess in chars_bank:
                user_guess = input("[" + user_guess + "] was used before. Enter a character in the range of (a-z) and "
                                                      "(0-9):\n")
            else:
                chars_bank += user_guess
                bank_check = False
        if user_guess.upper() in str(answer).upper():  # Upper in order to ignore if the letter is written in lower case
            while user_guess.upper() in str(answer).upper():
                i = upper_word_list.index(user_guess.upper())  # Returns index of the letter guessed
                under_lines[i] = answer[i]
                answer[i] = " "
                upper_word_list[i] = " "
                count_check += 1
                if count_check == count:
                    print("You win")
                    print("The word is: " + word)
                    playing = False
            if count_check != count:
                print("".join(under_lines) + "\nYou have, " + str(guesses) + " guesses left")
        else:
            guesses -= 1
            if guesses == 0:
                print("You lose")
                print("The word is: " + word)
                playing = False
            elif guesses != 0:
                print("".join(under_lines) + "\nTry again, " + str(guesses) + " guesses left")
        list_chars_bank = list(chars_bank)
        print("Used characters bank:\n" + str(list_chars_bank).upper())


stop_game = False
while stop_game is False:
    check = False
    while check is False:
        check = run_menu()
    categories_file = open("temp.txt", "r")
    count_lines = get_lines_count(categories_file)
    categories_file.close()

    random_num = random.randint(1, count_lines)  # Get a random integer in lines range
    word_to_guess = get_word(random_num)
    word_to_guess = word_to_guess[0:]

    chars_count = get_chars_count(list(word_to_guess))

    under_lines_guess = hide_word(word_to_guess)

    play(under_lines_guess, word_to_guess, chars_count)
    decide = input("\n\nDo you want to play again (yes \\ no)? ")
    check_decision = True
    while check_decision is True:
        if "no" in decide.lower():
            stop_game = True
            check_decision = False
            print("Quit game")
        elif "yes" in decide.lower():
            check_decision = False
        else:
            decide = input("If you want to play again enter \"yes\", if you wish to quit enter \"no\": ")
    os.remove("temp.txt")  # Delete file (no longer needed)
