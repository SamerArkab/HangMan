import os
import random

main_menu = [
    "Welcome to HangMan!\nPlease choose one or more categories to generate words from:",
    "(a) Movies",
    "(b) Games",
    "(c) TV-Shows",
    "(d) Anime\n"
]


def run_menu():
    movies = open("movies list.txt", "r")  # Open word files
    games = open("games list.txt", "r")
    tv = open("tv list.txt", "r")
    anime = open("anime list.txt", "r")
    for main in main_menu:
        print(main)
    categories = ""
    answer = input()
    file = open("temp.txt", "a+")  # File which will contain words from chosen categories
    while "a" or "b" or "c" or "d" in answer:
        if "a" in answer:
            categories += "Movies + "
            for i in movies.readlines():
                file.write(i)
            movies.close()  # Close word files
        if "b" in answer:
            categories += "Games + "
            for j in games.readlines():
                file.write(j)
            games.close()
        if "c" in answer:
            categories += "TV-Shows + "
            for k in tv.readlines():
                file.write(k)
            tv.close()
        if "d" in answer:
            categories += "Anime + "
            for t in anime.readlines():
                file.write(t)
            anime.close()
        categories = categories[0:-3]
        file.close()
        print("\nA game of HangMan (" + categories + ") will begin:\n")
        return True
    print("The menu will reset, enter one or more of the categories below (a, b or c).\n")
    return False


def get_word(random_number):
    f = open("temp.txt", "r")
    lines = f.readlines()
    ret = lines[random_number-1]
    return ret


def get_lines_count(file):
    return sum(1 for line in file)  # For each line count 1+1+...


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
        while user_guess in "\n =+-*/.`~!@#$%^&*()_,';:":
            print("Illegal input, please enter a character in the range of (a-z) and (0-9):")
            user_guess = input()
            chars_bank += user_guess
        while bank_check:
            if user_guess in chars_bank:
                user_guess = input("Input was used before. Enter a character in the range of (a-z) and (0-9):\n")
            else:
                chars_bank += user_guess
                bank_check = False
        if user_guess.upper() in str(answer).upper():  # upper in order to ignore if the letter is written
            while user_guess.upper() in str(answer).upper():  # in upper case or lower case
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

    random_num = random.randint(1, count_lines)  # Get a random integer
    word_to_guess = get_word(random_num)
    word_to_guess = word_to_guess[0:-1]  # Remove the "\n" char

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