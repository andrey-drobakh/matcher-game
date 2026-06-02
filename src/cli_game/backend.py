import random
import string

from src.core import (
    AbstractGameBackend,
    MoveData,
    PlayerInputStatus,
    GameStatus,
    MoveStatus
)


class CLIGameBackend(AbstractGameBackend):
    def __init__(self):
        super().__init__()

        self._all_cards = {}

    def init_game(self, md: MoveData):
        self._all_cards = self._create_all_cards(md.card_count)

        md.player_index = 0
        md.taken_cards.clear()

        md.names_to_taken_cards = {
            name: []
            for name in md.player_names
        }

        md.move_status = MoveStatus.NONE
        md.game_status = GameStatus.PLAY

    def is_game_over(self, md: MoveData) -> bool:
        return (
            md.game_status == GameStatus.STOPPED_BY_FORCE
            or len(md.taken_cards) == md.card_count
        )

    def reset_move(self, md: MoveData):
        md.player_input_status = None

        if md.move_status == MoveStatus.CARDS_TAKEN:
            return

        md.player_index = (
            md.player_index + 1
        ) % len(md.player_names)

    def handle_player_input(self, md: MoveData):
        pi = md.player_input.strip()

        if pi == ".":
            md.game_status = GameStatus.STOPPED_BY_FORCE
            md.player_input_status = PlayerInputStatus.SPECIAL_COMMAND
            return

        if not self._is_player_input_valid(pi):
            md.player_input_status = PlayerInputStatus.INVALID
            md.move_status = MoveStatus.CARDS_NOT_TAKEN
            return

        n1, n2 = [int(x) for x in pi.split()]

        if n1 == n2:
            md.player_input_status = (
                PlayerInputStatus.VALID_BUT_EQUAL_NUMBERS
            )
            md.move_status = MoveStatus.CARDS_NOT_TAKEN
            return

        if (
            not self._is_card_number_in_range(n1, md)
            or not self._is_card_number_in_range(n2, md)
        ):
            md.player_input_status = (
                PlayerInputStatus
                .VALID_DIFFERENT_NUMBERS_BUT_TOO_BIG_NUMBER
            )
            md.move_status = MoveStatus.CARDS_NOT_TAKEN
            return

        if (
            self._is_card_number_taken(n1, md)
            or self._is_card_number_taken(n2, md)
        ):
            md.player_input_status = (
                PlayerInputStatus
                .VALID_DIFFERENT_NUMBERS_NOT_TOO_BIG_BUT_TAKEN_CARD_NUMBER
            )
            md.move_status = MoveStatus.CARDS_NOT_TAKEN
            return

        value1 = self._all_cards[n1]
        value2 = self._all_cards[n2]

        md.card_numbers = [n1, n2]
        md.card_values = [value1, value2]
        md.player_input_status = PlayerInputStatus.CORRECT

        if value1 == value2:
            md.taken_cards.append(n1)
            md.taken_cards.append(n2)

            player_name = md.player_names[md.player_index]

            md.names_to_taken_cards[player_name].append(n1)
            md.names_to_taken_cards[player_name].append(n2)

            md.move_status = MoveStatus.CARDS_TAKEN
        else:
            md.move_status = MoveStatus.CARDS_NOT_TAKEN

    def _create_all_cards(self, card_count):
        pair_count = card_count // 2

        letters = list(string.ascii_lowercase[:pair_count]) * 2

        random.shuffle(letters)

        cards = {}

        for i, letter in enumerate(letters):
            cards[i + 1] = letter

        return cards

    def _is_player_input_valid(self, player_input):
        numbers = player_input.split()

        if len(numbers) != 2:
            return False

        if not numbers[0].isdigit():
            return False

        if not numbers[1].isdigit():
            return False

        return int(numbers[0]) > 0 and int(numbers[1]) > 0

    def _is_card_number_in_range(
        self,
        number,
        md: MoveData
    ):
        return 1 <= number <= md.card_count

    def _is_card_number_taken(
        self,
        number,
        md: MoveData
    ):
        return number in md.taken_cards