"""_summary_
"""

import sys
import random

from typing import Dict

import pygame

from model_script import Player, HexBoard
from view import View
from functions import next_element

# pylint: disable=no-member

#Board model variables.
BOARD_LIMIT = 3
DELTAS = [[1,0,-1],[0,1,-1],[-1,1,0],[-1,0,1],[0,-1,1],[1,-1,0]]


class GameController:
    """Class game controller
    """
    players: list[Player]

    def __init__(self, number_of_players=2, turn_time=60):
        # Model
        self.cfg = [{'name':'paul', 'army':'outpost_test'},
                    {'name':'benoit', 'army':'borgo_test'}]
        self.players = []
        self.number_of_players = number_of_players
        self.board = HexBoard(BOARD_LIMIT,DELTAS)
        # View
        self.view = View()
        # Controller
        # self.game_evaluator = game_evaluator
        self.turn_time = turn_time

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

    def get_info_from_id_tile(self, id_tile:str, player: Player) -> Dict :
        """retrieve informations of a tile model in a deck player from a id tile

        Args:
            id_tile (str): id tile
            player (Player): Instance of Player
        """
        for tile in player.deck.all_tiles:
            if tile.id_tile == id_tile:
                return tile.__dict__
        return {}

    def actiontile(self, player, event_list):
        """generate actions for using tile type action"""

        for tile in self.view.tiles_hand:
            tile_informations = self.get_info_from_id_tile(tile.id_tile, player)
            if tile_informations['action'] == "movement":
                self._movement_tile(tile)
            elif tile_informations['action'] == "sniper":
                self._sniper_tile(tile, player, event_list)
            elif tile_informations['action'] == "grenade":
                self._grenade_tile(tile, player, event_list)

    def _movement_tile(self, tile):
        """generate action tile of movement
        """
        if tile.drag.dragging:
            self.view.boardzone.displaygreenboard()
            self.view.displaysurf.blit(self.view.boardzone.drawsurf,(0,0))

        elif not tile.drag.dragging :
            tile_collided = pygame.sprite.spritecollideany(tile,
                                                        self.view.tiles_board,
                                                        pygame.sprite.collide_rect_ratio(0.75))
            if tile_collided is not None:
                self.view.tiles_hand.remove(tile)
                self.view.tiles_board.remove(tile_collided)
                self.view.tiles_board_moving.add(tile_collided)

    def _sniper_tile(self, tile, player, event_list):
        """Generate action tile for sniper tile
        """

        tile_collided = pygame.sprite.spritecollideany(tile,
                                                        self.view.tiles_board,
                                                        pygame.sprite.collide_rect_ratio(0.75))
        if tile.drag.dragging:
            self.view.boardzone.displaygreenboard()
            self.view.displaysurf.blit(self.view.boardzone.drawsurf,(0,0))

        if tile_collided is not None:
            next_player = next_element(self.players, player)
            tile_collided_info = self.get_info_from_id_tile(tile_collided.id_tile, next_player)
            if  tile_collided_info == {} or tile_collided_info["kind"] == "base":
                return
            else:
                if tile_collided.click_tile(event_list, self.view.displaysurf):
                    self.view.tiles_hand.remove(tile)
                    self.view.tiles_board.remove(tile_collided)
                    self.view.tiles_defausse.add(tile_collided)

    def _grenade_tile(self, tile, player, event_list):
        tile_collided = pygame.sprite.spritecollideany(tile,
                                                        self.view.tiles_board,
                                                        pygame.sprite.collide_rect_ratio(0.75))
        if tile.drag.dragging:
            self.view.boardzone.displaygreenboard()
            self.view.displaysurf.blit(self.view.boardzone.drawsurf,(0,0))

        if tile_collided is not None:
            next_player = next_element(self.players, player)
            tile_collided_info = self.get_info_from_id_tile(tile_collided.id_tile, next_player)
            if  tile_collided_info == {} or tile_collided_info["kind"] == "base":
                return
            else:
                if tile_collided.click_tile(event_list, self.view.displaysurf):
                    self.view.tiles_hand.remove(tile)
                    self.view.tiles_board.remove(tile_collided)
                    self.view.tiles_defausse.add(tile_collided)

    def _start_game(self):
        """Initiate first turn for placing hq
        """
        self.view.display_screen()
        self.board.create_board()
        random.shuffle(self.players)

        for player in self.players:

            player.deck.init_deck()
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

        self.view.move_tile_hand(event_list)
        self.view.move_tile_board(event_list)


        self.view.generate_all_sprite_group()
        self.view.display_all_sprite()

        self.actiontile(player, event_list)
        pygame.display.flip()

        if self.view.endbutton.isvalidated(event_list):

            self.view.remove_tiles_board_moving()
            self.view.get_tile_to_discard()              ##### CREER une fonction unique dans view ici
            index_tile_to_keep = self.view.get_tile_to_keep()    ##### CREER une fonction unique dans view ici
            index_tile_to_board = self.view.hand_tile_to_board() ##### CREER une fonction unique dans view ici
            for id_tile in index_tile_to_board:
                self.board.add_tile_to_board(player.hand.get_tile_by_name(id_tile))
            player.discard_tiles_hand(index_tile_to_keep)
            
            return True

    def end_turn(self, player: Player):
        """_summary_

        Args:
            player (Player): _description_
        """

    def update_board_model(self):
        """Save actual board from view into the board model
        """

        #### Save les modifications du board existant

        #### Save les changement des tiles de la main

        self.board.tiles = []
        for tile in self.view.tiles_board:
            # self.board.tiles.append(Tile())
            return




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
                    self.end_turn(player)
                    round_iteration +=1
                    run = False



if __name__ == "__main__":
    game = GameController()
    # # for elt in game.cfg:
    # #     game._add_player(elt["name"], elt['army'])
    # # game.players[0].deck.init_deck()
    # # print(game.get_info_from_id_tile('outpost-mouvement1', game.players[0])['kind'])
    game.run()
    # print(sys.path)
