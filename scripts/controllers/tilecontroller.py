import pygame
from typing import List, Optional

from scripts.model.model import HexBoard, Player, Tile
# from scripts.controllers import gamecontroler
from scripts.view.view import View, TileView
from scripts.utils.functions import *
from scripts.utils.config import *


class TileController:
    """ 
    Handles interactions and actions involving tiles on the board.

    This controller is responsible for managing the behavior of tiles
    during gameplay, including movement, damage, and other specific 
    actions.

    Attributes
    ----------
    board : HexBoard
        The game board containing tiles and their positions.
    view : View
        The graphical interface providing user interactions and
        feedback.
    gamecontroller : GameController
        Main controller.

    Methods
    -------
    get_tile_info(id_tile: str) -> dict:
        Retrieves the attributes of a tile by its unique ID.
    get_one_model_tile(id_tile: str) -> Tile:
        Retrieves a `Tile` object from the model using its ID.
    actiontile(player: Player, event_list: List[pygame.event.Event]
        ) -> None:
        Executes actions for tiles with specific action types.
    single_damage(tileview: TileView) -> None:
        Inflicts one damage on a tile and updates the model.
    launch_battle(event_list: List[pygame.event.Event]) -> None:
        Placeholder method to handle battle initiation.

    Private Methods
    ---------------
    _movement_tile(tileview: TileView, player: Player,\
        event_list: List[pygame.event.Event]) -> None:
        Handles movement action tile.
    _sniper_tile(player: Player, tileview: TileView, \
        event_list: List[pygame.event.Event]) -> None:
        Handles the sniper action tile.
    _grenade_tile(tileview: TileView, player: Player,\
        event_list: List[pygame.event.Event]) -> None:
        Handles the grenade action tile.
    _battle_tile(tileview: TileView, \
        event_list: List[pygame.event.Event]) -> None:
        Handles the battle action tile.
    _push_tile(player: Player, tileview: TileView,\
        event_list: List[pygame.event.Event]) -> None:
        Handles the push action tile.
    _airstrike_tile(tileview: TileView,\
        event_list: List[pygame.event.Event]) -> None:
        Handles the airstrike action tile.
    _highlight_army(self, player: Player) -> None:
        Highlight an army on the board.
    _check_tileview_criteria(self,
                            player: Player,
                            tileview:TileView,
                            is_ally: bool,
                            kind_filter:List[str],   
                            position_filter: List[Tuple[int, int, int]]                         
                            ) -> bool:
        Check if a tileview respects criteria.
        Return True if all criteria are respected
    _get_neighbors_tile_enemies_position(self,
                            player: Player,
                            id_tile: str
                        )-> Optional[List[Tuple[int, int]]]:
        Find pixel positions of the enemy tiles around a player's tile.
    """

    def __init__(self,
                board: HexBoard,
                view: View,
                gamecontroller
            ) -> None:
        """
        Initializes the controller with a game board and the view.

        Args:
            board (HexBoard): 
                Game Board model.
            view (View): 
                Graphical interface for user interactions and feedback.
            gamecontroller (GameController): Main controller.
        """
        self.board = board
        self.view = view
        self.gamecontroller = gamecontroller

    def get_tile_info(self, id_tile: str) -> dict:
        """
        Retrieves information about a tile by its ID.

        Args:
            id_tile (str): The unique identifier of the tile.

        Returns:
            dict: A dictionary containing the tile's attributes.
        Raises:
            ValueError: if no tile with the ID.
        """
        try:
            tile = next(tile for tile in self.board.all_tile
                        if tile.id_tile == id_tile)
            return tile.__dict__
        except StopIteration:
            raise ValueError(
                "ID tile incorrect or no tile with the given ID exists."
                )

    def get_one_model_tile(self, id_tile: str) -> Tile:
        """
        Retrieves the Tile model object corresponding to a given tile
        ID.

        Args:
            id_tile (str): The unique identifier of the tile.

        Returns:
            Tile: The Tile object matching the ID.

        Raises:
            ValueError: If no tile with the given ID exists.
        """
        tile = next(
        (tile for tile in self.board.all_tile if tile.id_tile == id_tile),
        None
    )
        if tile is None:
            raise ValueError(f"No tile found with ID '{id_tile}'.")

        return tile

    def _check_tileview_criteria(self,
                player: Player,
                tileview:TileView,
                is_ally: Optional[bool] = None,
                kind_filter:Optional[List[str]] = None,   
                position_filter: Optional[List[Tuple[int, int, int]]] = None                      
                ) -> bool:
        """
        Check if a tileview respects criteria.
        Return True if all criteria are respected

        Args:
            player (Player): 
                Player used for check.
            tileview (TileView): 
                The tileview to check.
            is_ally (Optional[bool]): 
                if True, check if the tile is in the player army.
                if False, check if the tile is in the enemy player army.
            kind_filter (Optional[List[str]]): 
                Check if the kind of the is in this list.
            position_filter (Optional[List[Tuple[int, int, int]]]):
                Check if the board position of the tile is in the 
                positions list
        """
        tile_info = self.get_tile_info(tileview.id_tile)

        # Check if the tile belongs to the correct army
        if is_ally is True:
            if tile_info['army_name'] != player.deck.army_name:
                return False
        elif is_ally is False:
            enemy_player = next_element(self.gamecontroller.players, player)
            if tile_info['army_name'] != enemy_player.deck.army_name:
                return False

        # Check if the kind of the tile is in the kind_filter list
        if kind_filter and tile_info['kind'] not in kind_filter:
            return False

        # Check if the board position of the tile is in the position_filter
        if position_filter and tile_info['board_position'] \
            not in position_filter:
            return False

        return True

    def _highlight_army(self,
                        player: Player,
                        show_hq: bool = True,
                        show_enemy: bool = False
                    ) -> None:
        """
        Highlights an army's positions on the board.

        Args:
            player (Player): 
                The player whose army positions are being highlighted.
            show_hq (bool, optional): 
                If True, highlights the player's headquarters (HQ). 
                Default is True.
            show_enemy (bool, optional): 
                If True, highlights the positions of the enemy player's
                army instead of the current player's army.
                Default is False.
            """
        if show_enemy:
            player = next_element(self.gamecontroller.players, player)

        army =  player.deck.army_name
        army_cube_position = self.board.occupied[army].copy()

        if not show_hq:
            hq_tile_position = player.deck.hq_tile.board_position
            army_cube_position.remove(hq_tile_position)

        army_pixel_position = list_cubes_to_pixel(army_cube_position)
        self.view.boardzone.highlight_hexagones(army_pixel_position)
        self.view.displaysurf.blit(self.view.boardzone.drawsurf, (0, 0))

    def actiontile(self, player: Player, event_list: List[pygame.event.Event]
                ) -> None:
        """
        Executes actions for tiles with specific action types.

        Iterates over tiles in the player's hand, detects interaction
        (dragging or collision), and triggers the appropriate action.

        Args:
            player (Player):
                The player performing the action.
            event_list (List[pygame.event.Event]):
                A list of pygame events.
        """
        action_map = {
        "movement": lambda tile: self._movement_tile(tile, player, event_list),
        "sniper": lambda tile: self._sniper_tile(player, tile, event_list),
        "grenade": lambda tile: self._grenade_tile(tile, player, event_list),
        "battle": self._battle_tile,
        "push": lambda tile: self._push_tile(player, tile, event_list),
        "airstrike": lambda tile: self._airstrike_tile(tile, event_list),
        }

        for tileview in self.view.tiles_hand:
            if tileview.manipulator.dragging \
                or self.view.boardzone.single_collision(tileview):
                tile_informations = self.get_tile_info(tileview.id_tile)
                action_type = tile_informations.get("action")

                if action_type in action_map:
                    action_map[action_type](tileview)

    def _movement_tile(self,
                    tileview: TileView,
                    player: Player,
                    event_list: List[pygame.event.Event]
                ) -> None:
        """
        Handles movement action tile.

        Args:
            tileview (TileView):
                The tile being moved.
            player (Player):
                The player executing the action.
            event_list (List[pygame.event.Event]):
                A list of pygame events.
        """
        if tileview.manipulator.dragging:
            self._highlight_army(player, show_hq=True)

        tile_collided = pygame.sprite.spritecollideany(
            tileview, # type: ignore
            self.view.tiles_board,
            pygame.sprite.collide_rect_ratio(0.75)
        )
        if tile_collided:
            if not self._check_tileview_criteria(player,
                                                tile_collided,
                                                is_ally=True):
                return
            else:
                if tile_collided.click_tile(event_list, self.view.displaysurf):
                    self.view.tiles_hand.remove(tileview)
                    self.view.tiles_board.remove(tileview)
                    self.view.tiles_board.remove(tile_collided)
                    self.view.tiles_board_moving.add(tile_collided)

    def _sniper_tile(self,
                    player: Player,
                    tileview: TileView,
                    event_list: List[pygame.event.Event]
                ) -> None:
        """
        Handles the sniper action tile.

        Args:
            player (Player):
                The player executing the action.
            tileview (TileView):
                The sniper tile being used.
            event_list (List[pygame.event.Event]): 
                A list of pygame events.
        """
        tile_collided = pygame.sprite.spritecollideany(
            tileview, # type: ignore
            self.view.tiles_board,
            pygame.sprite.collide_rect_ratio(0.75)
        )

        if tileview.manipulator.dragging:
            self._highlight_army(player, False, True)

        if tile_collided:
            if not self._check_tileview_criteria(player, 
                                                tile_collided,
                                                is_ally=False,
                                                kind_filter=["unite, module"]
                                            ):
                return
            else:
                if tile_collided.click_tile(event_list, self.view.displaysurf):
                    self.view.tiles_hand.remove(tileview)
                    self.view.tiles_board.remove(tileview)
                    self.single_damage(tile_collided)

    def _grenade_tile(self,
                    tileview: TileView,
                    player: Player,
                    event_list: List[pygame.event.Event]
                ) -> None:
        """
        Handles the grenade action tile.

        Args:
            tileview (TileView): The grenade tile being used.
            player (Player): The player executing the action.
            event_list (List[pygame.event.Event]): A list of pygame events.
        """
        tile_collided = pygame.sprite.spritecollideany(
            tileview, # type: ignore
            self.view.tiles_board,
            pygame.sprite.collide_rect_ratio(0.75)
        )
        n = get_neighbors_hex_positions(player.deck.hq_tile.board_position)
        p = list_cubes_to_pixel(n)
        if tileview.manipulator.dragging:
            self.view.boardzone.highlight_hexagones(p)
            self.view.displaysurf.blit(self.view.boardzone.drawsurf, (0, 0))

        if tile_collided:
            if not self._check_tileview_criteria(player,
                                                tile_collided, 
                                                is_ally=False,
                                                kind_filter=["unite, module"],
                                                position_filter=n
                                            ):
                return
            else:
                if tile_collided.click_tile(event_list, self.view.displaysurf):
                    self.view.tiles_hand.remove(tileview)
                    self.single_damage(tile_collided)

    def _battle_tile(self,
                    tileview: TileView,
                    event_list: List[pygame.event.Event]
                ) -> None:
        """
        Handles the battle action tile.

        Args:
            tileview (TileView): The battle tile being used.
            event_list (List[pygame.event.Event]): List of pygame events
        """
        if tileview.manipulator.dragging:
            self.view.boardzone.displaygreenboard()
            self.view.displaysurf.blit(self.view.boardzone.drawsurf, (0, 0))

        elif not tileview.manipulator.dragging:
            if self.view.boardzone.single_collision(tileview): # type: ignore
                self.launch_battle(event_list)

    def _push_tile(self,
                player: Player,
                tileview: TileView,
                event_list: List[pygame.event.Event]
            ) -> None:
        """
        Handles the push action tile.

        Args:
            player (Player):
                The player executing the action.
            tileview (TileView):
                The push tile being used.
            event_list (List[pygame.event.Event]):
                A list of pygame events.
        """
        tile_collided = pygame.sprite.spritecollideany(
            tileview, # type: ignore
            self.view.tiles_board,
            pygame.sprite.collide_rect_ratio(0.10)
        )
        
        if tileview.manipulator.dragging:
            self._highlight_army(player)

        if tile_collided:
            enemies_pixel_position = self._get_neighbors_tile_enemies_position(
                                                        player,
                                                        tile_collided.id_tile
                                                    )
            if enemies_pixel_position is None:
                return

            if not self._check_tileview_criteria(
                player,
                tile_collided,
                is_ally=True,
                ):
                return
            else:
                hexagone = self.view.boardzone.highlight_and_click_hexagones(
                                                    enemies_pixel_position,
                                                    event_list
                                                )
                self.view.displaysurf.blit(self.view.boardzone.drawsurf, (0, 0)
                                        )
                if hexagone:
                    enemy_tileview = pygame.sprite.spritecollideany(
                        hexagone, # type: ignore
                        self.view.tiles_board
                    )
                    self.view.tiles_hand.remove(tileview)
                    self.view.tiles_board.remove(enemy_tileview)
                    self.view.tiles_board_moving.add(enemy_tileview)

    def _airstrike_tile(self,
                        tileview: TileView,
                        event_list: List[pygame.event.Event]
                    ) -> None:
        """
        Handles the airstrike action tile.

        Args:
            tileview (TileView):
                The airstrike tile being used.
            event_list (List[pygame.event.Event]):
                A list of pygame events.
        """
        inner_hexagones_board = self.view.boardzone.get_multiple_hexa(
            INNER_BOARD_PIXEL_POSITIONS
        )
        
        hexagone_collided = pygame.sprite.spritecollideany(
            tileview, # type: ignore 
            inner_hexagones_board # type: ignore
        )
        if tileview.manipulator.dragging:
            self.view.boardzone.highlight_hexagones(INNER_BOARD_PIXEL_POSITIONS)
            self.view.displaysurf.blit(self.view.boardzone.drawsurf, (0, 0))
        elif not tileview.manipulator.dragging:
            self.view.boardzone.drawsurf.fill((pygame.Color('#00000000')))
            self.view.displaysurf.blit(self.view.boardzone.drawsurf, (0, 0))

        if hexagone_collided:
            self.view.boardzone.highlight_neighbors_hexagone(
                hexagone_collided, "red")
            self.view.displaysurf.blit(self.view.boardzone.drawsurf, (0, 0))

            if tileview.click_tile(event_list, self.view.displaysurf):
                self.view.tiles_hand.remove(tileview)
                hexagone_damaged = self.view.boardzone.get_neighbors_hexagone(
                    hexagone_collided
                )
                for tile in self.view.tiles_board:
                    if (pygame.sprite.spritecollideany(
                        tile,
                        hexagone_damaged) is not None # type: ignore
                            and tile.id_tile.split('-')[1] != "qg"):
                        self.single_damage(tile)

    def launch_battle(self, event_list: List[pygame.event.Event]):
        """
        Handles the push action tile.
        """
        self.gamecontroller.battleevaluator.run_battle(event_list)

    def single_damage(self, tileview: TileView) -> None:
        """
        Generate one damage on a tileview and update model.
        Use for action tile

        Args:
            tileview (TileView): Tileview to damage
        """
        tilemodel = self.get_one_model_tile(tileview.id_tile)
        if tilemodel.life_point:
            tilemodel.life_point = tilemodel.life_point-1
            if tilemodel.life_point <= 0:
                self.view.tiles_board.remove(tileview)
                self.board.remove_tile_from_board(tileview.id_tile)

    def _get_neighbors_tile_enemies_position(self,
                            player: Player,
                            id_tile: str
                        )-> Optional[List[Tuple[int, int]]]:
        """
        Find pixel positions of the enemy tiles around a player's tile.


        Args:
            player (Player): Player whose the tile is used.
            id_tile (str): ID of the tile.

        Returns:
            Optional[List[Tuple]]: List of pixel position.
        """
        enemy_army = next_element(
                            self.gamecontroller.players, player
                        ).deck.army_name
    
        tile_collided_info = self.get_tile_info(id_tile)

        neighbors_enemies_positions = [
            position for position in get_neighbors_hex_positions(
                                        tile_collided_info['board_position']
                                    )
            if position in self.board.position_index[enemy_army]
        ]

        if neighbors_enemies_positions == []:
            return None

        neighbors_enemies_positions = list_cubes_to_pixel(
            neighbors_enemies_positions
        )
        return neighbors_enemies_positions