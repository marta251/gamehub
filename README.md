# GameHub
A collection of games you can play from your terminal.

The project involves the development of a command-line application that will allow users to play a series of classic games. Specifically, the graphical interface will be managed directly in the terminal using Python's curses library (https://docs.python.org/3/howto/curses.html).

Here is the list of games we intend to implement:
- Chess
- Checkers
- Conway's Game of Life
- Snake
- Wordle

Nevertheless, the application will be structured to allow easy extension with new games in the future.

Each game will have its own set of options:
- Chess: single-player mode (play alone against an AI) or multiplayer mode (two players on the same terminal)
- Checkers: single-player or multiplayer mode
- Conway's Game of Life: speed, manual mode (an epoch is executed each time user input is received) or automatic mode (an iteration is periodically executed, with the option to set the desired time interval), density
- Snake: game difficulty

The idea for handling the AI, necessary for the single-player mode in chess, is to use the Stockfish ReST API or the Stockfish application itself. Specifically, the plan is to create two Docker images: the first will be lighter and require an Internet connection as it will use the ReST API to calculate AI moves, while the second will contain Stockfish itself, making it heavier but not requiring an Internet connection.

Usage examples:

gamehub chess --mode multiplayer

gamehub game-of-life --speed 100 --mode Automatic --density 45

gamehub snake --difficulty Easy