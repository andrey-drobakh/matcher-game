from dataclasses import dataclass
import string
import random

import src.core as core
from src.core import \
    MoveData, \
    PlayerInputStatus, \
    GameStatus, \
    MoveStatus
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

        print()

        md.player_names = names
        md.card_count = n

        return True

    def display_prompt( self, md: MoveData ) :
        name = md.player_names[ md.player_index ]
        print( f'{name} : ', end = '' )

    def read_player_input( self, md: MoveData ) :
        md.player_input = input()

    def display_card_values( self, md: MoveData ) :
        if md.player_input_status == PlayerInputStatus.CORRECT :
            print( 'card values :', *md.card_values )

    def display_move_message( self, md: MoveData ) :
        if md.game_status == GameStatus.STOPPED_BY_FORCE :
            print( 'Game interrupted!' )

            return

        header = 'error : '
        error_message = header
        if md.player_input_status == PlayerInputStatus.INVALID :
            error_message += 'type two numbers'
        elif md.player_input_status == PlayerInputStatus.VALID_BUT_EQUAL_NUMBERS :
            error_message += 'equal numbers'
        elif md.player_input_status == PlayerInputStatus.VALID_DIFFERENT_NUMBERS_BUT_TOO_BIG_NUMBER :
            error_message += 'too big number'
        elif md.player_input_status == PlayerInputStatus.VALID_DIFFERENT_NUMBERS_NOT_TOO_BIG_BUT_TAKEN_CARD_NUMBER :
            error_message += 'taken card'

        if md.player_input_status != PlayerInputStatus.CORRECT :
            print( error_message )

        if md.move_status == MoveStatus.CARDS_TAKEN :
            name = md.player_names[ md.player_index ]
            print( f'\t{name} got the cards' )

    def display_game_results( self, md: MoveData ) :
        if md.game_status == GameStatus.STOPPED_BY_FORCE :
            return

        print( '\n---Results---' )

        for name, cards in md.names_to_taken_cards.items() :
            n = len( cards ) // 2
            print( f'{name} : {n} pairs' )

        max_count = max( [ len( cards )
                           for cards in md.names_to_taken_cards.values() ] )
        winners = [ name for name, cards in md.names_to_taken_cards.items()
                    if len( cards ) == max_count ]

        if len( winners ) == 1 :
            print( f'The winner is {winners[ 0 ]}!\n' )
        else :
            print( 'Draw :', *winners, '\n' )


@dataclass
class Card :
    number : int
    value : str


class CLIGame_SampleBackend( sg.SampleBackend ) :
    def __init__( self ) :
        super().__init__()

        self._all_cards : dict[ int, str ] = {}
        self._names_to_taken_cards : dict[ str, list ] = {}

    def is_game_over( self, md: MoveData ) -> bool :
        return md.game_status == GameStatus.STOPPED_BY_FORCE or \
            len( md.taken_cards ) == md.card_count

    def init_game( self, md: MoveData ) :
        self._all_cards = self._create_all_cards( md.card_count )
        self._names_to_taken_cards = { name : [] for name in md.player_names }
        md.names_to_taken_cards = self._names_to_taken_cards

    def reset_move( self, md: MoveData ) :
        md.player_input_status = None

        if md.move_status == MoveStatus.CARDS_TAKEN :
            return

        self._shift_player_index( md )

    def handle_player_input( self, md: MoveData ) :
        pi = md.player_input

        if pi == '.' :
            md.game_status = GameStatus.STOPPED_BY_FORCE
            md.player_input_status = PlayerInputStatus.SPECIAL_COMMAND

            return

        if not self._is_player_input_valid( md ) :
            md.player_input_status = PlayerInputStatus.INVALID
            md.move_status = MoveStatus.CARDS_NOT_TAKEN

            return

        numbers = self._get_card_numbers( pi )
        n1 = numbers[ 0 ]
        n2 = numbers[ 1 ]

        if n1 == n2 :
            md.player_input_status = PlayerInputStatus.VALID_BUT_EQUAL_NUMBERS
            md.move_status = MoveStatus.CARDS_NOT_TAKEN
        elif not self._is_card_number_in_range( n1, md ) or \
            not self._is_card_number_in_range( n2, md ) :
            md.player_input_status = PlayerInputStatus.VALID_DIFFERENT_NUMBERS_BUT_TOO_BIG_NUMBER
            md.move_status = MoveStatus.CARDS_NOT_TAKEN
        elif self._is_card_number_taken( n1, md ) or \
            self._is_card_number_taken( n2, md ) :
            md.player_input_status = PlayerInputStatus.VALID_DIFFERENT_NUMBERS_NOT_TOO_BIG_BUT_TAKEN_CARD_NUMBER
            md.move_status = MoveStatus.CARDS_NOT_TAKEN
        else :
            md.player_input_status = PlayerInputStatus.CORRECT
            md.card_numbers = numbers
            values = self._get_card_values( numbers )
            md.card_values = values

            if values[ 0 ] == values[ 1 ] :
                name = md.player_names[ md.player_index ]
                v = values[ 0 ]
                self._names_to_taken_cards[ name ].append(
                    Card( numbers[ 0 ], v ) )
                self._names_to_taken_cards[ name ].append(
                    Card( numbers[ 1 ], v ) )

                md.taken_cards.append( numbers[ 0 ] )
                md.taken_cards.append( numbers[ 1 ] )

                md.move_status = MoveStatus.CARDS_TAKEN
            else :
                md.move_status = MoveStatus.CARDS_NOT_TAKEN

    def _get_card_values( self, card_numbers ) -> list[ str ] :
        n1 = card_numbers[ 0 ]
        n2 = card_numbers[ 1 ]

        return [ self._all_cards[ n1 ], self._all_cards[ n2 ] ]

    @staticmethod
    def _create_all_cards( size : int ) :
        """
        :param size: an even integer.
        """

        k = size // 2
        letters = list( string.ascii_lowercase[ : k ] ) * 2
        random.shuffle( letters )

        result = {}
        for i, letter in enumerate( letters ) :
            result[ i + 1 ] = letter

        return result

    def _is_card_number_taken( self, number, md : MoveData ) -> bool :
        return number in md.taken_cards

    def _is_card_number_in_range( self, number, md : MoveData ) -> bool :
        return number <= md.card_count

    def _get_card_numbers( self, valid_player_input : str ) -> list[ int ] :
        return [ int( n ) for n in valid_player_input.split() ]

    def _is_player_input_valid( self, md : MoveData ) -> bool :
        """
        Player Input is valid <=> it's two positive integer numbers.
        """
        numbers = md.player_input.split()

        if len( numbers ) == 2 :
            n1 = numbers[ 0 ]
            n2 = numbers[ 1 ]

            if n1.isnumeric() and n2.isnumeric() :
                n1 = int( n1 )
                n2 = int( n2 )

                if 1 <= n1 and 1 <= n2 :
                    return True

        return False

    def _shift_player_index( self, md : MoveData ) :
        if md.player_index < len( md.player_names ) - 1 :
            md.player_index += 1
        else :
            md.player_index = 0













