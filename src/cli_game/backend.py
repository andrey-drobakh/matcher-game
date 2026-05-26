import src.core as core
from src.core import MoveData


class CLIGameBackend( core.AbstractGameBackend ) :
    def __init__( self ) :
        super().__init__()

    def init_game( self, md : MoveData ) :
        pass

    def is_game_over( self, md : MoveData ) -> bool :
        pass

    def reset_move( self, md : MoveData ) :
        pass

    def handle_player_input( self, md : MoveData ) :
        pass


