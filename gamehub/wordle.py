import curses
from curses import wrapper
import random
import string
import time

class Wordle:
    def __init__(self):
        pass

    def draw_after_invalid_input(self, stdscr : object) -> None:
        stdscr.addstr(5, 0, "The inserted word is invalid. Please choose another word.")
        stdscr.refresh()
        time.sleep(1)
        stdscr.addstr(5, 0, "                                                         ")
        stdscr.refresh()

    def generate_updated_guess(self, new_guessed : str, to_guess : str, alphabet : list, old_guessed : str) -> tuple:
        updated_guess = ["_" for _ in range(5)]
        for i in range(5): # For every character in the guessed word check if it is in the target word
            if new_guessed[i] in to_guess: # If the character is in the target word put it wherever it is needed
                for j in range(5):
                    if new_guessed[i] == to_guess[j]:
                        updated_guess[j] = new_guessed[i]
            else:
                if new_guessed[i] in alphabet: # Remove guessed[i] from the alphabet (only if it is still there)
                    alphabet.remove(new_guessed[i])
        
        for i in range(5): # Check if the character is already guessed or not
            if updated_guess[i] == "_" and old_guessed[i] != "_":
                updated_guess[i] = old_guessed[i]

        return updated_guess, alphabet

    def draw_initial_board(self, stdscr : object, guessed_word : str, guesses : int, alphabet : list) -> None:
        stdscr.clear()
        stdscr.addstr(1, 0, "Inserted word: " + "".join(guessed_word))
        stdscr.addstr(2, 0, "Until now: " + "".join(guessed_word))
        stdscr.addstr(3, 0, "Guesses left: " + str(guesses))
        stdscr.addstr(6, 0, "Available letters: " + "".join(alphabet))
        stdscr.addstr(8, 0, "Enter a five letter word and press Enter to confirm your choice.")
        stdscr.refresh()

    def generate_list_of_words(self) -> list:
        with open('words.txt', 'r') as file:
            words = file.read().splitlines()
        return words

    def gameloop(self, stdscr : object) -> None:
        curses.curs_set(0)

        meaningful_words = self.generate_list_of_words()
        word_to_guess = random.choice(meaningful_words)

        guessed_word = ["_" for _ in range(5)] # Cotains only the letters that the player has guessed
        guesses = 6
        alphabet = list(string.ascii_lowercase)

        self.draw_initial_board(stdscr, guessed_word, guesses, alphabet)

        game_stopped = False # Flag to stop the game (when the player wins or loses)
        while not game_stopped:
            void_guessed_word = ["_" for _ in range(5)] # The space where the player inserts a new guess
            characters = 0 # Number of characters inserted by the player

            stdscr.addstr(1, 0, "Inserted word: " + "".join(void_guessed_word))
            stdscr.refresh()

            for i in range(5): # The player can insert 5 characters from the alphabet and then press Enter
                inserted_char = stdscr.getkey()
                if inserted_char not in list(string.ascii_lowercase) or inserted_char == '\n':
                    i -= 1
                else:
                    characters += 1
                    void_guessed_word[characters - 1] = inserted_char
                    stdscr.addstr(1, 0, "Inserted word: " + ''.join(void_guessed_word))
                    stdscr.refresh()
        
            inserted_char = stdscr.getkey() # Now the player can press Enter
            while inserted_char != '\n':
                inserted_char = stdscr.getkey()

            void_guessed_word = ''.join(void_guessed_word) # Check if the guessed word is in the list of meaningful words
            if void_guessed_word not in meaningful_words:
                self.draw_after_invalid_input(stdscr)
                characters = 0
                void_guessed_word = ["_" for _ in range(5)]
            else:
                guesses -= 1
                guessed_word, alphabet = self.generate_updated_guess(void_guessed_word, word_to_guess, alphabet, guessed_word)
                
                stdscr.addstr(2, 0, "Until now: " + "".join(guessed_word))
                stdscr.addstr(3, 0, "Guesses left: " + str(guesses))
                stdscr.addstr(6, 0, "                                                                                  ")
                stdscr.refresh()
                stdscr.addstr(6, 0, "Available letters: " + "".join(alphabet))
                stdscr.refresh()

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
                    stdscr.addstr(1, 0, "The word was: " + word_to_guess)
                    stdscr.refresh()
                    time.sleep(1)
                
                stdscr.refresh()
                time.sleep(1)

    def init_game(self) -> None:
        wrapper(self.gameloop)