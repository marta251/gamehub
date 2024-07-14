import string
import pytest # type: ignore
from gamehub.word_guesser import WordGuesser

class TestWordGuesser:
    def test_constructor(self) -> None:
        w = WordGuesser()
        assert isinstance(w, WordGuesser)

    @pytest.mark.parametrize("new_guessed, to_guess, alphabet, old_guessed, expected",
                             [("apple","think", ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'], "_____",
                               (['_','_','_','_','_'], ['b','c','d','f','g','h','i','j','k','m','n','o','q','r','s','t','u','v','w','x','y','z'])),

                              ("about","apple", ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'], "_____",
                               (['a','_','_','_','_'], ['a','c','d','e','f','g','h','i','j','k','l','m','n','p','q','r','s','v','w','x','y','z'])),

                              ("adobe","about", ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'], "_____",
                               (['a','b','o','_','_'], ['a','b','c','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']))])
    def test_generate_updated_guess(self,
                                    new_guessed : str,
                                    to_guess : str,
                                    alphabet : list,
                                    old_guessed : str,
                                    expected : tuple) -> None:
        w = WordGuesser()
        assert w.generate_updated_guess(new_guessed, to_guess, alphabet, old_guessed) == expected

    # With the following method we are going to test the gameloop
    # The user inserts the following words: apple (not the target word but a valid one),
    # aboud (an invalid word) and think (the target word)
    def test_gameloop_win(self, monkeypatch) -> None:
        def mock_inizialize_game(*args):
            return ["think", "apple", "about"], "think", ["_", "_", "_", "_", "_"], 6, list(string.ascii_lowercase), False
        
        def input_factory():
            inputs = ["a","p","p","l","e","\n",
                      "a","b","o","u","d","\n",
                      "t","h","u","\x7f","i","n","k","\n"]
            for i in inputs:
                yield i

        input_gen = input_factory()

        def get_next_input(*args):
            return next(input_gen)
        
        monkeypatch.setattr(WordGuesser, "check_terminal_size", lambda *args: True)
        monkeypatch.setattr(WordGuesser, "initialize_game", mock_inizialize_game)
        monkeypatch.setattr(WordGuesser, "draw_inserted_word", lambda *args: None)
        monkeypatch.setattr(WordGuesser, "get_key", get_next_input)
        monkeypatch.setattr(WordGuesser, "draw_after_invalid_input", lambda *args: None)
        monkeypatch.setattr(WordGuesser, "draw_after_update", lambda *args: None)
        monkeypatch.setattr(WordGuesser, "draw_winning_message", lambda *args: None)
        monkeypatch.setattr(WordGuesser, "draw_losing_message", lambda *args: None)

        w = WordGuesser()
        w.gameloop(None)
        assert w.won is True

    # With the following method we are going to test the gameloop when the user looses
    def test_gameloop_loose(self, monkeypatch) -> None:
        def mock_inizialize_game(*args):
            return ["think", "apple", "about", "shark", "beach", "chair"], "table", ["_", "_", "_", "_", "_"], 6, list(string.ascii_lowercase), False
        
        def input_factory():
            inputs = ["t","h","i","n","k","\n",
                      "a","p","p","l","e","\n",
                      "a","b","o","u","t","\n",
                      "s","h","a","r","k","\n",
                      "b","e","a","c","h","\n",
                      "c","h","a","i","r","\n"]
            for i in inputs:
                yield i

        input_gen = input_factory()

        def get_next_input(*args):
            return next(input_gen)
        
        monkeypatch.setattr(WordGuesser, "check_terminal_size", lambda *args: True)
        monkeypatch.setattr(WordGuesser, "initialize_game", mock_inizialize_game)
        monkeypatch.setattr(WordGuesser, "draw_inserted_word", lambda *args: None)
        monkeypatch.setattr(WordGuesser, "get_key", get_next_input)
        monkeypatch.setattr(WordGuesser, "draw_after_invalid_input", lambda *args: None)
        monkeypatch.setattr(WordGuesser, "draw_after_update", lambda *args: None)
        monkeypatch.setattr(WordGuesser, "draw_winning_message", lambda *args: None)
        monkeypatch.setattr(WordGuesser, "draw_losing_message", lambda *args: None)

        w = WordGuesser()
        w.gameloop(None)
        assert w.won is False
