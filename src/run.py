from src import core
import src.sample_game as sg
from src.cli_game.interface import (
    CLIGameInterface,
    CLIGame_SampleBackend,
)
import src.cli_game.common
# from src.cli_game.backend import CLIGameBackend


def run_game(
        game_backend : core.AbstractGameBackend,
        game_interface : core.AbstractGameInterface,
        game_data : core.AbstractGameData
) :
    be = game_backend
    i = game_interface
    data = game_data

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


if __name__ == '__main__' :
    # run_game(
    #     sg.SampleBackend(),
    #     sg.SampleInterface(),
    #     sg.GameData()
    # )

    run_game(
        CLIGame_SampleBackend(),
        CLIGameInterface(),
        src.cli_game.common.GameData()
    )

    # For now, this call uses "empty" objects,
    # and it causes running the infinite loop!!!
    # run_game( CLIGameBackend(), CLIGameInterface() )
