from src.core import \
    AbstractGameBackend, \
    AbstractGameInterface, \
    MoveData

import time


def wait() :
    time.sleep( 0.5 )


class SampleBackend( AbstractGameBackend ) :
    def __init__( self ) :
        super().__init__()

        self._player_input = ''
        self._game_is_over = False

    def init_game( self, md : MoveData ) :
        wait()
        print( 'backend : init game' )

    def is_game_over( self, md : MoveData ) -> bool :
        wait()

        answer = 'No' if not self._game_is_over else 'Yes'
        print( 'backend : is game over?', answer )

        return self._game_is_over

    def reset_move( self, md : MoveData ) :
        wait()
        print( '\nbackend : reset move' )

    def handle_player_input( self, md : MoveData ) :
        wait()
        print( 'backend : handle player input ...' )

        self._player_input = input( 'type \"go\" or \"stop\" : ' ).strip()

        if self._player_input == 'stop' :
            self._game_is_over = True


class SampleInterface( AbstractGameInterface ) :
    def __init__( self ) :
        super().__init__()
        self._prompt = 'interface :'

    def print_intro_text( self, md : MoveData ) :
        wait()
        print( self._prompt, 'intro text' )

    def read_and_handle_player_names( self, md : MoveData ) :
        wait()
        print( self._prompt, 'Here the program reads the player name and handles it' )

    def display_prompt( self, md : MoveData ) :
        wait()
        print( self._prompt, 'display prompt' )

    def read_player_input( self, md : MoveData ) :
        wait()
        print( self._prompt, 'here the program reads the input and handles it' )

    def display_move_message( self, md : MoveData ) :
        wait()
        print( self._prompt, 'display move message' )

    def display_game_results( self, md : MoveData ) :
        wait()
        print( '\n' + self._prompt, 'display game results' )
