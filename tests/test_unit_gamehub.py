import pytest # type: ignore
from gamehub.gamehub import GameHub
from hypothesis import given, strategies, settings, HealthCheck # type: ignore
from hypothesis.strategies import composite # type: ignore

class TestGameHub:       
    @composite
    def smaller_than(draw) -> tuple[int, int]:
        a = draw(strategies.integers())
        b = draw(strategies.integers(min_value=a))
        return a, b
    @given(strategies.integers(), smaller_than())
    @settings(max_examples=20, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_apply_bound_range(self, monkeypatch, x : int, bounds : tuple[int, int]) -> None:
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
        monkeypatch.setattr(GameHub, "setup_parsers", lambda n: None)
        g = GameHub()
        assert g.apply_bound(x, lower, upper) == expected
