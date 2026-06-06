import abc
from dataclasses import dataclass, field
from enum import Enum, auto


class PlayerInputStatus( Enum ) :
    INVALID = auto()
    VALID_BUT_EQUAL_NUMBERS = auto()
    VALID_DIFFERENT_NUMBERS_BUT_TOO_BIG_NUMBER = auto()
    VALID_DIFFERENT_NUMBERS_NOT_TOO_BIG_BUT_TAKEN_CARD_NUMBER = auto()
    CORRECT = auto()
    SPECIAL_COMMAND = auto()


class GameStatus( Enum ) :
    PLAY = auto()
    STOPPED_BY_FORCE = auto()


class MoveStatus( Enum ) :
    CARDS_TAKEN = auto()
    CARDS_NOT_TAKEN = auto()
    NONE = auto()


@dataclass
class AbstractGameData( abc.ABC ) :
    player_names: list[ str ] = None
    card_count: int = 0

    player_index: int = -1
    player_input: str = ''
    player_input_status: PlayerInputStatus = None
    card_numbers: list[ int ] = field( default_factory = list )
    card_values: list[ str ] = field( default_factory = list )

    taken_cards: list[ int ] = field( default_factory = list )
    names_to_taken_cards: dict[ str, list ] = field( default_factory = dict )
    game_status = GameStatus.PLAY
    move_status = MoveStatus.NONE


class AbstractGameBackend( abc.ABC ) :
    @abc.abstractmethod
    def init_game( self, gd : AbstractGameData ) :
        pass

    @abc.abstractmethod
    def is_game_over( self, gd : AbstractGameData ) -> bool :
        pass

    @abc.abstractmethod
    def reset_move( self, gd : AbstractGameData ) :
        pass

    @abc.abstractmethod
    def handle_player_input( self, gd : AbstractGameData ) :
        pass


class AbstractGameInterface( abc.ABC ) :
    @abc.abstractmethod
    def print_intro_text( self, gd : AbstractGameData ) :
        pass

    @abc.abstractmethod
    def read_and_handle_setup_data( self, gd : AbstractGameData ) -> bool :
        """
        :return: True, if data read is correct.
        """
        pass

    @abc.abstractmethod
    def display_prompt( self, gd : AbstractGameData ) :
        pass

    @abc.abstractmethod
    def read_player_input( self, gd : AbstractGameData ) :
        pass

    @abc.abstractmethod
    def display_card_values( self, gd : AbstractGameData ) :
        pass

    @abc.abstractmethod
    def display_move_message( self, gd : AbstractGameData ) :
        pass

    @abc.abstractmethod
    def display_game_results( self, gd : AbstractGameData ) :
        pass


