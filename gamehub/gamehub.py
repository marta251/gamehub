import argparse
from . import snake, game_of_life

# TODO: Implement the relative unit tests for the following functions

def apply_bound(value : int, lower_bound : int, upper_bound : int):
    if value < lower_bound:
        return lower_bound
    elif value > upper_bound:
        return upper_bound
    else:
        return value

def main():
    parser = argparse.ArgumentParser(prog="gamehub", description="GameHub is a game launcher for the terminal.")
    subparsers = parser.add_subparsers(dest="game", help="The game to be played.")

    # Subparser for snake game
    snake_parser = subparsers.add_parser("snake", help="Play Snake.")
    snake_parser.add_argument("--difficulty", type=str, default="Medium", choices=["Easy","Medium","Hard"], help="The difficulty level of the game.")

    # Subparser for Game of Life
    game_of_life_parser = subparsers.add_parser("game_of_life", help="Play Game of Life.")
    game_of_life_parser.add_argument("--speed", type=int, default=100, help="The speed of the simulation in ms.")
    game_of_life_parser.add_argument("--mode", type=str, default="Automatic", choices=["Manual","Automatic"], help="Manual: press any key to update; Automatic: update happens periodically.")
    game_of_life_parser.add_argument("--density", type=int, default=30, help="The initial density of the grid.") 

    args = parser.parse_args()
    if args.game == "snake":
        snake.Snake(args.difficulty).init_game()
    elif args.game == "game_of_life":
        game_of_life.GameOfLife(apply_bound(args.speed, 50, 10000),
                                args.mode,
                                apply_bound(args.density, 0, 100)).init_game()
        
if __name__ == "__main__":
    main()