import pytest # type: ignore
import gamehub.game_of_life as game_of_life
from hypothesis import given, strategies, settings # type: ignore

class TestGameOfLife:

    @given(
        strategies.integers(min_value=3, max_value=20),
        strategies.integers(min_value=3, max_value=20)
        )
    @settings(max_examples=5)
    def test_initialize_matrix_dimension(self, rows : int, cols : int):
        g = game_of_life.GameOfLife()
        matrix =  g.initialize_matrix(rows, cols, 10)
        assert len(matrix) == rows and len(matrix[0]) == cols
        
    @given(
        strategies.integers(min_value=3, max_value=20),
        strategies.integers(min_value=3, max_value=20)
        )
    @settings(max_examples=5)
    def test_initialize_matrix_values(self, rows : int, cols : int):
        g = game_of_life.GameOfLife()
        matrix =  g.initialize_matrix(rows, cols, 10)
        all_ones_or_zeros = all([elem == 0 or elem == 1 for row in matrix for elem in row])
        assert all_ones_or_zeros


    @pytest.mark.parametrize("matrix, expected",
                                [([[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
                                ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
                                ([[0, 1, 1], [1, 0, 1], [0, 1, 0]], [[0, 1, 1], [1, 0, 1], [0, 1, 0]]),
                                ([[0, 1, 0], [1, 0, 1], [1, 0, 1], [0, 1, 0]], [[0, 1, 0], [1, 0, 1], [1, 0, 1], [0, 1, 0]])])
                             
    def test_update_matrix (self, matrix : list[list[int]], expected : list[list[int]]):
        g = game_of_life.GameOfLife()
        assert g.update_matrix(matrix) == expected


    @given(
        strategies.lists(
            strategies.lists(
                strategies.integers(min_value=0, max_value=1),
                min_size=7, max_size=7),
            min_size=7, max_size=7)
        )
    @settings(max_examples=5)
    def test_update_matrix_dimension(self, matrix : list[list[int]]):
        g = game_of_life.GameOfLife()
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
    def test_update_matrix_values(self, matrix : list[list[int]]):
        g = game_of_life.GameOfLife()
        new_matrix =  g.update_matrix(matrix)        
        all_ones_or_zeros = all([elem == 0 or elem == 1 for row in new_matrix for elem in row])
        assert all_ones_or_zeros

    @pytest.mark.parametrize("matrix, row, col, expected",
                                [([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0, 0, 0),
                                ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 1, 1, 0),
                                ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], 2, 2, 3),
                                ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], 1, 1, 8),                               
                                ([[0, 1, 1], [1, 0, 1], [0, 1, 0]], 1, 0, 2),
                                ([[0, 1, 1], [1, 0, 1], [0, 1, 0]], 1, 1, 5)                                  
                                ])                            
    def test_count_live_neighbors(self, matrix : list[list[int]], row : int, col : int, expected : int):
        g = game_of_life.GameOfLife()
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
    def test_count_live_neighbors_bounds(self, matrix : list[list[int]], row : int, col : int):
        g = game_of_life.GameOfLife()
        count = g.count_live_neighbors(matrix, row, col)
        assert count >= 0 and count <= 8