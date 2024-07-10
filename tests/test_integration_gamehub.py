import pytest # type: ignore
from gamehub.snake import Snake
from gamehub.game_of_life import GameOfLife
from gamehub.chess.chess import Chess
from gamehub.wordle import Wordle
from gamehub.gamehub import GameHub
import argparse

class TestIntegrationGameHub:
    def test_integration_arguments_snake(self, monkeypatch):
        def namespace_generator(self) -> argparse.Namespace:
            return argparse.Namespace(
                game="snake",
                difficulty="Easy"
            )
        
        monkeypatch.setattr(GameHub, "setup_parsers", namespace_generator)
        monkeypatch.setattr(Snake, "init_game", lambda n: None)

        g = GameHub()
        game = g.run()
        assert game.difficulty == "Easy"
    
    def test_integration_arguments_gol(self, monkeypatch):
        def namespace_generator(self) -> argparse.Namespace:
            return argparse.Namespace(
                game="game_of_life",
                speed=100,
                mode="Automatic",
                density=30
            )
        
        monkeypatch.setattr(GameHub, "setup_parsers", namespace_generator)
        monkeypatch.setattr(GameOfLife, "init_game", lambda n: None)

        g = GameHub()
        game = g.run()
        assert game.speed == 100 and game.mode == "Automatic" and game.density == 30

    def test_integration_arguments_chess(self, monkeypatch):
        def namespace_generator(self) -> argparse.Namespace:
            return argparse.Namespace(
                game="chess",
                mode="Multiplayer"
            )
        
        monkeypatch.setattr(GameHub, "setup_parsers", namespace_generator)
        monkeypatch.setattr(Chess, "init_game", lambda n: None)

        g = GameHub()
        game = g.run()
        assert game.mode == "Multiplayer"

    def test_integration_arguments_wordle(self, monkeypatch):
        def namespace_generator(self) -> argparse.Namespace:
            return argparse.Namespace(
                game="wordle"
            )
        
        monkeypatch.setattr(GameHub, "setup_parsers", namespace_generator)
        monkeypatch.setattr(Wordle, "init_game", lambda n: None)

        g = GameHub()
        game = g.run()
        assert isinstance(game, Wordle)