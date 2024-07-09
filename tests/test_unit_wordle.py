import pytest  # type: ignore
import gamehub.wordle as wordle

class TestWordle:
    @pytest.mark.parametrize("new_guessed, to_guess, alphabet, old_guessed, expected",
                             [("apple","think", ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'], "_____",
                               (['_','_','_','_','_'], ['b','c','d','f','g','h','i','j','k','m','n','o','q','r','s','t','u','v','w','x','y','z'])),

                              ("about","apple", ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'], "_____",
                               (['a','_','_','_','_'], ['a','c','d','e','f','g','h','i','j','k','l','m','n','p','q','r','s','v','w','x','y','z'])),

                              ("adobe","about", ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'], "_____",
                               (['a','b','o','_','_'], ['a','b','c','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']))])
    def test_generate_updated_guess(self, new_guessed : str, to_guess : str, alphabet : list, old_guessed : str, expected : tuple) -> None:
        w = wordle.Wordle()
        assert w.generate_updated_guess(new_guessed, to_guess, alphabet, old_guessed) == expected