import src.core as core
from src.core import MoveData


class CLIGameInterface( core.AbstractGameInterface ) :
    def __init__( self ) :
        super().__init__()

    def print_intro_text( self, md: MoveData ) :
        pass

    def read_and_handle_player_names( self, md: MoveData ) :
        pass

    def display_prompt( self, md: MoveData ) :
        pass

    def read_player_input( self, md: MoveData ) :
        pass

    def display_move_message( self, md: MoveData ) :
        pass

    def display_game_results( self, md: MoveData ) :
        pass
