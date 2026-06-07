from dataclasses import dataclass, field
import string
import random

import src.core as core


@dataclass
class GameData( core.AbstractGameData ) :
    all_cards : dict[ int, str ] = field( default_factory = dict )

    @property
    def player_name( self ) :
        return self.player_names[ self.player_index ]


def create_all_cards( size : int ) :
    """
    :param size: an even integer.
    """

    k = size // 2
    letters = list( string.ascii_lowercase[ : k ] ) * 2
    random.shuffle( letters )

    result = { }
    for i, letter in enumerate( letters ) :
        result[ i + 1 ] = letter

    return result