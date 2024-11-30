from typing import Optional, List, Tuple

from scripts.model.model import HexBoard

class TileActionController:
    def __init__(self, board: HexBoard) -> None:
        """
        Initializes the Tile action controller with a game board.

        Args:
            board (HexBoard): Game Board
        """
        self.board = board