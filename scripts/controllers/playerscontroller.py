import pygame
from typing import Optional, List, Literal

from scripts.model.model import HexBoard, Player
from scripts.view.view import View
from scripts.controllers.tilecontroller import TileController

class PlayersController:
    """
    Controller class to handle the interactions and actions related to
    players.

    This class is responsible for managing the player's deck, tiles in
    hand, drawing tiles, and the actions performed during a player's
    turn. It also handles the rendering and display of player-related
    game elements.

    Attributes
    ----------
    board (HexBoard): 
        The game board containing the game state and board positions.
    players (List[Player]):
        List of players involved in the game.
    tileactioncontroller (TileController):
        A controller responsible for handling actions related to tiles.
    view (View):
        The view object that handles rendering and user interface.

    Methods
    -------
    get_id_tiles_from_hand(player: Player) -> List[str]:
        Retrieves a list of tile IDs from the player's hand.

    get_size_deck(player: Player) -> int:
        Retrieves the number of remaining tiles in the player's deck.

    prompt_deck(player: Player) -> None:
        Prompts the view to show the remaining tiles in the
        player's deck.

    draw_hq_tile(player: Player) -> None:
        Draws the HQ tile and adds it to the player's hand.

    draw_tiles_hand(player: Player, nb_tiles: int = 3) -> None:
        Draws a specified number of tiles from the player's deck into
        their hand.

    play_tile_hand(player: Player, event_list: List[pygame.event.Event]
            ) -> None:
        Executes the actions related to playing tiles from the player's
        hand after having drawn, including moving tiles on the board 
        and performing tile actions.

    end_player_turn(player: Player, event_list: List[pygame.event.Event]
            ) -> Optional[bool]:
        Ends the player's turn, allowing them to discard tiles and
        handle other end-of-turn logic. Return True if player end turn.
    """
    def __init__(self,
                board: HexBoard, 
                players: List[Player], 
                view: View,
                tileactioncontroller: TileController
            ) -> None:
        """
        Initializes the controller.

        Args:
            board (HexBoard):
                Game Board model.
            view (View): 
                Graphical interface for user interactions and feedback.
            tileactioncontroller (TileController):
                Tile controller.
        """
        self.board = board
        self.players = players
        self.tileactioncontroller = tileactioncontroller
        self.view = view

    def get_id_tiles_from_hand(self, player: Player) -> List[str]:
        """
        Retrieves a list of tile IDs from the player's hand.

        Args:
            player (Player): The player whose hand is being checked.

        Returns:
            List[str]: A list of tile IDs present in the player's hand.
        """
        return [tile.id_tile for tile in player.hand.hand_tiles]

    def get_size_deck(self, player: Player) -> int:
        """
        Retrieves the number of remaining tiles in the player's deck.

        Args:
            player (Player): 
                The player whose deck size is being checked.

        Returns:
            int: The number of tiles remaining in the player's deck.
        """
        return len(player.deck.tiles)

    def prompt_deck(self, player: Player) -> None:
        """
        Prompts the view to show the number of remaining tiles in
        the player's deck.

        Args:
            player (Player): The player whose deck size is displayed.
        """
        number_tiles = self.get_size_deck(player)
        self.view.get_tiles_deck(number_tiles)

    def draw_hq_tile(self, player: Player) -> None:
        """
        Draws the HQ tile and adds it to the player's hand, updating the
        view.

        Args:
            player (Player): The player drawing their HQ tile.
        """
        player.hand.add_tile(player.deck.hq_tile)
        id_tile = self.get_id_tiles_from_hand(player)
        self.view.get_tiles_hand(id_tile)

    def draw_tiles_hand(self,
                        player: Player,
                        nb_tiles: Literal[1,2,3]=3
                    ) -> None:
        """
        Draws a specified number of tiles from the player's deck into
        their hand.

        Args:
            player (Player):
                The player drawing tiles.
            nb_tiles (Literal[1, 2, 3]):
                The number of tiles to draw (default is 3).

        Raises:
            ValueError: If the number of tiles to draw exceeds the limit
            or is less than the tiles already in hand.
        """
        nb_tiles_hand = len(player.hand.hand_tiles)
        diff = nb_tiles - nb_tiles_hand
        if diff > 3:
            raise ValueError(
                "Number of tile in hand should not exceed 3."
            )
        if diff < 0:
            raise ValueError(
                "Number of tile ask less than number of tile already in hand"
            )
        elif diff != 0:
            player.get_tiles(diff) # type: ignore

        id_tiles = self.get_id_tiles_from_hand(player)
        self.view.get_tiles_hand(id_tiles)


    def play_tile_hand(self,
                    player: Player,
                    event_list: List[pygame.event.Event]
                ) -> None:
        """
        Executes actions related to playing tiles from the player's
        hand, including moving tiles on the board and performing
        tile-specific actions.

        Args:
            player (Player):
                The player performing the action.
            event_list (List[pygame.event.Event]):
                The list of pygame events to process.
        """
        self.view.move_tile_hand(event_list)
        self.view.move_tile_board(event_list)

        self.tileactioncontroller.actiontile(player, event_list)

        self.view.generate_all_sprite_group()
        self.view.display_all_sprite()


    def end_player_turn(self,
                        player: Player,
                        event_list: List[pygame.event.Event]
                    ) -> Optional[bool]:
        """
        Ends the player's turn, allowing them to discard tiles and
        handle other end-of-turn logic.

        Args:
            player (Player):
                The player whose turn is ending.
            event_list (List[pygame.event.Event]):
                The list of pygame events to process.

        Returns:
            bool:
                True if the player's turn ends successfully,
                False otherwise.
        """
        if self.view.endbutton.isvalidated(event_list):
            id_tileviews_to_keep = self.view.get_id_tile_to_keep()
            player.discard_tiles_hand(id_tileviews_to_keep)

            return True
