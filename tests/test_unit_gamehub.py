import pytest # type: ignore
import gamehub.gamehub as gamehub
from hypothesis import given, strategies, settings # type: ignore
from hypothesis.strategies import composite # type: ignore

class TestGameHub:
    @composite
    def smaller_than(draw) -> tuple[int, int]:
        a = draw(strategies.integers())
        b = draw(strategies.integers(min_value=a))
        return a, b
    @given(strategies.integers(), smaller_than())
    @settings(max_examples=20)
    def test_apply_bound_range(self, x : int, bounds : tuple[int, int]) -> None:
        g = gamehub.GameHub()
        res = g.apply_bound(x, bounds[0], bounds[1])
        assert bounds[0] <= res and res <= bounds[1]

    @pytest.mark.parametrize("x, lower, upper, expected",
                             [(1, 0, 2, 1),
                              (0, 0, 2, 0),
                              (2, 0, 2, 2),
                              (3, 0, 2, 2)])
    def test_apply_bound(self, x : int, lower : int, upper : int, expected : int) -> None:
        g = gamehub.GameHub()
        assert g.apply_bound(x, lower, upper) == expected
    