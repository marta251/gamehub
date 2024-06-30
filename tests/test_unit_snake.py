import pytest
import gamehub.snake as snake

class TestSnake:
    @pytest.mark.parametrize("key, current_direction, expected",
                             [("KEY_UP", "DOWN", "DOWN"),
                                ("KEY_DOWN", "RIGHT", "DOWN"),
                                ("KEY_LEFT", "UP", "LEFT"),
                                ("KEY_DOWN", "DOWN", "DOWN")])
    def test_calcule_direction(self, key, current_direction, expected):
        snake_t = snake.Snake()
        assert snake_t.calcule_direction(current_direction, key) == expected
