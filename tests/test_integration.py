import pytest # type: ignore
from gamehub.game_of_life import GameOfLife
from gamehub.gamehub import GameHub
import argparse

class TestIntegration:
    def test_integration_arguments(self, monkeypatch):
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