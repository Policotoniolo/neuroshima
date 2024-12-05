import pygame
from typing import List

from scripts.model.model import HexBoard, Player, Tile
from scripts.view.view import View, TileView
from scripts.utils.functions import *


class TileController:
    def __init__(self, board: HexBoard, view: View) -> None:
        """
        Initializes the Tile action controller with a game board.

        Args:
            board (HexBoard): Game Board
        """
        self.board = board
        self.view = view

    def get_tile_info(self, id_tile: str):
        for tile in self.board.all_tile:
            if tile.id_tile == id_tile:
                return tile.__dict__
        return {}

    def get_one_model_tile(self, id_tile: str) -> Tile:
        for tile in self.board.all_tile:
            if tile.id_tile == id_tile:
                return tile
        raise ValueError("ID tile incorrect or no tile with this ID.")


    def actiontile(self, player: Player, event_list: List[pygame.event.Event]):
        """generate actions for using tile type action"""

        for tileview in self.view.tiles_hand:
            if (tileview.drag.dragging == True or
                    self.view.boardzone.single_collision(tileview)
                ):
                tile_informations = self.get_tile_info(tileview.id_tile)
                if tile_informations['action'] == "movement":
                    self._movement_tile(tileview, player, event_list)
                elif tile_informations['action'] == "sniper":
                    self._sniper_tile(tileview, event_list)
                elif tile_informations['action'] == "grenade":
                    self._grenade_tile(tileview, player, event_list)
                elif tile_informations['action'] == "battle":
                    self._battle_tile(tileview)
                elif tile_informations['action'] == "push":
                    self._push_tile(tileview, event_list)
                elif tile_informations['action'] == "airstrike":
                    self._airstrike_tile(tileview, event_list)

    def _movement_tile(self, tileview, player, event_list):
        """generate action tile of movement
        """
        if tileview.drag.dragging:
            army = player.deck.army_name
            army_cube_position = self.board.occupied[army]
            army_pixel_position = list_cubes_to_pixel(army_cube_position)
            self.view.boardzone.highlight_hexagones(army_pixel_position)
            self.view.displaysurf.blit(self.view.boardzone.drawsurf, (0, 0))

        tile_collided = pygame.sprite.spritecollideany(
            tileview,
            self.view.tiles_board,
            pygame.sprite.collide_rect_ratio(0.75)
        )
        if tile_collided is not None:
            tile_collided_info = self.get_tile_info(tile_collided.id_tile)
            if (tile_collided_info == {} or
                    tile_collided_info['army_name'] != player.deck.army_name
                    ):
                return
            else:
                if tile_collided.click_tile(event_list, self.view.displaysurf):
                    self.view.tiles_hand.remove(tileview)
                    self.view.tiles_board.remove(tileview)
                    self.view.tiles_board.remove(tile_collided)
                    self.view.tiles_board_moving.add(tile_collided)

    def _sniper_tile(self, tileview, event_list):
        """Generate action tile for sniper tile
        """
        army = tileview.id_tile.split("-")[0]
        enemy_army = next_element(self.board.armies, army)

        tile_collided = pygame.sprite.spritecollideany(
            tileview,
            self.view.tiles_board,
            pygame.sprite.collide_rect_ratio(0.75)
        )

        if tileview.drag.dragging:

            enemies_cube_position = self.board.occupied[enemy_army].copy()
            enemy_hq_position = self.get_tile_info(
                enemy_army+"-qg")['board_position']
            enemies_cube_position.remove(enemy_hq_position)
            enemies_pixel_position = list_cubes_to_pixel(enemies_cube_position)
            self.view.boardzone.highlight_hexagones(enemies_pixel_position)
            self.view.displaysurf.blit(self.view.boardzone.drawsurf, (0, 0))

        if tile_collided is not None:

            tile_collided_info = self.get_tile_info(
                tile_collided.id_tile)
            if (tile_collided_info == {} or
                    tile_collided_info["kind"] == "base" or
                    tile_collided_info["army_name"] != enemy_army
                    ):
                return
            else:
                if tile_collided.click_tile(event_list, self.view.displaysurf):
                    self.view.tiles_hand.remove(tileview)
                    self.view.tiles_board.remove(tileview)
                    self.single_damage(tile_collided)

    def _grenade_tile(self, tileview: TileView, player: Player, event_list):
        """Generate action tile for grenade tile
        """
        tile_collided = pygame.sprite.spritecollideany(tileview,
                                                       self.view.tiles_board,
                                                       pygame.sprite.collide_rect_ratio(
                                                           0.75)
                                                       )
        n = get_neighbors_hex_positions(
            player.deck.hq_tile.board_position
        )
        p = list_cubes_to_pixel(n)
        if tileview.manipulator.dragging:
            self.view.boardzone.highlight_hexagones(p)  # not working
            self.view.displaysurf.blit(self.view.boardzone.drawsurf, (0, 0))

        if tile_collided is not None:
            tile_collided_info = self.get_tile_info(
                tile_collided.id_tile)
            if (tile_collided_info == {} or
                        tile_collided_info["kind"] == "base" or
                        tile_collided_info['army_name'] == player.deck.army_name or
                        tile_collided_info['board_position'] not in n
                    ):
                return
            else:
                if tile_collided.click_tile(event_list, self.view.displaysurf):
                    self.view.tiles_hand.remove(tileview)
                    self.single_damage(tile_collided)

    def _battle_tile(self, tileview: TileView):
        """Generate action for battle tile

        Args:
            tileview (TileView): TileView object
        """
        if tileview.manipulator.dragging:
            self.view.boardzone.displaygreenboard()
            self.view.displaysurf.blit(self.view.boardzone.drawsurf, (0, 0))

        elif not tileview.manipulator.dragging:
            if self.view.boardzone.single_collision(tileview):
                self.launch_battle()

    def _push_tile(self, tileview: TileView, event_list):
        """Generate action for push tile

        Args:
            tileview (TileView): TileView object
            event_list (_type_): pygame events list
        """
        tile_collided = pygame.sprite.spritecollideany(
            tileview,
            self.view.tiles_board,
            pygame.sprite.collide_rect_ratio(0.10)
        )

        if tileview.manipulator.dragging:

            army = tileview.id_tile.split("-")[0]
            allies_cube_position = self.board.occupied[army]
            allies_pixel_position = list_cubes_to_pixel(allies_cube_position)
            self.view.boardzone.highlight_hexagones(allies_pixel_position)
            self.view.displaysurf.blit(self.view.boardzone.drawsurf, (0, 0))

        if tile_collided is not None:
            tile_collided_info = self.get_tile_info(
                tile_collided.id_tile)
            if (tile_collided_info == {} or
                    tile_collided_info['army_name'] != tileview.id_tile.split(
                    "-")[0]
                    ):
                return
            else:
                n_tile_collided = get_neighbors_hex_positions(
                    tile_collided_info['board_position'])
                p_tile_collided = list_cubes_to_pixel(n_tile_collided)
                hexagone = self.view.boardzone.highlight_and_click_hexagones(
                    p_tile_collided,
                    event_list
                )
                self.view.displaysurf.blit(
                    self.view.boardzone.drawsurf, (0, 0))
                if hexagone is not None:
                    enemy_tileview = pygame.sprite.spritecollideany(
                        hexagone,
                        self.view.tiles_board
                    )
                    self.view.tiles_hand.remove(tileview)
                    self.view.tiles_board.remove(enemy_tileview)
                    self.view.tiles_board_moving.add(enemy_tileview)

    def _airstrike_tile(self, tileview: TileView, event_list):
        """Generate action for airstrike tile

        Args:
            tileview (TileView): TileView object
            event_list (_type_): pygame events list
        """
        inner_board_positions = [
            (376, 284), (376, 369), (451, 241), (451,
                                                 327), (450, 413), (525, 370), (525, 284)
        ]
        inner_hexagones_board = self.view.boardzone.get_multiple_hexa(
            inner_board_positions
        )
        hexagone_collided = pygame.sprite.spritecollideany(
            tileview,
            inner_hexagones_board
        )
        if tileview.manipulator.dragging:
            self.view.boardzone.highlight_hexagones(inner_board_positions)
            self.view.displaysurf.blit(self.view.boardzone.drawsurf, (0, 0))
        elif not tileview.manipulator.dragging:
            self.view.boardzone.drawsurf.fill((pygame.Color('#00000000')))
            self.view.displaysurf.blit(self.view.boardzone.drawsurf, (0, 0))

        if hexagone_collided is not None:
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
                        hexagone_damaged) is not None
                            and tile.id_tile.split('-')[1] != "qg"):
                        self.single_damage(tile)

    def launch_battle(self):
        print("BATTLE !")
        return

    def single_damage(self, tileview: TileView) -> None:
        """generate one damage on a tileview and update model. Use for action tile

        Args:
            tileview (TileView): Tileview to damage
        """
        tilemodel = self.get_one_model_tile(tileview.id_tile)
        if tilemodel is not None and tilemodel.life_point is not None:
            tilemodel.life_point = tilemodel.life_point-1
            if tilemodel.life_point <= 0:
                self.view.tiles_board.remove(tileview)
                self.board.remove_tile_from_board(tileview.id_tile)
