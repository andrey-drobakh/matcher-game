import src.core as core
from src.core import MoveData
import src.sample_game as sg


class CLIGameInterface( core.AbstractGameInterface ) :
    def __init__( self ) :
        super().__init__()
        self._label = 'CLI interface :'

    def print_intro_text( self, md: MoveData ) :
        text = (
            '\nWelcome to the Matcher game!\n'
            'First, enter player names (separated by space) and\nan even number N of cards.\n'
            'Then, each move the player types two numbers from 1 to N.\n'
            'Try to memorize the card values!\n'
        )

        print( text )

    def read_and_handle_setup_data( self, md: MoveData ) -> bool :
        names = input( 'player names : ' ).split()
        n = int( input( 'number of cards : ' ) )

        prefix = 'error:'
        error_message = ''
        if not 2 <= len( names ) <= 4 :
            error_message = 'players must be 2, 3 or 4'
            print( prefix, error_message )

            return False

        if n <= 0 or n % 2 != 0 :
            error_message = 'number of cards must be positive even integer'
            print( prefix, error_message )

            return False

        md.player_names = names
        md.card_count = n

        return True

    def display_prompt( self, md: MoveData ) :
        name = md.player_names[ md.player_index ]
        print( f'{name} : ', end = '' )

    def read_player_input( self, md: MoveData ) :
        md.player_input = input()

    def display_move_message( self, md: MoveData ) :
        print( self._label, 'display move message' )

    def display_game_results( self, md: MoveData ) :
        print( self._label, 'display game results' )


class CLIGame_SampleBackend( sg.SampleBackend ) :
    def __init__( self ) :
        super().__init__()

    def reset_move( self, md: MoveData ) :
        self._shift_player_index( md )

    def handle_player_input( self, md: MoveData ) :
        super().handle_player_input( md )

    def _is_player_input_correct( self, md : MoveData ) -> bool :
        numbers = md.player_input.split()

        if len( numbers ) == 2 :
            n1 = numbers[ 0 ]
            n2 = numbers[ 1 ]

            if n1.isnumeric() and n2.isnumeric() :
                n1 = int( n1 )
                n2 = int( n2 )

                if 1 <= n1 <= md.card_count and \
                    1 <= n2 <= md.card_count :
                    return True

        return False

    def _shift_player_index( self, md : MoveData ) :
        if md.player_index < len( md.player_names ) - 1 :
            md.player_index += 1
        else :
            md.player_index = 0













