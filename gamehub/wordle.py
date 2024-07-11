import curses
from curses import wrapper
import random
import string
import time

class Wordle:
    def __init__(self):
        pass

    def draw_initial_board(self, stdscr : object, guessed_word : str, guesses : int, alphabet : list) -> None:
        stdscr.clear()
        stdscr.addstr(1, 30, "Enter a five letter word, press Enter to confirm or ESC to exit.")
        stdscr.addstr(2, 30, "Inserted word: " + "".join(guessed_word))
        stdscr.addstr(3, 30, "Until now: " + "".join(guessed_word))
        stdscr.addstr(4, 30, "Guesses left: " + str(guesses))
        stdscr.addstr(6, 30, "Available letters: " + "".join(alphabet))
        stdscr.refresh()

    def draw_inserted_word(self, stdscr : object, void_guessed_word : list) -> None:
        stdscr.addstr(2, 30, "Inserted word: " + "".join(void_guessed_word))
        stdscr.refresh()

    def draw_after_update(self, stdscr : object, guessed_word : list, guesses : int, alphabet : list) -> None:
        stdscr.addstr(3, 30, "Until now: " + "".join(guessed_word))
        stdscr.addstr(4, 30, "Guesses left: " + str(guesses))
        stdscr.addstr(6, 30, "                                                                                  ")
        stdscr.refresh()
        stdscr.addstr(6, 30, "Available letters: " + "".join(alphabet))
        stdscr.refresh()

    def draw_losing_message(self, stdscr : object, word_to_guess : str) -> None:
        stdscr.clear()
        stdscr.addstr(0, 30, "Game over! You ran out of guesses.")
        stdscr.addstr(1, 30, "The word was: " + word_to_guess)
        stdscr.refresh()
        time.sleep(2)

    def draw_winning_message(self, stdscr : object) -> None:
        stdscr.clear()
        stdscr.addstr(0, 30, "You won!.")
        stdscr.refresh()
        time.sleep(2)

    def draw_after_invalid_input(self, stdscr : object) -> None:
        stdscr.addstr(5, 30, "The inserted word is invalid. Please choose another word.")
        stdscr.refresh()
        time.sleep(1)
        stdscr.addstr(5, 30, "                                                         ")
        stdscr.refresh()

    def generate_list_of_words(self) -> list:
        with open('/home/gamehub/files/words.txt', 'r') as file:
            words = file.read().splitlines()
        return words

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

    def check_terminal_size(self, min_lines : int, min_cols : int, stdscr : object) -> bool:
        if curses.COLS < min_cols or curses.LINES < min_lines:
            stdscr.addstr(0, 0, "Resize the terminal (" + str(min_cols) + "x" + str(min_lines) + ")", curses.A_BOLD)
            stdscr.refresh()
            time.sleep(2)
            return False
        return True
    
    def initialize_game(self, stdscr : object) -> tuple:
        curses.curs_set(0)
        meaningful_words = self.generate_list_of_words()
        word_to_guess = random.choice(meaningful_words)
        guessed_word = ["_" for _ in range(5)] # Cotains only the letters that the player has guessed
        guesses = 6
        alphabet = list(string.ascii_lowercase)
        game_stopped = False # Flag to stop the game (when the player wins or loses)
        self.draw_initial_board(stdscr, guessed_word, guesses, alphabet)

        return meaningful_words, word_to_guess, guessed_word, guesses, alphabet, game_stopped

    def gameloop(self, stdscr : object) -> None:
        if not self.check_terminal_size(10, 100, stdscr): # Check if the terminal size is enough to play the game
            return
        
        meaningful_words, word_to_guess, guessed_word, guesses, alphabet, game_stopped = self.initialize_game(stdscr)

        while not game_stopped:
            characters = 0 # Number of characters inserted by the player
            void_guessed_word = ["_" for _ in range(5)] # The space where the player inserts a new guess
            self.draw_inserted_word(stdscr, void_guessed_word)

            while characters <= 5:
                inserted_char = stdscr.getkey()               
                if inserted_char == '\x1b': # If the player presses ESC then exit the game
                    break
                elif inserted_char == '\x7f' and characters > 0: # If the player presses Backspace then delete the last character
                    characters -= 1
                    void_guessed_word[characters] = "_"
                    self.draw_inserted_word(stdscr, void_guessed_word)
                elif inserted_char in list(string.ascii_lowercase) and inserted_char != '\n' and characters != 5:
                    characters += 1
                    void_guessed_word[characters - 1] = inserted_char
                    self.draw_inserted_word(stdscr, void_guessed_word)
                elif inserted_char == '\n' and characters == 5:
                    break

            if inserted_char == '\x1b':
                break

            void_guessed_word = ''.join(void_guessed_word) # Check if the guessed word is meaningful
            if void_guessed_word not in meaningful_words:
                self.draw_after_invalid_input(stdscr)
            else:
                guesses -= 1
                guessed_word, alphabet = self.generate_updated_guess(void_guessed_word, word_to_guess, alphabet, guessed_word)
                self.draw_after_update(stdscr, guessed_word, guesses, alphabet)
                
                if guesses >= 0 and void_guessed_word == word_to_guess:
                    game_stopped = True
                    self.draw_winning_message(stdscr)
                
                if guesses == 0 and void_guessed_word != word_to_guess:
                    game_stopped = True
                    self.draw_losing_message(stdscr, word_to_guess)

                stdscr.refresh()
                time.sleep(1)

    def init_game(self) -> None:
        wrapper(self.gameloop)