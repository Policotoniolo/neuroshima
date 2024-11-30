from typing import Optional, List, Tuple

from scripts.model.model import HexBoard

class BoardController:
    def __init__(self, board: HexBoard) -> None:
        """
        Initializes the board controller with a game board.

        Args:
            board (HexBoard): Game Board
        """
        self.board = board 