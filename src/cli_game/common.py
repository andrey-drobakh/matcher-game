from dataclasses import dataclass

import src.core as core


@dataclass
class GameData( core.AbstractGameData ) :
    @property
    def player_name( self ) :
        return self.player_names[ self.player_index ]
