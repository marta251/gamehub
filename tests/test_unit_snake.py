import pytest # type: ignore
import gamehub.snake as snake
from hypothesis import given, strategies, assume, settings

class TestSnake:
    @pytest.mark.parametrize("key, current_direction, expected",
                             [("KEY_UP", "DOWN", "DOWN"),
                                ("KEY_DOWN", "RIGHT", "DOWN"),
                                ("KEY_LEFT", "UP", "LEFT"),
                                ("KEY_DOWN", "DOWN", "DOWN"),
                                ("KEY_RIGHT", "LEFT", "LEFT")])
    def test_calcule_direction(self, key, current_direction, expected):
        snake_t = snake.Snake()
        assert snake_t.calcule_direction(current_direction, key) == expected


    @pytest.mark.parametrize("y, x, direction, ROWS, COLS, expected",
                             [(0, 0, "UP", 10, 10, (0, 0)),
                              (0, 0, "RIGHT", 10, 10, (0, 2)),
                              (10, 10, "DOWN", 10, 10, (10, 10)),
                              (9, 9, "LEFT", 10, 10, (9, 7)),
                              (5, 5, "UP", 10, 10, (4,5))])
    def test_calculate_new_position(self, y, x, direction, ROWS, COLS, expected):
        s= snake.Snake()
        assert s.calcule_new_position(y, x, direction, ROWS, COLS) == expected

    @given(strategies.tuples(
            strategies.integers(min_value=0),
            strategies.integers(min_value=0),
            strategies.just("UP") |
            strategies.just("DOWN") |
            strategies.just("LEFT") |
            strategies.just("RIGHT"),
            strategies.integers(min_value=0),
            strategies.integers(min_value=0)))
    
    @settings(max_examples=20)
    def test_property_calcule_new_position_always_inside(self,t):
        assume(t[0] < t[3])
        assume(t[1] < t[4])
        s = snake.Snake()
        res_y, res_x = s.calcule_new_position(t[0],t[1],t[2],t[3],t[4])
        assert res_y < t[3] and res_x < t[4]