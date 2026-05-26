import abc


class AbstractGameBackend( abc.ABC ) :
    @abc.abstractmethod
    def init_game( self, md : MoveData ) :
        pass

    @abc.abstractmethod
    def is_game_over( self, md : MoveData ) -> bool :
        pass

    @abc.abstractmethod
    def reset_move( self, md : MoveData ) :
        pass

    @abc.abstractmethod
    def handle_player_input( self, md : MoveData ) :
        pass


class AbstractGameInterface( abc.ABC ) :
    @abc.abstractmethod
    def print_intro_text( self, md : MoveData ) :
        pass

    @abc.abstractmethod
    def read_and_handle_player_names( self, md : MoveData ) :
        pass

    @abc.abstractmethod
    def display_prompt( self, md : MoveData ) :
        pass

    @abc.abstractmethod
    def read_player_input( self, md : MoveData ) :
        pass

    @abc.abstractmethod
    def display_move_message( self, md : MoveData ) :
        pass

    @abc.abstractmethod
    def display_game_results( self, md : MoveData ) :
        pass


class MoveData :
    pass
