import argparse
from . import snake, game_of_life, wordle
import gamehub.chess.chess as chess

class GameHub:
    def __init__(self) -> None:
        self.args = self.setup_parsers()

    def apply_bound(self, value : int, lower_bound : int, upper_bound : int):
        if value < lower_bound:
            return lower_bound
        elif value > upper_bound:
            return upper_bound
        else:
            return value
        
    def setup_parsers(self) -> argparse.Namespace:
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

        # Subparser for Wordle
        wordle_parser = subparsers.add_parser("wordle", help="Play Wordle.")
        # Subparser for Chess
        chess_parser = subparsers.add_parser("chess", help="Play Chess.")
        chess_parser.add_argument("--mode", type=str, default="Multiplayer", choices=["Singleplayer", "Multiplayer"], help="The mode of the game.")

        return parser.parse_args()


    def run(self):
        game = None
        if self.args.game == "snake":
            game = snake.Snake(self.args.difficulty)
        elif self.args.game == "game_of_life":
            game = game_of_life.GameOfLife(self.apply_bound(self.args.speed, 50, 10000),
                                    self.args.mode,
                                    self.apply_bound(self.args.density, 0, 100))
        elif self.args.game == "wordle":
            game = wordle.Wordle()
        elif self.args.game == "chess":
            game = chess.Chess(self.args.mode)
            
        if game is not None:
            game.init_game()

        return game