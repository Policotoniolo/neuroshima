import pygame
from typing import Optional, List, Literal

from scripts.model.model import HexBoard, Player
from scripts.view.view import View
from scripts.controllers.tilecontroller import TileController

class PlayersController:
    def __init__(self, board: HexBoard, players: List[Player], view: View, tileactioncontroller: TileController
                ) -> None:
        """
        Initializes the controller with a game board.

        Args:
            board (HexBoard): Game Board
        """
        self.board = board
        self.players = self.players
        self.tileactioncontroller = tileactioncontroller
        self.view = view

    def get_id_tiles_from_hand(self, player: Player) -> List[str]:
        """get id tile from hand player model and return a list

        Args:
            player (Player): Player class
        """
        id_tiles = []
        for tile in player.hand.hand_tiles:
            id_tiles.append(tile.id_tile)
        return id_tiles

    def get_size_deck(self, player: Player) -> int:
        """get the number of remaining tiles in the player deck
        Args:
            player (Player): Instance of Player
        """
        return len(player.deck.tiles)

    def prompt_deck(self, player: Player):
        number_tiles = self.get_size_deck(player)
        self.view.get_tiles_deck(number_tiles)

    def draw_hq_tile(self, player: Player):
        player.get_tiles(1)
        id_tile = self.get_id_tiles_from_hand(player)
        self.view.get_tiles_hand(id_tile)

    def draw_tiles_hand(self, player: Player, nb_tiles: Literal[1,2,3]=3):
        nb_tiles_hand = len(player.hand.hand_tiles)
        diff = nb_tiles - nb_tiles_hand
        if diff > 3:
            raise ValueError()
        if diff < 0:
            raise ValueError(
                "Number of tile ask less than number of tile already in hand"
            )
        elif diff != 0:
            player.get_tiles(diff) # type: ignore

        id_tiles = self.get_id_tiles_from_hand(player)
        self.view.get_tiles_hand(id_tiles)


    def play_tile_hand(self, player: Player, event_list: List[pygame.event.Event]):
        self.view.move_tile_hand(event_list)
        self.view.move_tile_board(event_list)
        self.view.generate_all_sprite_group()
        self.view.display_all_sprite()

        self.tileactioncontroller.actiontile(player, event_list)


    def end_player_turn(self, player: Player, event_list: List[pygame.event.Event]):
        if self.view.endbutton.isvalidated(event_list):
            id_tileviews_to_keep = self.view.get_id_tile_to_keep()
            player.discard_tiles_hand(id_tileviews_to_keep)

            if len(self.board.position_index) == 19:
                pass
            return True
