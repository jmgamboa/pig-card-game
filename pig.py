import random

WINNING_SCORE = 100
BUST_VAL = 1
MAX_PLAYERS = 6
GAME_RESULTS = []
TURN_OPTIONS = ['0', '1']

class Die:

    def __init__(self, sides: int):
        self.sides = sides

    def roll(self) -> int:
        number = random.randint(1, self.sides)
        return number


class Player:

    def __init__(self, pid: int):
        self.id = pid
        self.score = 0

    def bust_score(self) -> None:
        print(f"Player {self.id} busted")
        self.score = 0

    def tally_score(self, dice: list) -> None:
        self.score += sum(dice)
        print(f"Player {self.id} score is {self.score}")


class Match:

    def __init__(self, player_count: int):
        self.players = []
        self.validate_player_count(player_count)
        self.create_players(player_count)
        self.over = False
        self.dice = [Die(6), Die(6)]

    def validate_player_count(self, player_count: int) -> None:
        if player_count < 2 or player_count > MAX_PLAYERS:
            raise ValueError(
                "Requires at least 2 and most {MAX_PLAYERS} players"
            )

    def create_players(self, player_count: int) -> None:
        for i in range(player_count):
            self.players.append(Player(i))

    def winner(self, player: Player) -> bool:
        if player.score >= WINNING_SCORE:
            print(f"Player {player.id} is the winner")
            self.over = True
            GAME_RESULTS.append(self)
            return True
        else:
            return False

    def roll_dice(self, player: Player) -> list:
        dice_values = []
        for die in self.dice:
            dice_values.append(die.roll())
        print(
            f"Player {player.id} rolled {dice_values[0]} & {dice_values[1]}"
        )
        return dice_values

    @staticmethod
    def evaluate_roll(dice: list, player: Player) -> tuple:
        """Tuple returns first the turn flag and then the
        must roll flag
        """
        if BUST_VAL == dice[0] \
                and BUST_VAL == dice[1]:
            player.bust_score()
            return Match.next_turn()
        elif BUST_VAL in dice:
            return Match.next_turn()
        elif dice[0] == dice[1]:
            must_roll = True
            player.tally_score(dice)
            return 1, must_roll
        else:
            player.tally_score(dice)
            must_roll = False
            return 1, must_roll

    @staticmethod
    def next_turn() -> tuple:
        return 0, False

    def turn_options(self, player: Player) -> int:
        print(f"Player {player.id}s turn")
        valid = False
        while not valid:
            option = self.get_option_input()
            valid = self.valid_option(option)
        return int(option)

    def valid_option(self, option: str) -> bool:
        if option not in TURN_OPTIONS:
            print(f"Not a valid option")
            return False
        return True

    def get_option_input(self):
        return input("Enter 1 to roll and 0 to hold: ")


if __name__ == '__main__':

    player_count = int(input("How many players? "))
    match = Match(player_count)
    while not match.over:
        for player in match.players:
            if match.over:
                break
            turn = 1
            must_roll = False
            while turn:
                if not must_roll:
                    roll = match.turn_options(player)
                if must_roll or roll:
                    dice_values = match.roll_dice(player)
                    turn, must_roll = Match.evaluate_roll(
                        dice_values, player
                    )
                else:
                    turn, must_roll = Match.next_turn()
                match.winner(player)
