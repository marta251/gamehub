import argparse
import snake

def main():
    parser = argparse.ArgumentParser(prog="gamehub", description="GameHub is a game launcher for the terminal.")
    parser.add_argument("--game", type=str, required=True, choices=["snake"], help="The game to be played.")

    args = parser.parse_args()
    if args.game == "snake":
        snake.init_game()
        
        
if __name__ == "__main__":
    main()