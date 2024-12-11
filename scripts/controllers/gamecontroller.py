import sys
import random
import pygame
from typing import Optional

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
    """
    The GameController class orchestrates the main gameplay logic of
    Neuroshima game. It integrates the model, view, and controller
    components to manage the game flow

    Attributes
    ----------
    players (List[Player]): 
        A list of Player instances representing the players in the game.
    board (HexBoard): 
        An instance of HexBoard that manages the game board state and
        configuration.
    view (View): 
        The visual representation of the game, including screen and
        sprite management.
    moduleevaluator (ModuleEvaluator): 
        Handles evaluation of specific modules in the game.
    tileactioncontroller (TileController): 
        Manages tile-specific actions, such as movement or special
        abilities.
    boardcontroller (BoardController): 
        Responsible for handling board updates and interactions.
    battleevaluator (BattleEvaluator): 
        Evaluates battles between players on the board.
    playerscontroller (PlayersController): 
        Handles player-specific actions, such as drawing tiles or
        ending turns.

    Methods
    ----------
    run() -> None:
        Executes the main game loop, managing the sequence of turns and
        rounds.

    Private Methods
    ----------
        _quitte_loop(event_list: List[pygame.event.Event]) -> None:
            Checks for quit events in the event list and exits the game
            if triggered.
        
        _set_up() -> None:
            Initializes the game setup, including shuffling players and
            displaying the screen.
        
        _end_turn(player: Player, event_list: List[pygame.event.Event]
            ) -> Optional[bool]:
            Ends the current player's turn, updating the board and
            handling turn logic.

        _start_game() -> None:
            Initiates the first turn, where players place their
            headquarters tiles on the board.
        
        _init_view_turn() -> None:
            Prepares the view for the start of a player's turn,
            updating the display.

        _init_player_turn(player: Player, round_iteration: int) -> None:
            Initializes the turn for a specific player, including
            drawing tiles and displaying the deck.
        
        _player_turn(player: Player,
        event_list: List[pygame.event.Event]) -> Optional[bool]:
            Executes the logic for a player's turn, including playing
            tiles and updating the board.

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

    def _quitte_loop(self, event_list: List[pygame.event.Event]) -> None:
        """
        Checks for quit events in the event list and exits the game if
        triggered.

        Args:
            event_list (List[pygame.event.Event]): 
                List of pygame events to check.
        """
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def _set_up(self) -> None:
        """
        Sets up the initial game state by displaying the screen 
        and shuffling the players' order.
        """
        self.view.display_screen()
        random.shuffle(self.players)
        

    def _end_turn(self, player: Player, event_list: List[pygame.event.Event]
                ) -> Optional[bool]:
        """
        Ends the current player's turn, updating the board and handling
        end-turn logic.

        Args:
            player (Player):
                The player whose turn is ending.
            event_list (List[pygame.event.Event]):
                List of pygame events.

        Returns:
            bool: True if the turn ends successfully.
        """
        if self.playerscontroller.end_player_turn(player, event_list):
            self.boardcontroller.update_board(player)
            return True

    def _start_game(self) -> None:
        """
        Initiates the first phase of the game, where players place
        their HQ tiles.
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

    def _init_view_turn(self) -> None:
        """
        Prepares the view for a new player's turn by updating and
        displaying all sprites.
        """
        self.view.display_screen()
        self.view.display_all_sprite()

    def _init_player_turn(self, player: Player, round_iteration: int
                        ) -> None:
        """
        Initializes a player's turn by drawing tiles and displaying
        their deck.

        Args:
            player (Player): The player whose turn is being initialized.
            round_iteration (int): The current round number.
        """
        if round_iteration==1 or round_iteration==2:
            self.playerscontroller.draw_tiles_hand(player, round_iteration)
        else:
            self.playerscontroller.draw_tiles_hand(player, 3)
        self.playerscontroller.prompt_deck(player)

    def _player_turn(self, player: Player, event_list) -> Optional[bool]:
        """
        Executes a single player's turn, including tile placement and
        board updates.

        Args:
            player (Player):
                The player taking the turn.
            event_list (List[pygame.event.Event]):
                List of pygame events.

        Returns:
            bool: True if the player's turn ends successfully.
        """

        self.view.display_screen()


        self.playerscontroller.play_tile_hand(player, event_list)
        self.boardcontroller.update_board_view_from_hand()

        self.view.generate_all_sprite_group()
        self.view.display_all_sprite()

        pygame.display.flip()

        if self._end_turn(player, event_list):
            return True



    def run(self) -> None:
        """
        Runs the main game loop, managing the sequence of rounds and
        player turns.
        """
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
