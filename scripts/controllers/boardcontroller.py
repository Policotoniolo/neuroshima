# This import able to import gamecontroller without circular 
# import issue
from __future__ import annotations


from typing import Optional, Dict, Literal

from scripts.model.model import Tile, Player
from scripts.view.view import TileView
from scripts.controllers import gamecontroller
from scripts.utils.functions import *


class BoardController:
    """
    A controller class responsible for managing the state and
    synchronization of the game board between the model and the view.

    The `BoardController` class provides methods to update the board
    model and view, synchronize tile information, and handle specific
    game mechanics such as movement speciale capacities, netting of
    units.

    Attributes
    ----------
    gamecontroller (GameController): 
        The main controller with all others sub controllers and
        models informations.

    Methods
    ----------
    update_board(player: Player) -> None:
        Updates the board model and view, synchronizing their states
        with the given player's tiles.

    update_board_view_from_hand() -> None:
        Updates the board model and view when tiles are moved from the
        hand area.


    Private Methods
    ----------
    _get_one_model_tile(id_tile: str) -> Tile:
        Retrieves a `Tile` object from the model using its ID.

    _check_if_tile_on_board(id_tile: str) -> bool:
        Checks if a tile with the given ID is present on the board.

    _get_info_from_id_tile(id_tile: str) -> Optional[TileView]:
        Retrieves information about a tile from the board model using
        its ID.

    _get_one_view_tile(id_tile: str) -> Tile:
        Retrieves a `TileView` object for a tile currently displayed on
        the board view (tiles_board sprites group).

    _update_unite_with_movement(player: Player) -> None:
        Marks units with movement capabilities and add them in the
        sprite group `tiles_board_moving`, allowing them to move on the
        board.

    _update_tile_model(id_tile: str,\
                        pixel_position: tuple,\
                        angle_index: Literal[0, 1, 2, 3, 4, 5]\
                    ) -> None:
        Updates the model state of a tile based on its ID, new position,
        and new rotation angle.

    _update_board_model() -> None:
        Synchronizes the board model to match the current state of the
        board view.

    _update_netted_unite()-> None:
        Updates the attribut `is_netted` of enemy tiles on the board
        affected by netting mechanics.

    _update_board_view() -> None:
        Updates the board view by cleaning the discard zone and the
        sprite tile_board_moving.
    """

    def __init__(self,
                gamecontroller: gamecontroller.GameController
                ) -> None:
        """
        Initializes the controller.

        Args:
            gamecontroller (GameController): 
                The main controller with all others sub controllers and
                models informations.
        """
        self.gamecontroller = gamecontroller

    def update_board(self, player: Player) -> None:
        """
        Updates the board model and view, synchronizing their states.

        This method updates the following aspects:
        - The board model based on the current state of the board view.
        - The board view by cleaning the discard zone and the sprite 
        tile_board_moving.
        - Tiles that have movement capabilities.
        - Units that are affected by netting mechanics.

        Args:
            player (Player): The player whose tiles are being updated.
        """
        self._update_board_model()
        self._update_board_view()
        self._update_unite_with_movement(player)
        self._update_netted_unite()

    def update_board_view_from_hand(self) -> None:
        """
        Updates the board model while moving tiles from the hand area.

        Synchronizes tile placement or removal between the hand and the
        board, ensuring the model reflects any changes in tile
        positioning or angle.
        """
        for tileview in self.gamecontroller.view.tiles_hand:
            tileviewinfo = self._get_info_from_id_tile(tileview.id_tile)
            tile_kind = tileviewinfo.get("kind")
            tile_position = tileview.rect.topleft
            is_valid_position = tile_position in BOARD_PIXEL_TO_CUBE

            if tile_kind in ["unite", "module", "base"]:
                if self.gamecontroller.view.boardzone.single_collision(tileview):
                    self.gamecontroller.view.tiles_board.add(tileview)
                    if is_valid_position:
                        self._update_tile_model(
                                            tileview.id_tile,
                                            tileview.rect.topleft,
                                            tileview.angle_index
                                            )

                elif self._check_if_tile_on_board(tileview.id_tile):
                        self.gamecontroller.view.tiles_board.remove(tileview)
                        self.gamecontroller.board.remove_tile_from_board(tileview.id_tile)

    # --- MÉTHODES PRIVÉES ---

    def _check_if_tile_on_board(self, id_tile: str) -> bool:
        """
        Checks if a tile with the specified ID is currently on the
        board.

        Args:
            id_tile (str): The ID of the tile to check.

        Returns:
            bool: True if the tile is on the board, False otherwise.
        """
        return any(tile.id_tile == id_tile
                    for army in self.gamecontroller.board.armies
                    for tile in self.gamecontroller.board.tiles[army]
                )

    def _get_info_from_id_tile(self, id_tile: str) -> Dict:
        """
        Retrieves information about a tile using its ID.

        Args:
            id_tile (str): The ID of the tile.

        Returns:
            Dict: A dictionary containing the tile's attributes.
        Raises:
            ValueError: if tile not found
        """
        try:
            tile = next(tile for tile in self.gamecontroller.board.all_tile
                        if tile.id_tile == id_tile)
            return tile.__dict__
        except StopIteration:
            raise ValueError(
                "ID tile incorrect or no tile with the given ID exists."
                )

    def _get_one_view_tile(self, id_tile: str) -> Optional[TileView]:
        """
        Retrieves a `TileView` object for a tile currently displayed on
        the board view (tiles_board sprites group).

        Args:
            id_tile (str): The ID of the tile.

        Returns:
            Optional[TileView]: 
                The `TileView` object if the tile is on the board view,
                or None if not found.
        """
        return next(
                    (tileview
                    for tileview in self.gamecontroller.view.tiles_board
                    if tileview.id_tile == id_tile),
                    None
                )

    def _update_unite_with_movement(self, player: Player):
        """
        Marks units with movement capabilities and add them in the
        sprite group `tiles_board_moving`, allowing them to move on the
        board.

        Args:
            player (Player): The player whose units are being updated.
        """
        moving_units = (
            tilemodel for tilemodel in self.gamecontroller.board.tiles[player.deck.army_name]
            if tilemodel.special_capacities
            and "movement" in tilemodel.special_capacities
        )

        for tilemodel in moving_units:
            tileview = self._get_one_view_tile(tilemodel.id_tile)
            if tileview and tileview not in self.gamecontroller.view.tiles_hand:
                self.gamecontroller.view.tiles_board_moving.add(tileview)

    def _update_tile_model(self,
                        id_tile: str,
                        pixel_position: tuple,
                        angle_index: Literal[0, 1, 2, 3, 4, 5]
                    ) -> None:
        """
        Updates the model state of a tile based on its ID, new position,
        and new rotation angle.

        Args:
            id_tile (str): 
                The ID of the tile being updated.
            pixel_position (tuple): 
                The new screen coordinates of the tile.
            angle_index (Literal[0, 1, 2, 3, 4, 5]): 
                The new rotation index of the tile.
        """
        tilemodel = self._get_one_model_tile(id_tile)
        cube_coordinates = coordinates_pixel_to_cube(pixel_position)

        old_board_position = tilemodel.board_position
        tilemodel.board_position = cube_coordinates
        tilemodel.rotate_tile(angle_index)

        if not self._check_if_tile_on_board(id_tile):
            self.gamecontroller.board.add_tile_to_board(tilemodel)

        else:
            self.gamecontroller.board.occupied[tilemodel.army_name].append(cube_coordinates)
            self.gamecontroller.board.occupied[tilemodel.army_name].remove(old_board_position)

            del self.gamecontroller.board.position_index[tilemodel.army_name]\
                [old_board_position]
            self.gamecontroller.board.position_index[tilemodel.army_name][cube_coordinates] \
                = tilemodel

    def _update_board_model(self) -> None:
        """
        Synchronizes the board model to match the current state of the
        board view.

        This method saves the positions and angles of all tiles
        currently displayed on the board view.
"""
        for tileview in self.gamecontroller.view.tiles_board:
            self._update_tile_model(
            id_tile=tileview.id_tile,
            pixel_position=tileview.rect.topleft,
            angle_index=tileview.angle_index
        )

    def _update_netted_unite(self) -> None:
        """
        Updates the attribut `is_netted` of enemy tiles on the board
        affected by netting mechanics.
        """
        for army in self.gamecontroller.board.armies:
            enemy_army = next_element(self.gamecontroller.board.armies, army)
            enemy_tiles = self.gamecontroller.board.position_index[enemy_army]

            for tilemodel in self.gamecontroller.board.tiles[army]:
                if not tilemodel.net_directions:
                    continue

                for net_directions in tilemodel.net_directions:
                    netted_positions = calculate_position(
                                                    net_directions,
                                                    tilemodel.board_position
                                                    )
                    if netted_positions in enemy_tiles:
                        enemy_tile = enemy_tiles[netted_positions]
                        enemy_tile.is_netted = True

    def _update_board_view(self) -> None:
        """
        Updates the board view by cleaning the discard zone and the
        sprite tile_board_moving.
        """
        self.gamecontroller.view.remove_tiles_board_moving()
        self.gamecontroller.view.get_tile_to_discard()

    def _get_one_model_tile(self, id_tile: str) -> Tile:
        """
        Retrieves a `Tile` object from the model using its ID.

        Args:
            id_tile (str): The ID of the tile.

        Returns:
            Tile: The corresponding `Tile` object.

        Raises:
            ValueError:
            If no tile with the specified ID exists on the board.
        """

        tile = next(
        (tile for tile in self.gamecontroller.board.all_tile if tile.id_tile == id_tile),
        None
    )
        if tile is None:
            raise ValueError(f"No tile found with ID '{id_tile}'.")

        return tile