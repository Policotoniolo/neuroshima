import pygame
from typing import Optional, Dict, Literal

from scripts.model.model import HexBoard, Tile, Player
from scripts.view.view import View, TileView
from scripts.utils.functions import *

class BoardController:
    def __init__(self, board: HexBoard, view: View) -> None:
        """
        Initializes the board controller with a game board.

        Args:
            board (HexBoard): Game Board
        """
        self.board = board
        self.view = view


    def get_one_model_tile(self, id_tile) -> Optional[Tile]:
        """retrieve one tile model in board from a id tile

        Args:
            id_tile (str): id tile
        """
        for army in self.board.armies:
            for tile in self.board.tiles[army]:
                if tile.id_tile == id_tile:
                    return tile

    def _update_tile_model(self, id_tile: str, pixel_position: tuple, angle_index: Literal[0,1,2,3,4,5]) -> None:
        """Update a tile on the baord model

        Args:
            id_tile (str): id of the tile
            pixel_position (tuple): Pixel position on the screen
            angle_index (int): Index of the angle of the tile
        """
        tilemodel = self.get_one_model_tile(id_tile)
        if tilemodel:
            self.board.add_tile_to_board(tilemodel)
        cube_coordinates = coordinates_pixel_to_cube(pixel_position)
        if tilemodel is not None and cube_coordinates is not None:
            # Create a function for board.position_index
            old_board_position = tilemodel.board_position

            tilemodel.board_position = cube_coordinates
            tilemodel.rotate_tile(angle_index)

            self.board.occupied[tilemodel.army_name].append(cube_coordinates)
            self.board.occupied[tilemodel.army_name].remove(old_board_position)

    def _update_board_model(self):
        """Save actual board from view into the board model
        """
        for tileview in self.view.tiles_board:
            id_tile = tileview.id_tile
            pixel_position = tileview.rect.topleft
            angle_index = tileview.angle_index
            self._update_tile_model(id_tile, pixel_position, angle_index)

    def _update_netted_unite(self):
        for army in self.board.armies:
            enemy_army = next_element(self.board.armies,army)
            
            for tilemodel in self.board.tiles[army]:
                if tilemodel.net_directions:

                    for net_directions in tilemodel.net_directions:
                        netted_positions = calculate_position(net_directions,
                                                        tilemodel.board_position
                                                )
                        if netted_positions in self.board.occupied[enemy_army]:
                            index = self.board.occupied[enemy_army].index(netted_positions)
                            enemy_tile = self.board.tiles[enemy_army][index]
                            enemy_tile.is_netted = True

    def _update_board_view(self):
        self.view.remove_tiles_board_moving()
        self.view.get_tile_to_discard()

    def update_board(self, player: Player):
        self._update_board_model()
        self._update_board_view()
        self._update_netted_unite()

    def update_unite_with_movement(self, player: Player):
        for tilemodel in self.board.tiles[player.deck.army_name]:
            if (tilemodel.special_capacities and
                    "movement" in tilemodel.special_capacities):
                tileview = self.get_one_view_tile(tilemodel.id_tile)
                if tileview not in self.view.tiles_hand:
                    self.view.tiles_board_moving.add(tileview)

    def update_board_view_from_hand(self):
        """Update the board model while moving tileview from hand
        """
        for tileview in self.view.tiles_hand:
            tileviewinfo = self.get_info_from_id_tile(tileview.id_tile)
            if tileviewinfo["kind"] in ["unite", "module"]:
                if pygame.sprite.spritecollideany(
                    tileview,
                    self.view.boardzone.hexagones
                ) is not None:
                    self.view.tiles_board.add(tileview)
                    if tileview.rect.topleft in list(BOARD_PIXEL_TO_CUBE.keys()):
                        self._update_tile_model(
                            tileview.id_tile, tileview.rect.topleft, tileview.angle_index)
                else:
                    self.view.tiles_board.remove(tileview)
                    self.board.remove_tile_from_board(tileview.id_tile)


    def get_info_from_id_tile(self, id_tile: str) -> Dict:
        """retrieve informations of a tile model ont the board from a id tile

        Args:
            id_tile (str): id tile
        """
        for army in self.board.armies:
            for tile in self.board.tiles[army]:
                if tile.id_tile == id_tile:
                    return tile.__dict__
        return {}


    def get_one_view_tile(self, id_tile) -> Optional[TileView]:
        """retrieve one tile view if the tile is on the boardview

        Args:
            id_tiles (_type_): id_tile
        """
        for tileview in self.view.tiles_board:
            if tileview.id_tile == id_tile:
                return tileview