from src.core import (
    AbstractGameBackend,
    AbstractGameInterface,
    AbstractGameData,
)

import time


def wait() :
    time.sleep( 0.5 )


class GameData( AbstractGameData ) :
    pass


class SampleBackend( AbstractGameBackend ) :
    def __init__( self ) :
        super().__init__()

        self._player_input = ''
        self._game_is_over = False

    def init_game( self, gd : AbstractGameData ) :
        wait()
        print( 'backend : init game' )

    def is_game_over( self, gd : AbstractGameData ) -> bool :
        wait()

        answer = 'No' if not self._game_is_over else 'Yes'
        print( 'backend : is game over?', answer )

        return self._game_is_over

    def reset_move( self, gd : AbstractGameData ) :
        wait()
        print( '\nbackend : reset move' )

    def handle_player_input( self, gd : AbstractGameData ) :
        wait()
        print( 'backend : handle player input ...' )

        self._player_input = input( '\ttype \"go\" or \"stop\" : ' ).strip()

        if self._player_input == 'stop' :
            self._game_is_over = True


class SampleInterface( AbstractGameInterface ) :
    def __init__( self ) :
        super().__init__()
        self._prompt = 'interface :'

    def print_intro_text( self, gd : AbstractGameData ) :
        wait()
        print( self._prompt, 'intro text' )

    def read_and_handle_setup_data( self, gd : AbstractGameData ) -> bool :
        wait()
        print( self._prompt, 'Here the program reads the player name and handles it' )

        return True

    def display_prompt( self, gd : AbstractGameData ) :
        wait()
        print( self._prompt, 'display prompt' )

    def read_player_input( self, gd : AbstractGameData ) :
        wait()
        print( self._prompt, 'here the program just reads the input' )

    def display_move_message( self, gd : AbstractGameData ) :
        wait()
        print( self._prompt, 'display move message' )

    def display_card_values( self, gd : AbstractGameData ) :
        wait()
        print( self._prompt, 'display card values' )

    def display_game_results( self, gd : AbstractGameData ) :
        wait()
        print( '\n' + self._prompt, 'display game results' )
