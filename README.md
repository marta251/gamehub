# GameHub
**A collection of games you can play from your terminal.**

GameHub is a command-line application that allows users to play a series of games whose graphical interface is managed using Python's [curses library](https://docs.python.org/3/howto/curses.html). Here are the currently implemented games:

### Chess
Two players can play on the same terminal (multi-player mode) or you can play alone against an AI (single-player mode). If you are playing alone be ready to lose (you are playing against Stockfish).

### Snake
You can choose between three levels of difficulty (easy, medium, hard).

### Conway's Game of Life
A cellular automaton where you can observe the evolution of cells based on simple rules. It is a zero-player game, meaning that its evolution is determined by only its initial state, requiring no further input. You can choose between manual (an iteration is executed every time an input is received) and automatic mode (an iteration is periodically executed with the desired time interval), the speed and the density of the initial configuration.

### Word Guesser
You have to guess a random 5-letter English word. After each attempt the letters that are not present in the target word are removed from the available letters list and the ones that are present are shown on the terminal. You have six attempts to guess the word.


## Usage
You can use the following command structure to run any of the games:
```
gamehub <game_name> [options]
```
To check the available options for each game you can use:
```
gamehub <game_name> -h
```
Usage example:
```
gamehub game_of_life --mode Automatic --speed 100 --density 20
```

## Installation
### Normal Installation
### Using Docker Hub
You can also pull the pre-build image from Docker Hub:

1. Ensure you have already installed Docker. Otherwise you can follow the instructions [here](https://docs.docker.com/engine/install/).

2. Pull the GameHub Docker image from Docker Hub: 
    ```
    docker pull marta251/gamehub
    ```

3. Run the docker container
    ```
    docker run -it marta251/gamehub
    ```

## Maintainers
- marta01.malagutti@edu.unife.it
- riccardo.morelli@edu.unife.it