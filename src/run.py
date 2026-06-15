from src import core
import src.sample_game as sg
from src.cli_game.interface import (
    CLIGameInterface,
    CLIGame_SampleBackend,
)
import src.cli_game.common
# from src.cli_game.backend import CLIGameBackend


def run_game_match(
        game_backend : core.AbstractGameBackend,
        game_interface : core.AbstractGameInterface,
        game_data : core.AbstractGameData,
        print_intro_text : bool = True,
) :
    be = game_backend
    i = game_interface
    data = game_data

    if print_intro_text :
        i.print_intro_text( data )

    if not i.read_and_handle_setup_data( data ) :
        return

    be.init_game( data )
    while not be.is_game_over( data ) :
        be.reset_move( data )

        i.display_prompt( data )
        i.read_player_input( data )

        be.handle_player_input( data )

        i.display_card_values( data )
        i.display_move_message( data )
    i.display_game_results( data )


def run_app() :
    print_intro_text = True
    while True :
        run_game_match(
            CLIGame_SampleBackend(),
            CLIGameInterface(),
            src.cli_game.common.GameData(),
            print_intro_text
        )

        quit_app = False

        while True :
            play_again = input( '\nPlay again? [y/n] : ' )
            match play_again.strip().lower() :
                case 'yes' | 'y' :
                    print_intro_text = False

                    break
                case 'no' | 'n' :
                    quit_app = True

                    break
                case _ :
                    print( 'error : type \'yes\', \'no\' or just \'y\' or \'n\'' )

        if quit_app :
            break

    print( '\nBye!' )


if __name__ == '__main__' :
    # run_game_match(
    #     sg.SampleBackend(),
    #     sg.SampleInterface(),
    #     sg.GameData()
    # )

    # run_game_match(
    #     CLIGame_SampleBackend(),
    #     CLIGameInterface(),
    #     src.cli_game.common.GameData()
    # )

    run_app()
