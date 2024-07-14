import pytest # type: ignore
from gamehub.game_of_life import GameOfLife
from hypothesis import given, strategies, settings # type: ignore

class TestGameOfLife:
    def test_constructor_default(self) -> None:
        g = GameOfLife()
        assert g.speed == 100 and g.mode == "Automatic" and g.density == 30
    
    @given(strategies.integers(min_value=50, max_value=1000))
    @settings(max_examples=5)
    def test_property_constructor_delta_time(self, speed : int) -> None:
        g = GameOfLife(speed)
        assert g.delta_time == speed / 1000

    @given(
        strategies.integers(min_value=3, max_value=20),
        strategies.integers(min_value=3, max_value=20)
        )
    @settings(max_examples=5)
    def test_property_initialize_matrix_dimension(self, rows : int, cols : int) -> None:
        g = GameOfLife()
        matrix = g.initialize_matrix(rows, cols, 10)
        assert len(matrix) == rows and len(matrix[0]) == cols
        
    @given(
        strategies.integers(min_value=3, max_value=20),
        strategies.integers(min_value=3, max_value=20)
        )
    @settings(max_examples=5)
    def test_property_initialize_matrix_values(self, rows : int, cols : int) -> None:
        g = GameOfLife()
        matrix =  g.initialize_matrix(rows, cols, 10)
        all_ones_or_zeros = all([elem == 0 or elem == 1 for row in matrix for elem in row])
        assert all_ones_or_zeros

    @pytest.mark.parametrize("matrix, expected",
                                [([[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
                                ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
                                ([[0, 1, 1], [1, 0, 1], [0, 1, 0]], [[0, 1, 1], [1, 0, 1], [0, 1, 0]]),
                                ([[0, 1, 0], [1, 0, 1], [1, 0, 1], [0, 1, 0]], [[0, 1, 0], [1, 0, 1], [1, 0, 1], [0, 1, 0]])])                       
    def test_update_matrix (self, matrix : list[list[int]], expected : list[list[int]]) -> None:
        g = GameOfLife()
        assert g.update_matrix(matrix) == expected

    @given(
        strategies.lists(
            strategies.lists(
                strategies.integers(min_value=0, max_value=1),
                min_size=7, max_size=7),
            min_size=7, max_size=7)
        )
    @settings(max_examples=5)
    def test_property_update_matrix_dimension(self, matrix : list[list[int]]) -> None:
        g = GameOfLife()
        new_matrix =  g.update_matrix(matrix)
        assert len(new_matrix) == len(matrix) and len(new_matrix[0]) == len(matrix[0])
        
    @given(
        strategies.lists(
            strategies.lists(
                strategies.integers(min_value=0, max_value=1),
                min_size=7, max_size=7),
            min_size=7, max_size=7)
        )
    @settings(max_examples=5)
    def test_property_update_matrix_values(self, matrix : list[list[int]]) -> None:
        g = GameOfLife()
        new_matrix = g.update_matrix(matrix)    
        all_ones_or_zeros = all([elem == 0 or elem == 1 for row in new_matrix for elem in row])
        assert all_ones_or_zeros

    @given(
        strategies.lists(
            strategies.lists(
                strategies.integers(min_value=0, max_value=1), min_size=6, max_size=6),
                min_size=6, max_size=6))
    @settings(max_examples=5)
    def test_property_count_live_neighbors_values(self, matrix : list[list[int]]) -> None:
        g = GameOfLife()
        all_count_between_0_and_8 = all([g.count_live_neighbors(matrix, row, col) >= 0 and g.count_live_neighbors(matrix, row, col) <= 8 for row in range(len(matrix)) for col in range(len(matrix[0]))])
        assert all_count_between_0_and_8

    @pytest.mark.parametrize("matrix, row, col, expected",
                                [([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0, 0, 0),
                                ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 1, 1, 0),
                                ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], 2, 2, 3),
                                ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], 1, 1, 8),                               
                                ([[0, 1, 1], [1, 0, 1], [0, 1, 0]], 1, 0, 2),
                                ([[0, 1, 1], [1, 0, 1], [0, 1, 0]], 1, 1, 5)])                            
    def test_count_live_neighbors(self,
                                  matrix : list[list[int]],
                                  row : int,
                                  col : int,
                                  expected : int) -> None:
        g = GameOfLife()
        assert g.count_live_neighbors(matrix, row, col) == expected

    @given(
        strategies.lists(
            strategies.lists(
                strategies.integers(min_value=0, max_value=1),
                min_size=7, max_size=7),
            min_size=7, max_size=7),
        strategies.integers(min_value=0, max_value=6),
        strategies.integers(min_value=0, max_value=6)
        )
    @settings(max_examples=5)
    def test_property_count_live_neighbors_bounds(self,
                                         matrix : list[list[int]],
                                         row : int,
                                         col : int) -> None:
        g = GameOfLife()
        count = g.count_live_neighbors(matrix, row, col)
        assert count >= 0 and count <= 8

    def test_gameloop(self, monkeypatch) -> None:
        def key_input_factory():
            inputs = ["a", "\x1b"]
            for input in inputs:
                yield input

        key_input_generator = key_input_factory()
    
        def get_next_food_coordinates(self, *args):
            return next(key_input_generator)

        def mock_initialize_matrix(self, *args):
            return [[0, 1, 0, 0, 1], 
                    [1, 1, 0, 1, 0], 
                    [1, 1, 1, 0, 0]]
        
        def mock_init_curse(self, *args):
            return None, 3, 6

        monkeypatch.setattr(GameOfLife, "get_input_and_sleep", get_next_food_coordinates)
        monkeypatch.setattr(GameOfLife, "init_curses", mock_init_curse)
        monkeypatch.setattr(GameOfLife, "draw_board", lambda *args: None)
        monkeypatch.setattr(GameOfLife, "initialize_matrix", mock_initialize_matrix)

        g = GameOfLife()
        g.gameloop(None)

        # 1st iteration
        # assert g.matrix == [[1, 1, 1, 0, 0], 
        #                     [0, 0, 0, 1, 0], 
        #                     [1, 0, 1, 0, 0]]
        # 2nd iteration
        assert g.matrix == [[0, 1, 1, 0, 0], 
                            [1, 0, 0, 1, 0], 
                            [0, 0, 0, 0, 0]]
