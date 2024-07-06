import curses
from curses import wrapper
import random
import string
import time

#TODO: create some more functions to make the code more readable, comment the word to guess, 
# change the position of the whole game (maybe to the center of the screen) and
# update the alphabet (maybe it is not necessary)

# TODO: add 'self' in the function signature and add init_game function

def how_good_is_the_guess(new_guessed : str, to_guess : str, alphabet : list, old_guessed : str) -> tuple:
    updated_guess = ["_" for _ in range(5)]
    for i in range(5): # For every character in the guessed word check if it is in the target word
        if new_guessed[i] in to_guess: # If the character is in the target word put it whereever it is needed
            for j in range(5):
                if new_guessed[i] == to_guess[j]:
                    updated_guess[j] = new_guessed[i]
        else:
            # Remove guessed[i] from the alphabet (only if it is still there)
            if new_guessed[i] in alphabet:
                alphabet.remove(new_guessed[i])
    
    for i in range(5):
        if updated_guess[i] == "_" and old_guessed[i] != "_":
            updated_guess[i] = old_guessed[i]

    return updated_guess, alphabet

def generate_list_of_words() -> list:
    with open('words.txt', 'r') as file:
        words = file.read().splitlines()
    return words

def gameloop(stdscr) -> None:
    curses.curs_set(0)

    meaningful_words = generate_list_of_words() # Generate a list of meaningful words
    word_to_guess = random.choice(meaningful_words) # Choose a random word from the list

    guessed_word = ["_" for _ in range(5)] # Only the letters that the player has guessed
    guesses = 6
    alphabet = list(string.ascii_lowercase)

    stdscr.clear()
    stdscr.addstr(0, 0, "Target word: " + "".join(word_to_guess))
    stdscr.addstr(1, 0, "Inserted word: " + "".join(guessed_word))
    stdscr.addstr(2, 0, "Until now: " + "".join(guessed_word))
    stdscr.addstr(3, 0, "Guesses left: " + str(guesses))
    stdscr.addstr(6, 0, "Alphabet: " + "".join(alphabet))
    stdscr.refresh()

    game_stopped = False # Flag to stop the game (when the player wins or loses)

    while not game_stopped: # While the game is not finished
        void_guessed_word = ["_" for _ in range(5)] # The space where the player inserts a new guess
        characters = 0 # Number of characters inserted by the player

        stdscr.addstr(1, 0, "Inserted word: " + "".join(void_guessed_word))
        # stdscr.addstr(2, 0, "Until now: " + "".join(guessed_word))
        stdscr.refresh()

        for i in range(5):
            inserted_char = stdscr.getkey() # Get the character inserted by the player
            if inserted_char not in list(string.ascii_lowercase) or inserted_char == '\n':
                i -= 1
            else:
                characters += 1
                void_guessed_word[characters - 1] = inserted_char
                stdscr.addstr(1, 0, "Inserted word: " + ''.join(void_guessed_word))
                stdscr.refresh()
            
        # Now the player has inserted 5 characters from the alphabet and can press Enter
        inserted_char = stdscr.getkey()
        while inserted_char != '\n':
            inserted_char = stdscr.getkey()

        # At this point, we have to check if the guessed word is in the list of meaningful words
        void_guessed_word = ''.join(void_guessed_word)
        if void_guessed_word not in meaningful_words:
            stdscr.addstr(5, 0, "The inserted word is invalid. Please choose another word.")
            stdscr.refresh()
            time.sleep(1)
            stdscr.addstr(5, 0, "                                                         ")
            stdscr.refresh()
            characters = 0
            void_guessed_word = ["_" for _ in word_to_guess]
        else:
            guesses -= 1
            guessed_word, alphabet = how_good_is_the_guess(void_guessed_word, word_to_guess, alphabet, guessed_word)
            
            stdscr.addstr(2, 0, "Until now: " + "".join(guessed_word))
            stdscr.addstr(3, 0, "Guesses left: " + str(guesses))
            stdscr.addstr(6, 0, "Alphabet: " + "".join(alphabet))
            if guesses >= 0 and guessed_word == list(word_to_guess):
                game_stopped = True
                stdscr.clear()
                stdscr.addstr(0, 0, "You won!.")
                stdscr.refresh()
                time.sleep(1)
            
            if guesses == 0 and guessed_word != list(word_to_guess):
                game_stopped = True
                stdscr.clear()
                stdscr.addstr(0, 0, "Game over! You ran out of guesses.")
                stdscr.refresh()
                time.sleep(1)
            
            stdscr.refresh()
            time.sleep(1)

wrapper(gameloop)

'''
def init_game(self) -> None:
    wrapper(self.gameloop)  # Call the function via wrapper
'''