"""
This module contains the unit tests for the GameHub class.
"""
import sys
import pytest # type: ignore
from gamehub.gamehub import GameHub
from hypothesis import given, strategies, settings, HealthCheck # type: ignore
from hypothesis.strategies import composite # type: ignore

class TestGameHub:
    """
    This class contains the unit tests for the GameHub class.
    """
    @composite
    def smaller_than(draw) -> tuple[int, int]:
        """
        Generate two integers where the second one is greater than the first one.
        """
        a = draw(strategies.integers())
        b = draw(strategies.integers(min_value=a))
        return a, b
    @given(strategies.integers(), smaller_than())
    @settings(max_examples=20, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_apply_bound_range(self, monkeypatch, x : int, bounds : tuple[int, int]) -> None:
        """
        Test that the result is always within the bounds.
        """
        monkeypatch.setattr(GameHub, "setup_parsers", lambda n: None)
        g = GameHub()
        res = g.apply_bound(x, bounds[0], bounds[1])
        assert bounds[0] <= res and res <= bounds[1]
    @pytest.mark.parametrize("x, lower, upper, expected",
                             [(1, 0, 2, 1),
                              (0, 0, 2, 0),
                              (2, 0, 2, 2),
                              (3, 0, 2, 2)])
    def test_apply_bound(self,
                         x : int,
                         lower : int,
                         upper : int,
                         expected : int,
                         monkeypatch) -> None:
        """
        Test the correctness of the method that applies a lower and an upper bound to a given value.
        """
        monkeypatch.setattr(GameHub, "setup_parsers", lambda n: None)
        g = GameHub()
        assert g.apply_bound(x, lower, upper) == expected

    def test_parse_arguments_snake(self, monkeypatch) -> None:
        """
        Test the parsing of the command line arguments for the Snake game.
        """
        monkeypatch.setattr("sys.argv", ["gamehub", "snake","--difficulty", "Easy"])
        g = GameHub()
        assert g.args.game == "snake" and g.args.difficulty == "Easy"

    def test_parse_arguments_gof(self, monkeypatch) -> None:
        """
        Test the parsing of the command line arguments for the Game of Life.
        """
        monkeypatch.setattr("sys.argv",
                            ["gamehub", "game_of_life",
                             "--speed", "100",
                             "--mode", "Automatic",
                             "--density", "40"])
        g = GameHub()
        assert g.args.game == "game_of_life" and g.args.speed == 100 and g.args.mode == "Automatic" and g.args.density == 40

    def test_parse_arguments_word_guesser(self, monkeypatch) -> None:
        """
        Test the parsing of the command line arguments for the Word Guesser game.
        """
        monkeypatch.setattr("sys.argv", ["gamehub", "word_guesser"])
        g = GameHub()
        assert g.args.game == "word_guesser"

    def test_parse_arguments_chess(self, monkeypatch) -> None:
        """
        Test the parsing of the command line arguments for Chess.
        """
        monkeypatch.setattr("sys.argv", ["gamehub", "chess", "--mode", "Singleplayer"])
        g = GameHub()
        assert g.args.game == "chess" and g.args.mode == "Singleplayer"
