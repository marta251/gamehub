import pytest # type: ignore
import gamehub.snake as snake
from hypothesis import given, strategies, settings
from hypothesis.strategies import composite, integers


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

    @composite
    def smaller_than(draw):
        a = draw(integers(min_value=0))
        b = draw(integers(min_value=a))
        return a, b

    @given(strategies.tuples(
            smaller_than(),
            smaller_than(),
            strategies.just("UP") |
            strategies.just("DOWN") |
            strategies.just("LEFT") |
            strategies.just("RIGHT")))
    @settings(max_examples=20)
    def test_property_calcule_new_position_always_inside(self,t):
        s = snake.Snake()
        res_y, res_x = s.calcule_new_position(t[0][0],t[1][0],t[2],t[0][1],t[1][1])
        assert res_y <= t[0][1] and res_x <= t[1][1]
        
    @pytest.mark.parametrize("ROWS, COLS, body",
                             [   (5, 5, [(0, 0), (0, 2), (0, 4)]),
                                 (5, 5, [(0, 0), (0, 2), (0, 4)]),
                                 (5, 5, [(2, 2), (3, 2), (3, 4)]),
                                 (5, 5, [(2, 2), (3, 2), (3, 4)])])
    def test_new_food_coordinates(self, ROWS, COLS, body):
        s = snake.Snake()
        (y, x) = s.new_food_coordinates(ROWS, COLS, body)
        assert (y, x) not in body

    @given(strategies.tuples(
        strategies.integers(min_value=0),
        strategies.integers(min_value=0)))
    @settings(max_examples=10)
    def test_property_new_food_coordinates_always_inside(self,t):
        s = snake.Snake()
        (y, x) = s.new_food_coordinates(t[0], t[1], [])
        assert y <= t[0] and x <= t[1] and x % 2 == 0

    @pytest.mark.parametrize("body, y_food, x_food, expected",
                             [  ([(0, 0), (0, 2), (0, 4)], 0, 6, False),
                                ([(0, 0), (0, 2), (0, 4)], 0, 4, True),
                                ([(4, 6), (5, 6)], 12, 2, False),
                                 ([(4, 6), (5, 6)], 5, 6, True) ])
    def test_check_food_eaten(self, body, y_food, x_food, expected):
        s = snake.Snake()
        assert s.check_food_eaten(body, y_food, x_food) == expected
    
    @pytest.mark.parametrize("body, expected",
                             [  ([(0, 0), (0, 2), (0, 4)], False),
                                ([(0, 0), (0, 2), (0, 4), (1,4), (1,2), (0,2)], True),
                                ([(9, 6), (10, 6), (11, 6)], False),
                                ([(9, 6), (10, 6), (10, 4), (9,4), (9,6)], True) ])
    def test_verify_collision(self, body, expected):
        s = snake.Snake()
        assert s.verify_collision(body) == expected

    #TODO: Try property based testing for verify_collision (the last element of the snake should not be in the rest of the snake)
    '''
    @composite
    def random_snake(draw):
        a = draw(integers(min_value=0, max_value=100))
        b = draw(integers(min_value=0, max_value=100)) * 2
        snake = [(a,b)]
        while len(snake) < 5:
            rand = random.randint(0, 3)
            if rand == 0:
                a -= 1
            elif rand == 1:
                a += 1
            elif rand == 2:
                b -= 2
            else:
                b += 2
            snake.append((a,b))
            
        return a, b
        '''