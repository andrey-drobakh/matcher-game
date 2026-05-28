import abc
from dataclasses import dataclass


class AbstractGameBackend( abc.ABC ) :
    @abc.abstractmethod
    def init_game( self, md : MoveData ) :
        pass

    @abc.abstractmethod
    def is_game_over( self, md : MoveData ) -> bool :
        pass

    @abc.abstractmethod
    def reset_move( self, md : MoveData ) :
        pass

    @abc.abstractmethod
    def handle_player_input( self, md : MoveData ) :
        pass


class AbstractGameInterface( abc.ABC ) :
    @abc.abstractmethod
    def print_intro_text( self, md : MoveData ) :
        pass

    @abc.abstractmethod
    def read_and_handle_setup_data( self, md : MoveData ) -> bool :
        """
        :return: True, if data read is correct.
        """
        pass

    @abc.abstractmethod
    def display_prompt( self, md : MoveData ) :
        pass

    @abc.abstractmethod
    def read_player_input( self, md : MoveData ) :
        pass

    @abc.abstractmethod
    def display_move_message( self, md : MoveData ) :
        pass

    @abc.abstractmethod
    def display_game_results( self, md : MoveData ) :
        pass


@dataclass
class MoveData :
    player_names : list[ str ] = None
    card_count : int = 0
    # setup_data_error_message : str = ''

    player_index : int = -1
    player_input : str = ''
