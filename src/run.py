import core
import src.sample_game as sg
from src.cli_game.interface import CLIGameInterface, CLIGame_SampleBackend
from src.cli_game.backend import CLIGameBackend


def run_game(
        game_backend : core.AbstractGameBackend,
        game_interface : core.AbstractGameInterface
) :
    be = game_backend
    i = game_interface

    md = core.MoveData()

    i.print_intro_text( md )

    if not i.read_and_handle_setup_data( md ) :
        return

    be.init_game( md )
    while not be.is_game_over( md ) :
        be.reset_move( md )

        i.display_prompt( md )
        i.read_player_input( md )

        be.handle_player_input( md )

        i.display_move_message( md )
    i.display_game_results( md )


if __name__ == '__main__' :
    # run_game( sg.SampleBackend(), sg.SampleInterface() )
    run_game( CLIGame_SampleBackend(), CLIGameInterface() )

    # For now, this call uses "empty" objects,
    # and it causes running the infinite loop!!!
    # run_game( CLIGameBackend(), CLIGameInterface() )
