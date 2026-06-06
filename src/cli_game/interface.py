from dataclasses import dataclass
import string
import random

import src.core as core
from src.core import (
    PlayerInputStatus,
    GameStatus,
    MoveStatus,
)
from src.cli_game.common import GameData


class CLIGameInterface( core.AbstractGameInterface ) :
    def __init__( self ) :
        super().__init__()
        self._label = 'CLI interface :'

    def print_intro_text( self, gd : GameData ) :
        text = (
            '\nWelcome to the Matcher game!\n'
            'First, enter player names (separated by space) and\nan even number N of cards.\n'
            'Then, each move the player types two numbers from 1 to N.\n'
            'Try to memorize the card values!\n'
        )

        print( text )

    def read_and_handle_setup_data( self, gd : GameData ) -> bool :
        names = input( 'player names : ' ).split()
        n = int( input( 'number of cards : ' ) )

        prefix = 'error:'
        error_message = ''
        if not 2 <= len( names ) <= 4 :
            error_message = 'number of players must be 2, 3 or 4'
            print( prefix, error_message )

            return False
        elif n <= 0 or n % 2 != 0 :
            error_message = 'number of cards must be positive even integer'
            print( prefix, error_message )

            return False

        print()

        gd.player_names = names
        gd.card_count = n

        return True

    def display_prompt( self, gd : GameData ) :
        name = gd.player_name
        print( f'{name} : ', end = '' )

    def read_player_input( self, gd : GameData ) :
        gd.player_input = input()

    def display_card_values( self, gd : GameData ) :
        if gd.player_input_status == PlayerInputStatus.CORRECT :
            print( 'card values :', *gd.card_values )

    def display_move_message( self, gd : GameData ) :
        if gd.game_status == GameStatus.STOPPED_BY_FORCE :
            print( 'Game interrupted!' )

            return

        header = 'error : '
        error_message = header
        if gd.player_input_status == PlayerInputStatus.INVALID :
            error_message += 'type two numbers'
        elif gd.player_input_status == PlayerInputStatus.VALID_BUT_EQUAL_NUMBERS :
            error_message += 'equal numbers'
        elif gd.player_input_status == PlayerInputStatus.VALID_DIFFERENT_NUMBERS_BUT_TOO_BIG_NUMBER :
            error_message += 'too big number'
        elif gd.player_input_status == PlayerInputStatus.VALID_DIFFERENT_NUMBERS_NOT_TOO_BIG_BUT_TAKEN_CARD_NUMBER :
            error_message += 'taken card'

        if gd.player_input_status != PlayerInputStatus.CORRECT :
            print( error_message )

        if gd.move_status == MoveStatus.CARDS_TAKEN :
            name = gd.player_name
            print( f'\t{name} got the cards' )

    def display_game_results( self, gd : GameData ) :
        if gd.game_status == GameStatus.STOPPED_BY_FORCE :
            return

        print( '\n---Results---' )

        for name, cards in gd.names_to_taken_cards.items() :
            n = len( cards ) // 2
            print( f'{name} : {n} pairs' )

        max_count = max( [ len( cards )
                           for cards in gd.names_to_taken_cards.values() ] )
        winners = [ name for name, cards in gd.names_to_taken_cards.items()
                    if len( cards ) == max_count ]

        if len( winners ) == 1 :
            print( f'The winner is {winners[ 0 ]}!\n' )
        else :
            print( 'Draw :', *winners, '\n' )


@dataclass
class Card :
    number : int
    value : str


class CLIGame_SampleBackend( core.AbstractGameBackend ) :
    def __init__( self ) :
        super().__init__()

        self._all_cards : dict[ int, str ] = {}
        self._names_to_taken_cards : dict[ str, list ] = {}

    def is_game_over( self, gd : GameData ) -> bool :
        return gd.game_status == GameStatus.STOPPED_BY_FORCE or \
            len( gd.taken_cards ) == gd.card_count

    def init_game( self, gd : GameData ) :
        self._all_cards = self._create_all_cards( gd.card_count )
        self._names_to_taken_cards = { name : [] for name in gd.player_names }
        gd.names_to_taken_cards = self._names_to_taken_cards

    def reset_move( self, gd : GameData ) :
        gd.player_input_status = None

        if gd.move_status == MoveStatus.CARDS_TAKEN :
            return

        self._shift_player_index( gd )

    def handle_player_input( self, gd : GameData ) :
        pi = gd.player_input

        if pi == '.' :
            gd.game_status = GameStatus.STOPPED_BY_FORCE
            gd.player_input_status = PlayerInputStatus.SPECIAL_COMMAND

            return

        if not self._is_player_input_valid( gd ) :
            gd.player_input_status = PlayerInputStatus.INVALID
            gd.move_status = MoveStatus.CARDS_NOT_TAKEN

            return

        numbers = self._get_card_numbers( pi )
        n1 = numbers[ 0 ]
        n2 = numbers[ 1 ]

        if n1 == n2 :
            md.player_input_status = PlayerInputStatus.VALID_BUT_EQUAL_NUMBERS
            md.move_status = MoveStatus.CARDS_NOT_TAKEN
        elif not self._is_card_number_in_range( n1, gd ) or \
            not self._is_card_number_in_range( n2, gd ) :
            md.player_input_status = PlayerInputStatus.VALID_DIFFERENT_NUMBERS_BUT_TOO_BIG_NUMBER
            md.move_status = MoveStatus.CARDS_NOT_TAKEN
        elif self._is_card_number_taken( n1, gd ) or \
            self._is_card_number_taken( n2, gd ) :
            gd.player_input_status = PlayerInputStatus.VALID_DIFFERENT_NUMBERS_NOT_TOO_BIG_BUT_TAKEN_CARD_NUMBER
            gd.move_status = MoveStatus.CARDS_NOT_TAKEN
        else :
            gd.player_input_status = PlayerInputStatus.CORRECT
            gd.card_numbers = numbers
            values = self._get_card_values( numbers )
            gd.card_values = values

            if values[ 0 ] == values[ 1 ] :
                name = gd.player_name
                v = values[ 0 ]
                self._names_to_taken_cards[ name ].append(
                    Card( numbers[ 0 ], v ) )
                self._names_to_taken_cards[ name ].append(
                    Card( numbers[ 1 ], v ) )

                gd.taken_cards.append( numbers[ 0 ] )
                gd.taken_cards.append( numbers[ 1 ] )

                gd.move_status = MoveStatus.CARDS_TAKEN
            else :
                gd.move_status = MoveStatus.CARDS_NOT_TAKEN

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

    def _is_card_number_taken( self, number, gd : GameData ) -> bool :
        return number in gd.taken_cards

    def _is_card_number_in_range( self, number, gd : GameData ) -> bool :
        return number <= gd.card_count

    def _get_card_numbers( self, valid_player_input : str ) -> list[ int ] :
        return [ int( n ) for n in valid_player_input.split() ]

    def _is_player_input_valid( self, gd : GameData ) -> bool :
        """
        Player Input is valid <=> it's two positive integer numbers.
        """
        numbers = gd.player_input.split()

        if len( numbers ) == 2 :
            n1 = numbers[ 0 ]
            n2 = numbers[ 1 ]

            if n1.isnumeric() and n2.isnumeric() :
                n1 = int( n1 )
                n2 = int( n2 )

                if 1 <= n1 and 1 <= n2 :
                    return True

        return False

    def _shift_player_index( self, gd : GameData ) :
        if gd.player_index < len( gd.player_names ) - 1 :
            gd.player_index += 1
        else :
            gd.player_index = 0













