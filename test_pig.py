import unittest
from pig import Die
from pig import Match
from pig import Player
from unittest.mock import patch

class TestDie(unittest.TestCase):

    def test_init(self):
        sides = 6
        d6 = Die(sides)
        assert d6.sides == sides

    def test_roll(self):
        sides = 6
        d6 = Die(sides)
        output = d6.roll()
        assert type(output) == int
        assert 1 <= output <= sides


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.p1 = Player(1)

    def test_init(self):
        assert self.p1.id
        assert type(self.p1.id) is int
        assert self.p1.score == 0

    def test_bust(self):
        self.p1.score = 100
        self.p1.bust_score()
        assert self.p1.score == 0

    def test_tally(self):
        original_score = 35
        self.p1.score = original_score
        dice = [3, 5]
        self.p1.tally_score(dice)
        supposed_score = original_score + sum(dice)
        assert self.p1.score == supposed_score


class TestMatch(unittest.TestCase):

    def setUp(self):
        # create match with 3 players
        self.player_count = 3
        self.match = Match(self.player_count)
        self.winner = Player(1)
        self.winner.score = 100
        self.loser = Player(2)
        self.loser.score = 0

    def test_init(self):
        assert len(self.match.players) == self.player_count
        assert self.match.over is False
        assert type(self.match.dice) == list

    def test_invalid(self):
        with self.assertRaises(ValueError):
            Match(100)
        with self.assertRaises(ValueError):
            Match(0)

    def test_winner(self):
        winner = self.match.winner(self.winner)
        assert winner is True
        loser = self.match.winner(self.loser)
        assert loser is False

    def test_roll_dice(self):
        dice = self.match.roll_dice(self.loser)
        assert type(dice) == list

    def test_roll_evaluations(self):
        result = Match.evaluate_roll([1, 1], self.winner)
        assert result[0] == 0
        assert result[1] == False

        result = Match.evaluate_roll([1, 3], self.winner)
        assert result[0] == 0
        assert result[1] == False

        result = Match.evaluate_roll([3, 3], self.winner)
        assert result[0] == 1
        assert result[1] == True

        result = Match.evaluate_roll([6, 5], self.winner)
        assert result[0] == 1
        assert result[1] == False

    def test_next_turn(self):
        result = Match.next_turn()
        assert result[0] == 0
        assert result[1] == False

    @patch('pig.Match.get_option_input', return_value='0')
    def test_pass_turn_option(self, mock):
        output = self.match.turn_options(self.winner)
        assert output == 0

    @patch('pig.Match.get_option_input', return_value='1')
    def test_roll_option(self, mock):
        output = self.match.turn_options(self.winner)
        assert output == 1

    def test_invalid_option(self):
        invalid_option = '5'
        result = self.match.valid_option(invalid_option)
        assert result == False


if __name__ == '__main__':
    unittest.main()
