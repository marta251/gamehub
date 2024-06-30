import pytest
from game import snake
class TestSnake:
    @pytest.mark.parametrize("key, current_direction, expected",
                             [("KEY_UP", "DOWN", "UP"),
                                ("KEY_DOWN", "RIGHT", "DOWN"),
                                ("KEY_LEFT", "UP", "LEFT"),
                                ("KEY_DOWN", "DOWN", "DOWN")])
    def test_calcule_direction(self, key, current_direction, expected):
        snake = snake.Snake()
        assert snake.calcule_direction(current_direction, key) == expected
