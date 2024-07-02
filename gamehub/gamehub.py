import argparse
from . import snake, game_of_life

def main():
    parser = argparse.ArgumentParser(prog="gamehub", description="GameHub is a game launcher for the terminal.")
    parser.add_argument("--game", type=str, required=True, choices=["snake", "game_of_life"], help="The game to be played.")

    args = parser.parse_args()
    if args.game == "snake":
        snake.Snake().init_game()
    elif args.game == "game_of_life":
        game_of_life.GameOfLife().init_game()
        
        
if __name__ == "__main__":
    main()