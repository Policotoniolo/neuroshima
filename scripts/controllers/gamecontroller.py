import sys
import random
import pygame

from scripts.model.model import Player, HexBoard
from scripts.utils.config import BOARD_LIMIT
from scripts.view.view import View
from scripts.controllers.moduleevaluator import ModuleEvaluator
from scripts.controllers.battleevaluator import BattleEvaluator
from scripts.controllers.tilecontroller import TileController
from scripts.controllers.boardcontroller import BoardController
from scripts.controllers.playerscontroller import PlayersController
from scripts.utils.functions import *


class GameController:
    """Class game controller
    """

    def __init__(self):

        # Model
        self.players = [Player("paul", "borgo"),
                        Player("benoit", "moloch")]
        self.board = HexBoard(
                            BOARD_LIMIT,
                            armies=['borgo', 'moloch'],
                            players=self.players
                        )
        
        # View
        self.view = View()
        
        # Controller
        self.moduleevaluator = ModuleEvaluator(self)
        self.tileactioncontroller = TileController(self)
        self.boardcontroller = BoardController(self)
        self.battleevaluator = BattleEvaluator(self)
        self.playerscontroller = PlayersController(self)

    def _quitte_loop(self, event_list: List[pygame.event.Event]):
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def _set_up(self):
        self.view.display_screen()
        random.shuffle(self.players)
        

    def _end_turn(self, player: Player, event_list: List[pygame.event.Event]):
        if self.playerscontroller.end_player_turn(player, event_list):
            self.boardcontroller.update_board(player)
            return True

    def _start_game(self):
        """Initiate first turn for placing hq
        """
        for player in self.players:
            self.playerscontroller.draw_hq_tile(player)
            run = True
            while run:
                event_list = pygame.event.get()

                self._quitte_loop(event_list)

                self.playerscontroller.play_tile_hand(player, event_list)
                self.boardcontroller.update_board_view_from_hand()
                pygame.display.flip()
                
                if self._end_turn(player, event_list):
                    run = False

    def _init_view_turn(self):
        self.view.display_screen()
        self.view.display_all_sprite()

    def _init_player_turn(self, player: Player, round_iteration: int):

        if round_iteration==1 or round_iteration==2:
            self.playerscontroller.draw_tiles_hand(player, round_iteration)
        else:
            self.playerscontroller.draw_tiles_hand(player, 3)
        self.playerscontroller.prompt_deck(player)

    def _player_turn(self, player: Player, event_list):
        """generate player turn

        Args:
            player (Player): Instance of Player Class
        """

        self.view.display_screen()


        self.playerscontroller.play_tile_hand(player, event_list)
        self.boardcontroller.update_board_view_from_hand()

        self.view.generate_all_sprite_group()
        self.view.display_all_sprite()

        pygame.display.flip()

        if self._end_turn(player, event_list):
            return True



    def run(self):
        """Script running the game"""
        game_running = True
        self._set_up()
        self._start_game()

        round_iteration = 1

        while game_running:

            turn_running = True
            player = self.players[(round_iteration-1) % 2]
            
            self._init_view_turn()
            self._init_player_turn(player, round_iteration)

            while turn_running:
                event_list = pygame.event.get()

                self._quitte_loop(event_list)

                if self._player_turn(player, event_list):
                    round_iteration += 1
                    turn_running = False
