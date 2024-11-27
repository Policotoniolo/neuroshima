"""_summary_
"""

import sys
import random

from typing import Dict

import pygame

from model_script import Player, HexBoard, Tile
from scripts.config import BOARD_LIMIT, BOARD_PIXEL_TO_CUBE, CUBE_DIRECTION_VECTORS
from view import View, TileView
from moduleevaluator import ModuleEvaluator
from battleevaluator import BattleEvaluator
from functions import *


class GameController:
    """Class game controller
    """
    players: list[Player]

    def __init__(self, number_of_players=2, turn_time=60):
        # Model
        self.cfg = [{'name':'paul', 'army':'borgo'}, 
                    {'name':'benoit', 'army':'moloch'}] # le choix des armées et joueur devra être amélioré. J'ai fait ça en attendant, non prio
        self.players = []
        self.number_of_players = number_of_players
        self.board = HexBoard(BOARD_LIMIT,CUBE_DIRECTION_VECTORS, armies = ['borgo', 'moloch'])
        self.all_tiles = []
        # View
        self.view = View()
        # Controller
        self.moduleevaluator = ModuleEvaluator(self.board)
        self.battleevaluator = BattleEvaluator(self.board, self.moduleevaluator, self.view)
        self.turn_time = turn_time #Pas encore utilisé, permettra de mettre un temps max par tour

    def _add_player(self, name, army_name):
        self.players.append(Player(name, army_name))

    def timer(self):
        """Function not finished yet

        Returns:
            _type_: _description_
        """
        return

    def get_id_tiles_from_hand(self, player: Player) -> list:
        """get id tile from hand player model and return a list

        Args:
            player (Player): Player class
        """
        id_tiles = []
        for tile in player.hand.tiles:
            id_tiles.append(tile.id_tile)
        return id_tiles

    def get_size_deck(self, player: Player) -> int:
        """get the number of remaining tiles in the player deck
        Args:
            player (Player): Instance of Player
        """
        return len(player.deck.tiles)

    def get_hq_tile_player(self, player: Player) -> Tile|None:
        hq_tile = self.get_one_model_tile(player.deck.army_name+"-qg")
        if hq_tile is not None:
            return hq_tile

    def get_info_from_id_tile(self, id_tile:str) -> Dict :
        """retrieve informations of a tile model in a deck player from a id tile

        Args:
            id_tile (str): id tile
            player (Player): Instance of Player
        """
        for tile in self.all_tiles:
            if tile.id_tile == id_tile:
                return tile.__dict__
        return {}

    def get_one_model_tile(self, id_tile) -> Tile|None:
        """retrieve one tile model in a deck player from a id tile

        Args:
            id_tile (str): id tile
        """
        for tile in self.all_tiles:
            if tile.id_tile == id_tile:
                return tile

    def get_one_view_tile(self, id_tile) -> TileView|None:
        """retrieve one tile view if the tile is on the board model and boardview

        Args:
            id_tiles (_type_): id_tile
        """
        for tileview in self.view.tiles_board:
            if tileview.id_tile == id_tile:
                return tileview

    def actiontile(self, player, event_list):
        """generate actions for using tile type action"""

        for tileview in self.view.tiles_hand:
            if (tileview.drag.dragging == True or 
                self.view.boardzone.single_collision(tileview)
                ):
                tile_informations = self.get_info_from_id_tile(tileview.id_tile)
                if tile_informations['action'] == "movement":
                    self._movement_tile(tileview,player ,event_list)
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
            self.view.displaysurf.blit(self.view.boardzone.drawsurf,(0,0))

        tile_collided = pygame.sprite.spritecollideany(
            tileview,
            self.view.tiles_board,
            pygame.sprite.collide_rect_ratio(0.75)
        )
        if tile_collided is not None:
            tile_collided_info = self.get_info_from_id_tile(tile_collided.id_tile)
            if  (tile_collided_info == {} or 
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
            enemy_hq_position = self.get_info_from_id_tile(enemy_army+"-qg")['board_position']
            enemies_cube_position.remove(enemy_hq_position)
            enemies_pixel_position = list_cubes_to_pixel(enemies_cube_position)
            self.view.boardzone.highlight_hexagones(enemies_pixel_position)
            self.view.displaysurf.blit(self.view.boardzone.drawsurf,(0,0))

        if tile_collided is not None:

            tile_collided_info = self.get_info_from_id_tile(tile_collided.id_tile)
            if  (tile_collided_info == {} or 
                    tile_collided_info["kind"] == "base" or 
                    tile_collided_info["army_name"] != enemy_army
                    ):
                return
            else:
                if tile_collided.click_tile(event_list, self.view.displaysurf):
                    self.view.tiles_hand.remove(tileview)
                    self.view.tiles_board.remove(tileview)
                    self.single_damage(tile_collided)

    def _grenade_tile(self, tileview: TileView, player, event_list):
        """Generate action tile for grenade tile
        """
        tile_collided = pygame.sprite.spritecollideany(tileview, # type: ignore
                                            self.view.tiles_board,
                                            pygame.sprite.collide_rect_ratio(0.75)
                                        )
        n = get_neighbors(
            self.get_hq_tile_player(player).board_position # type: ignore
            ) 
        p = list_cubes_to_pixel(n)
        if tileview.drag.dragging:
            self.view.boardzone.highlight_hexagones(p)  #not working
            self.view.displaysurf.blit(self.view.boardzone.drawsurf,(0,0))

        if tile_collided is not None:
            tile_collided_info = self.get_info_from_id_tile(tile_collided.id_tile)
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
        if tileview.drag.dragging:
            self.view.boardzone.displaygreenboard()
            self.view.displaysurf.blit(self.view.boardzone.drawsurf,(0,0))

        elif not tileview.drag.dragging:
            if self.view.boardzone.single_collision(tileview): # type: ignore
                self.launch_battle()

    def _push_tile(self, tileview: TileView, event_list):
        """Generate action for push tile

        Args:
            tileview (TileView): TileView object
            event_list (_type_): pygame events list
        """
        tile_collided = pygame.sprite.spritecollideany(
            tileview, # type: ignore
            self.view.tiles_board,
            pygame.sprite.collide_rect_ratio(0.10)
        )

        if tileview.drag.dragging:

            army = tileview.id_tile.split("-")[0]
            allies_cube_position = self.board.occupied[army]
            allies_pixel_position = list_cubes_to_pixel(allies_cube_position)
            self.view.boardzone.highlight_hexagones(allies_pixel_position)
            self.view.displaysurf.blit(self.view.boardzone.drawsurf,(0,0))

        if tile_collided is not None:
            tile_collided_info = self.get_info_from_id_tile(tile_collided.id_tile)
            if  (tile_collided_info == {} or 
                    tile_collided_info['army_name'] != tileview.id_tile.split("-")[0] 
                    ):
                return
            else:
                n_tile_collided = get_neighbors(tile_collided_info['board_position'])
                p_tile_collided = list_cubes_to_pixel(n_tile_collided)
                hexagone = self.view.boardzone.highlight_and_click_hexagones(
                    p_tile_collided, 
                    event_list
                )
                self.view.displaysurf.blit(self.view.boardzone.drawsurf,(0,0))
                if hexagone is not None:
                    enemy_tileview = pygame.sprite.spritecollideany(
                        hexagone, # type: ignore
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
    (376,284),(376,369),(451,241),(451,327),(450,413),(525,370),(525,284)
        ]
        inner_hexagones_board = self.view.boardzone.get_multiple_hexa(
            inner_board_positions
            )
        hexagone_collided = pygame.sprite.spritecollideany(
            tileview, # type: ignore
            inner_hexagones_board # type: ignore
        ) 
        if tileview.drag.dragging:
            self.view.boardzone.highlight_hexagones(inner_board_positions)
            self.view.displaysurf.blit(self.view.boardzone.drawsurf,(0,0))
        elif not tileview.drag.dragging:
            self.view.boardzone.drawsurf.fill((pygame.Color('#00000000')))
            self.view.displaysurf.blit(self.view.boardzone.drawsurf,(0,0))

        if hexagone_collided is not None:
            self.view.boardzone.highlight_neighbors_hexagone(hexagone_collided, "red")
            self.view.displaysurf.blit(self.view.boardzone.drawsurf,(0,0))

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

    def _start_game(self):
        """Initiate first turn for placing hq
        """
        self.view.display_screen()
        self.board.create_board()
        random.shuffle(self.players)

        for player in self.players:

            player.deck.init_deck()
            self.all_tiles = self.all_tiles + player.deck.tiles
            player.get_tiles(1)

            id_tiles = self.get_id_tiles_from_hand(player)
            self.view.get_tiles_hand(id_tiles)

            run = True
            while run:

                event_list = pygame.event.get()
                for event in event_list:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                self.view.move_tile_hand(event_list)

                self.view.generate_all_sprite_group()
                self.view.display_all_sprite()
                pygame.display.flip()

                if self.view.endbutton.isvalidated(event_list):
                    run = False
                    self.view.hand_tile_to_board()
                    player.discard_tiles_hand(id_tiles_to_keep=[])
                    self.update_board_model()

            player.deck.shuffle_deck()

    def init_player_turn(self, player: Player, round_iteration: int):
        """Initiate player turn

        Args:
            player (Player): Instance of Player Class
            round_iteration (int): Round number
        """
        if round_iteration == 0:
            player.get_tiles(1)
            id_tiles = self.get_id_tiles_from_hand(player)
            self.view.get_tiles_hand(id_tiles)
        elif round_iteration == 1:
            player.get_tiles(2)
            id_tiles = self.get_id_tiles_from_hand(player)
            self.view.get_tiles_hand(id_tiles)
        else:
            player.get_tiles(3)
            id_tiles = self.get_id_tiles_from_hand(player)
            self.view.get_tiles_hand(id_tiles)

    def player_turn(self, player: Player, event_list):
        """generate player turn

        Args:
            player (Player): Instance of Player Class
        """

        self.view.display_screen()
        
        self.update_unite_with_movement(player)
        self.view.move_tile_hand(event_list)
        self.view.move_tile_board(event_list)
        self.update_board_view_from_hand()

        self.view.generate_all_sprite_group()
        self.view.display_all_sprite()

        self.actiontile(player, event_list)

        pygame.display.flip()

        if self.view.endbutton.isvalidated(event_list):

            self.view.remove_tiles_board_moving()
            self.view.get_tile_to_discard()              
            id_tileviews_to_keep = self.view.get_id_tile_to_keep() 
            player.discard_tiles_hand(id_tileviews_to_keep)
            self.update_board_model()
            self.update_netted_unite(player)
            return True

    def update_tile_model(self, id_tile: str, pixel_position: tuple, angle_index: int) -> None:
        """Update a tile on the baord model

        Args:
            id_tile (str): id of the tile
            pixel_position (tuple): Pixel position on the screen
            angle_index (int): Index of the angle of the tile
        """
        tilemodel = self.get_one_model_tile(id_tile)
        self.board.add_tile_to_board(tilemodel)
        cube_coordinates = coordinates_pixel_to_cube(pixel_position)
        if tilemodel is not None and cube_coordinates is not None:
            old_board_position = tilemodel.board_position

            tilemodel.board_position = cube_coordinates # type: ignore
            tilemodel.rotate_tile(angle_index)

            self.board.occupied[tilemodel.army_name].append(cube_coordinates)
            self.board.occupied[tilemodel.army_name].remove(old_board_position)

    def update_board_model(self):
        """Save actual board from view into the board model
        """
        for tileview in self.view.tiles_board:
            id_tile = tileview.id_tile
            pixel_position = tileview.rect.topleft
            angle_index = tileview.angle_index
            self.update_tile_model(id_tile, pixel_position, angle_index)

    def update_netted_unite(self, player: Player):

        for tilemodel in self.board.tiles[player.deck.army_name]:
            if tilemodel.net is not None:
                for net_directions in tilemodel.net:
                    netted_positions = tuple(map(sum, 
                                                    zip(net_directions, 
                                                        tilemodel.board_position
                                                        )
                                                    )
                                            )
                    if netted_positions in self.board.occupied[
                        next_element(self.board.armies, player.deck.army_name)]:

                        index = self.board.occupied[
                        next_element(self.board.armies, player.deck.army_name)].index(netted_positions)
                        enemy_tile = self.board.tiles[
                        next_element(self.board.armies, player.deck.army_name)][index]
                        enemy_tile.is_netted = True
        

    def update_unite_with_movement(self, player: Player):
        for tilemodel in self.board.tiles[player.deck.army_name]:
            if (tilemodel.special_capacities is not None and
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
                        self.update_tile_model(tileview.id_tile, tileview.rect.topleft, tileview.angle_index)
                else:
                    self.view.tiles_board.remove(tileview)
                    self.board.remove_tile_from_board(tileview.id_tile)


    def run(self):
        """Script running the game"""

        for elt in self.cfg:
            self._add_player(elt["name"], elt['army'])

        self._start_game()
        round_iteration = 0
        run = True

        while True:
            run = True
            self.view.display_screen()
            self.view.display_all_sprite()
            player = self.players[round_iteration%2]

            self.init_player_turn(player, round_iteration)
            self.view.get_tiles_deck(self.get_size_deck(player))

            while run:
                event_list = pygame.event.get()
                for event in event_list:

                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        sys.exit()

                if self.player_turn(player, event_list):
                    round_iteration +=1
                    run = False


if __name__ == "__main__":
    game = GameController()
    game.run()
