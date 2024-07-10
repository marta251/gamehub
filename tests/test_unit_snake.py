from collections import deque
import pytest # type: ignore
import gamehub.snake as snake
from hypothesis import given, strategies, settings # type: ignore
from hypothesis.strategies import composite, integers # type: ignore

class TestSnake:
    @pytest.mark.parametrize("key, current_direction, expected",
                             [("KEY_UP", "DOWN", "DOWN"),
                                ("KEY_DOWN", "RIGHT", "DOWN"),
                                ("KEY_LEFT", "UP", "LEFT"),
                                ("KEY_DOWN", "DOWN", "DOWN"),
                                ("KEY_RIGHT", "LEFT", "LEFT")])
    def test_calcule_direction(self, key : str, current_direction : str, expected : str) -> None:
        snake_t = snake.Snake()
        assert snake_t.calcule_direction(current_direction, key) == expected

    @pytest.mark.parametrize("y, x, direction, SNAKE_BOUNDS, expected",
                             [(1, 2, "UP", (1, 10, 2, 20), (1, 2)),
                              (1, 2, "RIGHT", (1, 10, 2, 20), (1, 4)),
                              (10, 10, "DOWN", (1, 10, 2, 20), (10, 10)),
                              (9, 8, "LEFT", (1, 10, 2, 20), (9, 6)),
                              (5, 4, "UP", (1, 10, 2, 20), (4,4))])
    def test_calculate_new_position(self, y : int, x : int, direction : str, SNAKE_BOUNDS : tuple[int, int, int, int], expected : tuple[int, int]) -> None:
        s= snake.Snake()
        assert s.calcule_new_position(y, x, direction, SNAKE_BOUNDS) == expected

    
    @composite
    def smaller_than_y(draw) -> tuple[int, int]:
        a = draw(integers(min_value=1))
        b = draw(integers(min_value=a))
        return a, b
    @composite
    def smaller_than_x(draw) -> tuple[int, int]:
        a = draw(integers(min_value=2)) * 2
        b = draw(integers(min_value=a)) * 2
        return a, b
    @given(strategies.tuples(
            smaller_than_y(),
            smaller_than_x(),
            strategies.just("UP") |
            strategies.just("DOWN") |
            strategies.just("LEFT") |
            strategies.just("RIGHT")))
    @settings(max_examples=20)
    def test_property_calcule_new_position_always_inside(self,t : tuple[tuple[int, int], tuple[int, int], str]) -> None:
        s = snake.Snake()
        SNAKE_BOUNDS = (1, t[0][1], 2, t[1][1])
        res_y, res_x = s.calcule_new_position(t[0][0],t[1][0],t[2],SNAKE_BOUNDS)
        assert res_y >= SNAKE_BOUNDS[0] and res_y <= SNAKE_BOUNDS[1] and res_x >= SNAKE_BOUNDS[2] and res_x <= SNAKE_BOUNDS[3] and res_x % 2 == 0
    
        
    @pytest.mark.parametrize("body, SNAKE_BOUNDS",
                             [   ([(0, 0), (0, 2), (0, 4)], (1, 5, 2, 10)),
                                 ([(0, 0), (0, 2), (0, 4)], (1, 5, 2, 10)),
                                 ([(2, 2), (3, 2), (3, 4)], (1, 5, 2, 10)),
                                 ([(2, 2), (3, 2), (3, 4)], (1, 5, 2, 10))])
    def test_new_food_coordinates(self, body : deque[tuple[int, int]], SNAKE_BOUNDS : tuple[int, int, int, int]):
        s = snake.Snake()
        (y, x) = s.new_food_coordinates(body, SNAKE_BOUNDS)
        assert (y, x) not in body

    @given(strategies.tuples(
        strategies.integers(min_value=10),
        strategies.integers(min_value=20)
        ))
    @settings(max_examples=10)
    def test_property_new_food_coordinates_always_inside(self,t : tuple[int, int]):
        s = snake.Snake()
        SNAKE_BOUNDS = (1, t[0], 2, t[1])
        (y, x) = s.new_food_coordinates([], SNAKE_BOUNDS)
        assert y >= SNAKE_BOUNDS[0] and y <= SNAKE_BOUNDS[1] and x >= SNAKE_BOUNDS[2] and x <= SNAKE_BOUNDS[3] and x % 2 == 0

    @pytest.mark.parametrize("body, y_food, x_food, expected",
                             [  ([(0, 0), (0, 2), (0, 4)], 0, 6, False),
                                ([(0, 0), (0, 2), (0, 4)], 0, 4, True),
                                ([(4, 6), (5, 6)], 12, 2, False),
                                 ([(4, 6), (5, 6)], 5, 6, True) ])
    def test_check_food_eaten(self, body : deque[tuple[int, int]], y_food : int, x_food : int, expected : bool):
        s = snake.Snake()
        assert s.check_food_eaten(body, y_food, x_food) == expected
    
    @pytest.mark.parametrize("body, expected",
                             [  ([(0, 0), (0, 2), (0, 4)], False),
                                ([(0, 0), (0, 2), (0, 4), (1,4), (1,2), (0,2)], True),
                                ([(9, 6), (10, 6), (11, 6)], False),
                                ([(9, 6), (10, 6), (10, 4), (9,4), (9,6)], True) ])
    def test_verify_collision(self, body : deque[tuple[int, int]], expected : bool):
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