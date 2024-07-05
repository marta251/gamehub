import curses
from curses import wrapper
import random
import string
import time

def generate_list_of_words() -> list:
    with open('words.txt', 'r') as file:
        words = file.read().splitlines()
    return words

# TODO: add 'self' in the function signature and add init_game function
def gameloop(stdscr) -> None:
    curses.curs_set(0)

    meaningful_words = generate_list_of_words() # Generate a list of meaningful words
    word_to_guess = random.choice(meaningful_words) # Choose a random word from the list

    guessed_word = ["_" for _ in word_to_guess]
    guesses = 6
    alphabet = string.ascii_lowercase

    stdscr.clear()
    stdscr.addstr(0, 0, "Target word: " + "".join(word_to_guess))
    stdscr.addstr(1, 0, "Guessed word: " + "".join(guessed_word))
    stdscr.addstr(3, 0, "Guesses left: " + str(guesses))
    stdscr.refresh()

    game_stopped = False # Flag to stop the game (when the player wins or loses)
    characters = 0 # Number of characters inserted by the player

    while not game_stopped: # While the game is not finished
        while True:
            inserted_char = stdscr.getkey() # Get the character inserted by the player
            if ord(inserted_char) == 10: # If the player presses Enter
                break
            else:
                characters += 1 # Increment the number of inserted characters
                guessed_word[characters - 1] = inserted_char
                stdscr.addstr(1, 0, "Guessed word: " + ''.join(guessed_word))
                stdscr.refresh()

        # At this point, the player has pressed Enter
        guessed_word = ''.join(guessed_word)
        if guessed_word in meaningful_words:
            game_stopped = True
            stdscr.clear()
            stdscr.addstr(1, 0, "Do all the necessary checks.")
            stdscr.refresh()
            time.sleep(2)
        else:
            game_stopped = True
            stdscr.clear()
            stdscr.addstr(1, 0, "The word is not meaningful. Please choose another word.")
            stdscr.addstr(4, 0, "Chars: " + ''.join(str(characters)))
            stdscr.refresh()
            time.sleep(2)

        '''
        if letter in word_to_guess: # If the chosen letter is in the target word you have to find it
            for i in range(len(word_to_guess)):
                if word_to_guess[i] == letter:
                    guessed_word[i] = letter
                    stdscr.addstr(1, 0, "Guessed word: " + "".join(guessed_word))
                    stdscr.refresh()
                    if guessed_word == list(word_to_guess): # If the guessed word is the target word, the player wins
                        game_stopped = True
                        stdscr.clear()
                        stdscr.addstr(0, 0, "Congratulations! You guessed the word.")
                        stdscr.refresh()
                        break
        else:
            guesses -= 1
            if guesses == 0:
                game_stopped = True
                stdscr.clear()
                stdscr.addstr(0, 0, "Game over! You ran out of guesses.")
                stdscr.refresh()
                break
            else:
                stdscr.addstr(3, 0, "Guesses left: " + str(guesses))
                stdscr.refresh()
    time.sleep(2)
    '''

wrapper(gameloop)

'''
def init_game(self) -> None:
    wrapper(self.gameloop)  # Call the function via wrapper
'''