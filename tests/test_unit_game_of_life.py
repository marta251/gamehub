"""
This module contains the class TestGameOfLife that implements
the unit tests for the GameOfLife class.
"""
import pytest # type: ignore
from gamehub.game_of_life import GameOfLife
from hypothesis import given, strategies, settings # type: ignore

class TestGameOfLife:
    """
    This class contains the unit tests for the GameOfLife class.
    """
    def test_constructor_default(self) -> None:
        """
        Test that verifies that the constructor called without arguments
        always sets the attributes to the default values.
        """
        game_of_life = GameOfLife()
        assert (
            game_of_life.speed == 100
            and game_of_life.mode == "Automatic"
            and game_of_life.density == 30
        )

    @given(strategies.integers(min_value=50, max_value=1000))
    @settings(max_examples=5)
    def test_property_constructor_delta_time(self, speed : int) -> None:
        """
        Tst that verifies that the constructor always correctly sets
        the delta_time attribute equal to speed / 1000.
        """
        game_of_life = GameOfLife(speed)
        assert game_of_life.delta_time == speed / 1000

    @given(
        strategies.integers(min_value=3, max_value=20),
        strategies.integers(min_value=3, max_value=20)
        )
    @settings(max_examples=5)
    def test_property_initialize_matrix_dimension(self, rows : int, cols : int) -> None:
        """
        Test that verifies that the dimensions of the initialized matrix
        always match the input values.
        """
        game_of_life = GameOfLife()
        matrix = game_of_life.initialize_matrix(rows, cols, 10)
        assert len(matrix) == rows and len(matrix[0]) == cols

    @given(
        strategies.integers(min_value=3, max_value=20),
        strategies.integers(min_value=3, max_value=20)
        )
    @settings(max_examples=5)
    def test_property_initialize_matrix_values(self, rows : int, cols : int) -> None:
        """
        Test that verifies that the values of the initialized
        matrix are always 0 or 1.
        """
        game_of_life = GameOfLife()
        matrix =  game_of_life.initialize_matrix(rows, cols, 10)
        all_ones_or_zeros = all([elem == 0 or elem == 1 for row in matrix for elem in row])
        assert all_ones_or_zeros

    @pytest.mark.parametrize("matrix, expected",
        [([[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
        ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
        ([[0, 1, 1], [1, 0, 1], [0, 1, 0]], [[0, 1, 1], [1, 0, 1], [0, 1, 0]]),
        ([[0, 1, 0], [1, 0, 1], [1, 0, 1], [0, 1, 0]], [[0, 1, 0], [1, 0, 1], [1, 0, 1], [0, 1, 0]])])
    def test_update_matrix (self, matrix : list[list[int]], expected : list[list[int]]) -> None:
        """
        Test that verifies that the update_matrix method correctly updates the matrix
        based on the rules of the game of life.
        """
        game_of_life = GameOfLife()
        assert game_of_life.update_matrix(matrix) == expected

    @given(
        strategies.lists(
            strategies.lists(
                strategies.integers(min_value=0, max_value=1),
                min_size=7, max_size=7),
            min_size=7, max_size=7)
        )
    @settings(max_examples=5)
    def test_property_update_matrix_dimension(self, matrix : list[list[int]]) -> None:
        """
        Test that verifies that the dimensions of the updated matrix
        are the same as the input matrix.
        """
        game_of_life = GameOfLife()
        new_matrix =  game_of_life.update_matrix(matrix)
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
        """
        Test that verifies that the values of the updated matrix are all 0s or 1s.
        """
        game_of_life = GameOfLife()
        new_matrix = game_of_life.update_matrix(matrix)
        all_ones_or_zeros = all([elem == 0 or elem == 1 for row in new_matrix for elem in row])
        assert all_ones_or_zeros

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
        """
        Test that verifies that the count_live_neighbors method correctly counts
        """
        game_of_life = GameOfLife()
        assert game_of_life.count_live_neighbors(matrix, row, col) == expected

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
        """
        Test that verifies that the count_live_neighbors method always
        returns a value between 0 and 8.
        """
        game_of_life = GameOfLife()
        count = game_of_life.count_live_neighbors(matrix, row, col)
        assert count >= 0 and count <= 8

    def test_gameloop(self, monkeypatch) -> None:
        """
        Test that verifies that the gameloop works correctly.
        Mock the user input, the functions dedicated to the drawing of the board
        and the initialization of the matrix to have a known state.
        We check that after two iterations the matrix is updated correctly.
        """
        def key_input_factory():
            inputs = ["a", "\x1b"]
            for input in inputs:
                yield input

        key_input_generator = key_input_factory()

        def get_next_input(self, *args):
            return next(key_input_generator)

        def mock_initialize_matrix(self, *args):
            return [[0, 1, 0, 0, 1],
                    [1, 1, 0, 1, 0],
                    [1, 1, 1, 0, 0]]

        def mock_init_curse(self, *args):
            return None, 3, 6

        monkeypatch.setattr(GameOfLife, "get_input_and_sleep", get_next_input)
        monkeypatch.setattr(GameOfLife, "init_curses", mock_init_curse)
        monkeypatch.setattr(GameOfLife, "draw_board", lambda *args: None)
        monkeypatch.setattr(GameOfLife, "initialize_matrix", mock_initialize_matrix)

        game_of_life = GameOfLife()
        game_of_life.gameloop(None)

        # 1st iteration
        # assert g.matrix == [[1, 1, 1, 0, 0],
        #                     [0, 0, 0, 1, 0],
        #                     [1, 0, 1, 0, 0]]
        # 2nd iteration
        assert game_of_life.matrix == [[0, 1, 1, 0, 0],
                            [1, 0, 0, 1, 0],
                            [0, 0, 0, 0, 0]]
