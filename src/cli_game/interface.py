from dataclasses import dataclass
import string
import random
import time

import src.core as core
from src.core import (
    PlayerInputStatus,
    GameStatus,
    MoveStatus,
)
from src.cli_game.common import GameData, create_all_cards


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
        n = input( 'number of cards : ' )

        prefix = 'error:'
        error_message = ''

        if not n.isnumeric() :
            error_message = 'number of cards must be a number'
            print( prefix, error_message )

            return False

        n = int( n )

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
            prompt = 'card values :'
            question_mark = '\u2754'

            print( prompt, *gd.card_values, end = '', flush = True )
            time.sleep( 2.0 )
            print( '\r' + prompt + '\033[K' +
                   ' ' + question_mark + ' ' + question_mark, flush = True )
            time.sleep( 0.6 )


    def display_move_message( self, gd : GameData ) :
        if gd.game_status == GameStatus.STOPPED_BY_FORCE :
            print( 'Game interrupted!' )

            return

        header = 'error : '
        error_message = header
        match gd.player_input_status :
            case PlayerInputStatus.INVALID :
                error_message += 'type two numbers'
            case PlayerInputStatus.VALID_BUT_EQUAL_NUMBERS :
                error_message += 'equal numbers'
            case PlayerInputStatus.VALID_DIFFERENT_NUMBERS_BUT_TOO_BIG_NUMBER :
                error_message += 'too big number'
            case PlayerInputStatus.VALID_DIFFERENT_NUMBERS_NOT_TOO_BIG_BUT_TAKEN_CARD_NUMBER :
                error_message += 'taken card'

        if gd.player_input_status != PlayerInputStatus.CORRECT :
            print( error_message )

        if gd.move_status == MoveStatus.CARDS_TAKEN :
            name = gd.player_name
            print( f'\t{name} got the cards' )

        if gd.move_status == MoveStatus.CARDS_NOT_TAKEN :
            print()

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


class _PIHandlerHelper :
    def __init__( self, game_data : GameData ) :
        self._gd = game_data

    @staticmethod
    def is_player_input_valid( raw_player_input : str ) -> bool :
        """
        Player Input is valid <=> it's two positive integer numbers.
        """
        numbers = raw_player_input.split()

        if len( numbers ) == 2 :
            n1 = numbers[ 0 ]
            n2 = numbers[ 1 ]

            if n1.isnumeric() and n2.isnumeric() :
                n1 = int( n1 )
                n2 = int( n2 )

                if 1 <= n1 and 1 <= n2 :
                    return True

        return False

    @staticmethod
    def get_card_numbers( valid_player_input : str ) -> list[ int ] :
        return [ int( n ) for n in valid_player_input.split() ]

    def is_card_number_too_big( self,  card_number ) -> bool :
        return card_number <= self._gd.card_count

    def is_card_number_taken( self,  card_number ) -> bool :
        return card_number in self._gd.taken_cards

    def get_card_values( self,  card_numbers : list ) -> list :
        n1 = card_numbers[ 0 ]
        n2 = card_numbers[ 1 ]

        return [ self._gd.all_cards[ n1 ], self._gd.all_cards[ n2 ] ]


class CLIGame_SampleBackend( core.AbstractGameBackend ) :
    def __init__( self ) :
        super().__init__()

    def is_game_over( self, gd : GameData ) -> bool :
        return gd.game_status == GameStatus.STOPPED_BY_FORCE or \
            len( gd.taken_cards ) == gd.card_count

    def init_game( self, gd : GameData ) :
        gd.all_cards = create_all_cards( gd.card_count )
        gd.names_to_taken_cards = { name : [] for name in gd.player_names }

    def reset_move( self, gd : GameData ) :
        gd.player_input_status = None

        if gd.move_status == MoveStatus.CARDS_TAKEN :
            return

        gd.player_index = ( gd.player_index + 1 ) % len( gd.player_names )

    def handle_player_input( self, gd : GameData ) :
        helper = _PIHandlerHelper( gd )

        pi = gd.player_input

        if pi == '.' :
            gd.game_status = GameStatus.STOPPED_BY_FORCE
            gd.player_input_status = PlayerInputStatus.SPECIAL_COMMAND

            return

        if not helper.is_player_input_valid( pi ) :
            gd.player_input_status = PlayerInputStatus.INVALID
            gd.move_status = MoveStatus.CARDS_NOT_TAKEN

            return

        numbers = helper.get_card_numbers( pi )
        n1 = numbers[ 0 ]
        n2 = numbers[ 1 ]

        if n1 == n2 :
            gd.player_input_status = PlayerInputStatus.VALID_BUT_EQUAL_NUMBERS
            gd.move_status = MoveStatus.CARDS_NOT_TAKEN
        elif not helper.is_card_number_too_big( n1 ) or \
                not helper.is_card_number_too_big( n2 ) :
            gd.player_input_status = PlayerInputStatus.VALID_DIFFERENT_NUMBERS_BUT_TOO_BIG_NUMBER
            gd.move_status = MoveStatus.CARDS_NOT_TAKEN
        elif helper.is_card_number_taken( n1 ) or \
                helper.is_card_number_taken( n2 ) :
            gd.player_input_status = PlayerInputStatus.VALID_DIFFERENT_NUMBERS_NOT_TOO_BIG_BUT_TAKEN_CARD_NUMBER
            gd.move_status = MoveStatus.CARDS_NOT_TAKEN
        else :
            gd.player_input_status = PlayerInputStatus.CORRECT
            gd.card_numbers = numbers
            values = helper.get_card_values( numbers )
            gd.card_values = values

            if values[ 0 ] == values[ 1 ] :
                name = gd.player_name
                v = values[ 0 ]
                gd.names_to_taken_cards[ name ].append(
                    Card( numbers[ 0 ], v ) )
                gd.names_to_taken_cards[ name ].append(
                    Card( numbers[ 1 ], v ) )

                gd.taken_cards.append( numbers[ 0 ] )
                gd.taken_cards.append( numbers[ 1 ] )

                gd.move_status = MoveStatus.CARDS_TAKEN
            else :
                gd.move_status = MoveStatus.CARDS_NOT_TAKEN



