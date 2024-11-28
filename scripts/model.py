import random
import importlib
from dataclasses import dataclass, field

from typing import List, Literal, Tuple, Optional, Dict

from config import CUBE_DIRECTION_VECTORS
from functions import raise_wrong_cube_coordinate


@dataclass
class Tile:
    """
    Represents a tile in a hexagonal grid-based game.

    The `Tile` class models a game tile with attributes for its type,
    position, combat characteristics, and special effects.
    The tile's orientation can be rotated, which affects its attack,
    defense, and other directional properties.

    Attributes
    ----------
        army_name (str): 
            Name of the army the tile belongs to.
        id_tile (str): 
            Unique identifier for the tile.
        kind (Literal['base', 'unite', 'module', 'fondation']): 
            Type of the tile, which determines its role and behavior. 
            Must be one of "base", "unite", "module", or "fondation".
        initiative (Optional[List[int]]): 
            List of initiative values for the tile,
            determining turn order. 
            None for tiles that do not participate in initiative-based
            actions.
        range_attacks_direction (List[tuple]): 
            List of directions for ranged attacks in cube coordinates.
        range_attacks_power (List[int]): 
            Corresponding power values for ranged attacks. 
            Each index aligns with `range_attacks_direction`.
        cac_attacks_direction (List[tuple]): 
            List of directions for close-combat (melee) attacks in cube
            coordinates.
        cac_attacks_power (List[int]): 
            Corresponding power values for close-combat attacks. 
            Each index aligns with `cac_attacks_direction`.
        net_directions (Optional[List[tuple]]): 
            Directions in which the tile can apply a "net" effect,
            if applicable.
        life_point (Optional[int]): 
            Number of life points the tile has. None for tiles that are
            not damageable.
        shields_directions (Optional[List[tuple]]): 
            Directions of shields for the tile in cube coordinates,
            if applicable.
        special_capacities (List[str]): 
            List of special abilities or effects the tile possesses.
        module (Optional[List[dict]]): 
            List of module effects of the tile, where each module effect
            has a name.
            Only if kind tile is "module".
            (key) and associated directional effects (values).
        action (Optional[str]): 
            Describes special action associated with the tile.
            Only if kind tile is "action".
        board_position (Tuple[int, int, int]): 
            The tile's position on the game board in cube coordinates.
        url_image (str): 
            URL of the tile's image for display in the game interface.
        is_netted (bool, default=False): 
            Indicates whether the tile is currently under a "net" effect
            , disabling some of its abilities.
        module_effects (List, default_factory=list): 
            Stores additional effects applied to the tile via modules.
            Applicable if tile kind not action
        rotational_index (Literal[0, 1, 2, 3, 4, 5], default=0): 
            Current rotation of the tile, represented as an index from
            0 to 5, corresponding to 60° increments on the hexagonal
            grid.

    Methods
    ----------
        rotate_tile(new_rotation_index: Literal[0, 1, 2, 3, 4, 5]
                ) -> None:
                Rotates the tile to a specified orientation.
                This updates all directional attributes (e.g., attacks,
                shields) to match the new orientation.

    Private Methods
    ----------
        _direction_positive_rotation(direction: Tuple[int, int, int]
                                ) -> Tuple[int, int, int]:
            Rotates a direction vector 60° clockwise.
        
        _direction_negative_rotation(direction: Tuple[int, int, int]
                                ) -> Tuple[int, int, int]:
            Rotates a direction vector 60° counterclockwise.

        _directions_rotation(directions: List[Tuple[int, int, int]],
                            rotation_diff: int) 
                        -> List[Tuple[int, int, int]]:
            Rotates a list of direction vectors by a specified number of
            steps.

        _rotate_shield(rotation_diff: int) -> None:
            Rotates the shield directions of the tile.

        _rotate_attacks(rotation_diff: int) -> None:
            Rotates the attack directions (both ranged and melee) of the
            tile.

        _rotate_net(rotation_diff: int) -> None:
            Rotates the net effect directions of the tile.

        _rotate_module(rotation_diff: int) -> None:
            Rotates the directional effects of modules applied to the
            tile.
    """

    army_name: str
    id_tile: str
    kind: Literal['base', 'unite', 'module', 'fondation']
    initiative: Optional[List[int]]
    range_attacks_direction: List[tuple]
    range_attacks_power: List[int]
    cac_attacks_direction: List[tuple]
    cac_attacks_power: List[int]
    net_directions: Optional[List[tuple]]
    life_point: Optional[int]
    shields_directions: Optional[List[tuple]]
    special_capacities: List[str]
    module: Optional[List[dict]]
    action: Optional[str]
    board_position: Tuple[int, int, int]
    url_image: str
    is_netted: bool = False
    module_effects: List = field(default_factory=list)
    rotational_index:Literal[0,1,2,3,4,5] = 0

    def rotate_tile(self, new_rotation_index: Literal[0,1,2,3,4,5]
                ) -> None:
        """
        generate all the rotation (attacks, shields) of a tile 
        according to a new rotation direction.

        Args:
            new_rotation_direction (int): New rotation index of the 
            tile. Beetwen 0 and 5
        """
        if not 0 <= new_rotation_index <= 5:
            raise ValueError("new_rotation_direction must be between 0 and 5.")

        rotation_diff = new_rotation_index - self.rotational_index
        if rotation_diff == 0:
            return

        self._rotate_attacks(new_rotation_index)
        self._rotate_shield(new_rotation_index)
        self._rotate_net(new_rotation_index)
        self._rotate_module(new_rotation_index)
        self.rotational_index = new_rotation_index

    # --- MÉTHODES PRIVÉES ---
    def _direction_positive_rotation(
                                self,direction: Tuple[int, int, int]
                                ) -> Tuple[int, int, int]:
        """Return the rotated direction with a angle of +60°

        Args:
            direction (Tuple[int, int, int]): 
                Direction coordinnates to rotate. 
                Cube coordinnates define on the hexaboard

        Returns:
            Tuple: direction rotated
        """
        q,r,s = direction
        return (-r, -s, -q)

    def _direction_negative_rotation(
                                self,direction: Tuple[int, int, int]
                                ) -> Tuple[int, int, int]:
        """Return the rotated direction with a angle of -60°

        Args:
            direction (Tuple[int, int, int]):
                Direction to rotate. 
                Cube coordinnates define on the hexaboard

        Returns:
            Tuple: direction rotated
        """
        q,r,s = direction
        return (-s, -q, -r)

    def _directions_rotation(self,
                            directions: List[Tuple[int, int, int]],
                            rotation_diff: int
                        ) -> List[Tuple[int, int, int]]:
        """
        Rotate a list of direction by a speficied number of step 
        (+60° or -60°)

        Args:
            directions (List[Tuple[int, int, int]]): 
                A list of cube coordinates representing
                the directions to be rotated.
            rotation_diff (int): 
                The number of rotation steps. 
                A positive value indicates clockwise rotation,
                while a negative value indicates
                counterclockwise rotation.

        Returns:
            List[Tuple[int, int, int]]:
                A new list of directions after applying the rotation.
        """
        return [
                    (
                    self._direction_positive_rotation(direction)
                    if rotation_diff > 0
                    else self._direction_negative_rotation(direction)
                ) 
            for _ in range(abs(rotation_diff))
            for direction in directions
        ]

    def _rotate_shield(self, rotation_diff: int) -> None:
        """
        Rotate shields directions of a tile by a speficied number of
        step.

        Args:
            rotation_diff (int): 
                The number of rotation steps. 
                A positive value indicates clockwise rotation,
                while a negative value indicates
                counterclockwise rotation.
        """
        if self.shields_position:
            self.shields_position = self._directions_rotation(
                                                self.shields_position,
                                                rotation_diff
                                            )

    def _rotate_attacks(self, rotation_diff: int) -> None:
        """
        Rotate attack directions of a tile by a speficied number of
        step.

        Args:
            rotation_diff (int): 
                The number of rotation steps. 
                A positive value indicates clockwise rotation,
                while a negative value indicates
                counterclockwise rotation.
        """
        if self.range_attacks_direction:
            self.range_attacks_direction = self._directions_rotation(
                                        self.range_attacks_direction,
                                        rotation_diff
                                    )
        if self.cac_attacks_direction:
            self.cac_attacks_direction = self._directions_rotation(
                                        self.cac_attacks_direction,
                                        rotation_diff
                                    )

    def _rotate_net(self, rotation_diff: int) -> None:
        """
        Rotate net directions of a tile by a speficied number of step.

        Args:
            rotation_diff (int): 
                The number of rotation steps. 
                A positive value indicates clockwise rotation,
                while a negative value indicates
                counterclockwise rotation.
        """
        if self.net_directions:
            self.net_directions = self._directions_rotation(
                            self.net_directions,
                            rotation_diff
                        )

    def _rotate_module(self, rotation_diff: int) -> None:
        """
        Rotate module directions of a tile by a speficied number of
        step.

        Args:
            rotation_diff (int): 
                The number of rotation steps. 
                A positive value indicates clockwise rotation,
                while a negative value indicates
                counterclockwise rotation.
        """
        if self.module:
            for index, effect in enumerate(self.module):
                effect_name = list(effect.keys())[0]
                self.module[index][effect_name] = \
                    self._directions_rotation(
                            list(effect.values())[0],
                            rotation_diff
                        )


class Deck:
    """Represents a deck of tiles for a specific army in the game.

    Attributes
    ----------
        army_name (str): The name of the army associated with this deck.
        tiles (List[Tile]): The list of tiles in the deck.
        defausse (List[Tile]): The discard pile for removed tiles
    
    Methods
    ----------
        shuffle_deck(self) -> None:
            Shuffles the tiles list deck.

        init_deck(self) -> None:
            Initializes the deck tiles list.

        remove_top_deck_tile(self) -> Optional[Tile]:
            Removes and returns the top tile from the deck.

    Private Methods
    ----------
    _get_army(self) -> List[dict]:
        Dynamically imports the army data module and return a list of
        dict representing the army's tiles.


    _dict_to_tile(self, dict_tile: dict) -> Tile:
        Converts a dictionary representation of a tile into a Tile
        object.
    """

    def __init__(self, army_name: str):
        self.tiles: List[Tile] = []  # Main deck
        self.army_name = army_name
        self.defausse: List[Tile] = []  # Discard pile

    def shuffle_deck(self) -> None:
        """Shuffles the tiles list deck."""
        random.shuffle(self.tiles)

    def init_deck(self) -> None:
        """Initializes the deck tiles list."""
        army = self._get_army()
        self.tiles = [self._dict_to_tile(tile_dict) for tile_dict in army]

    def remove_top_deck_tile(self) -> Optional[Tile]:
        """Removes and returns the top tile from the deck.

        Returns:
            Optional[Tile]:
                The removed tile, or None if the deck is empty.
        """
        return self.tiles.pop(0) if self.tiles else None

    # --- MÉTHODES PRIVÉES ---

    def _get_army(self) -> List[dict]:
        """
        Dynamically imports the army data module and return a list of
        dict representing the army's tiles.

        Returns:
            List[dict]: List of dictionaries representing the army's
            tiles.

        Raises:
            ValueError: If the army module or attribute is not found.
        """
        try:
            module = importlib.import_module(f"armies.{self.army_name}")
            army = getattr(module, self.army_name)
        except ModuleNotFoundError:
            raise ValueError(
                f"Army module '{self.army_name}' not found."
            )
        except AttributeError:
            raise ValueError(
                f"Army '{self.army_name}' not defined in the module."
            )
        return army

    def _dict_to_tile(self, dict_tile: dict) -> Tile:
        """
        Converts a dictionary representation of a tile into a Tile
        object.
        Args:
            dict_tile (dict): 
                dict containing information for Tile initialisation
        Raises:.
            TypeError: If the provided dict_tile is not a dictionary.
        """

        # Ensure the input is a dictionary
        if not isinstance(dict_tile, dict):
            raise TypeError("Expected a dictionary for dict_tile, got "
                            f"{type(dict_tile).__name__}.")

        return Tile(
            kind=dict_tile['kind'],
            army_name=dict_tile['army_name'],
            id_tile=dict_tile['id_tile'],
            initiative=dict_tile['initiative'],
            range_attacks_direction=dict_tile['range_attacks_direction'],
            range_attacks_power=dict_tile['range_attacks_power'],
            cac_attacks_direction=dict_tile['cac_attacks_direction'],
            cac_attacks_power=dict_tile['cac_attacks_power'],
            net_directions=dict_tile['net'],
            life_point=dict_tile['life_point'],
            shields_directions=dict_tile['shields_position'],
            special_capacities=dict_tile['special_capacities'],
            module=dict_tile['module'],
            action=dict_tile['action'],
            url_image=dict_tile['url_image'],
            board_position=(-1, -1, -1)  # Default invalid position
        )


class Hand:
    """
    Describe the hand of a player in the game. These are the tiles drawn
    by the player at the start of a turn.
    
    Attributes
    ----------
        hand_tiles (List[Tile] = []):
            The tiles currently in the player's hand.
    
    Methods
    ----------
        add_tile(self, tile: Tile) -> None:
            add a tile in hand

        discard_tile(self, tiles: List[Tile]) -> None:
            remove tiles from the hand.

        get_tile_by_id(self, id_tile : str) -> Tile:
            Return a tile from the hand according to the id tile
    """
    def __init__(self):
        self.hand_tiles: List[Tile] = []

    def add_tile(self, tile: Tile) -> None:
        """
        add a tile in the hand.

        Args:
            tile (Tile): Tile to add in the hand
        Raises:.
            ValueError: If the hand contains already three tiles.
        """
        if len(self.hand_tiles)>3:
            raise ValueError("Cannot add more than 3 tiles to the hand.")
        self.hand_tiles.append(tile)

    def discard_tile(self, tiles: List[Tile]) -> None:
        """
        remove tiles from the hand.

        Args:
            tiles (List[Tile]): List of tiles to remove

        Raises:.
            ValueError: If tile not found in hand
        """
        for tile in tiles:
            if tile in self.hand_tiles:
                self.hand_tiles.remove(tile)
            else:
                raise ValueError(f"Tile {tile.id_tile} not found in hand.")

    def get_tile_by_id(self, id_tile : str) -> Tile:
        #Non used, maybe delete this methos
        """
        Return a tile from the hand according to the id tile

        Args:
            id_tile (str): id tile

        Returns:
            Tile: tile corresponding to the id tile

        Raises:.
            ValueError: If tile not found in hand
        """
        for tile in self.hand_tiles:
            if tile.id_tile == id_tile:
                return tile
        else:
            raise ValueError(f"Tile {tile.id_tile} not found in hand.")

class Player:
    """Describe a player with his hand and his deck.
    Attributes
    ----------
        name (str): player name
        army_name (str): army name
    Methods
    ----------
        get_tiles(self, number_tiles_wanted: int) -> None:
            Get the number of tile wanted in hand.
            Check the tiles already in hand.
        discard_tiles_hand(self, id_tiles_to_keep: List = []):
            Discard tiles from Hand player but keep in hand some tiles
            if the player wants.

    """
    def __init__(self, name: str, army_name: str):
        self.name = name
        self.hand = Hand()
        self.deck = Deck(army_name)

    def get_tiles(self, number_tiles_wanted: Literal[1, 2, 3]) -> None:
        """
        Draw the desired number of tiles into the hand, ensuring the
        maximum hand size is not exceeded.

        Args:
            number_tiles_wanted (int): Desired number of tiles.
        Raises:
            ValueError: If the requested number exceeds the hand limit.

        """
        if number_tiles_wanted > 3:
            raise ValueError(
                        "Cannot have more than 3 tiles to the hand."
                    )
        
        nb_tiles_in_hand = len(self.hand.hand_tiles)
        nb_tiles_to_draw = number_tiles_wanted - nb_tiles_in_hand

        if nb_tiles_to_draw != 0:
            for _ in range (nb_tiles_to_draw) :
                tile = self.deck.remove_top_deck_tile()
                if tile:
                    self.hand.add_tile(tile)

    def discard_tiles_hand(self, id_tiles_to_keep: List[str] = []) -> None:
        """
        Discard tiles from the player's hand while optionally keeping
        specific tiles.

        Args:
            id_tiles_to_keep (List): IDs of tiles to keep in hand.
        """
        if len(self.hand.hand_tiles) == 0:
            return
        
        tiles_to_discard = [
                        tile for tile in self.hand.hand_tiles
                        if tile.id_tile not in id_tiles_to_keep
                        ]

        self.hand.discard_tile(tiles_to_discard)
        self.deck.defausse.extend(tiles_to_discard)


class HexBoard():
    """
    Represents the game board in a hexagonal grid system.
    
    Attributes
    ----------
        board_limit (Literal[3, 4]): 
            The size of the board, defined as the number of hexagons
            from the center to the outermost edge.
        armies (List[str]):
            Names of the armies participating in the game
        cube_direction_vectors (List[Tuple]):
            Predefined vectors used to calculate adjacent hexagonal
            coordinates.
        tiles (Dict[str,List[Tile]]):
            Tracks all tiles on the board for each army. Keys are army
            names, and values are lists of `Tile` objects
        hexes (List[Tuple[int, int, int]]):
            Contains all valid hexagonal positions on the board in cubic
            coordinates.
        occupied (Dict[str,List[Tuple[int, int, int]]]):
            Tracks occupied positions for each army. Keys are army
            names, and values are lists of occupied positions.
        position_index (Dict[str,Dict[Tuple[int, int, int],Tile]]):
            Maps positions to tiles for each army. Keys are army names,
            and values are dictionaries with positions as keys and
            `Tile` objects as values.
    
    Methods
    ----------
        add_tile_to_board(self, tile: Tile) -> None:
            Add a tile to the board if not already on the board, do
            nothing else.
            If the position is invalid raises an exception.
        remove_tile_from_board(self, id_tile: str) -> None:
            Removes a tile from the board by its ID. If the tile is not
            found, raises an exception.
        find_army_tile_at_position(self,\
                                    army_name: str,
                                    position: Tuple[int, int, int]
                                    ) -> Optional[Tile]:
            Finds and returns the tile belonging to a specific army at
            a given position. Returns `None` if no tile is found
        find_any_tile_at_position(self,  position: Tuple[int, int, int]\
                                    ) -> Optional[Tile]:
            Finds and returns a tile from any army at the specified
            position. Returns `None` if no tile is found.
        create_board(self) -> None:
            Initializes the board by generating all valid positions
            based on the `board_limit`.
    """
    def __init__(self,
                board_limit: Literal[3, 4],
                armies: List[str]
            ) -> None:

        if board_limit not in [3,4]:
            raise ValueError("board_limit must be 3 or 4")
        if len(armies) < 2:
            raise ValueError("At least two armies must be specified.")

        self.board_limit = board_limit
        self.cube_direction_vectors: List[Tuple] = CUBE_DIRECTION_VECTORS
        self.armies = armies
        self.tiles: Dict[str,List[Tile]]\
            = {army: [] for army in armies}
        self.hexes: List[Tuple[int, int, int]] = []
        self.occupied: Dict[str,List[Tuple[int, int, int]]]\
            = {army: [] for army in armies}
        self.position_index: Dict[str,Dict[Tuple[int, int, int],Tile]]\
            = {army: {} for army in self.armies}


    def add_tile_to_board(self, tile: Tile) -> None:
        """
        Add a tile to the board if not already on the board, do
        nothing else.

        Args:
            tile (Tile): Tile to add
        Raises:
            ValueError: If the tile argument is not a instance of Tile
            ValueError: If wrong board position
            ValueError: If the position is already occupied
        """
        if not isinstance(tile, Tile):
            raise ValueError("tile is not a Tile instance")
        if tile.board_position not in self.hexes:
            raise ValueError(
                f"tile position not on the board: {tile.board_position}"
            )

        if tile in self.tiles[tile.army_name]:
            return

        if tile.board_position in self.occupied[tile.army_name]:
            raise ValueError(
                    f"Position {tile.board_position} is already occupied."
                )

        self.occupied[tile.army_name].append(tile.board_position)
        self.tiles[tile.army_name].append(tile)
        self.position_index[tile.army_name][tile.board_position] = tile

    def remove_tile_from_board(self, id_tile: str) -> None:
        """
        Removes a tile from the board by its ID.

        Args:
            id_tile (int): ID of the tile
        Raises:
            ValueError: If the tile with the given ID is not found.
        """
        for army in self.armies:
            for index, tile in enumerate(self.tiles[army]):
                if tile.id_tile == id_tile:
                    self.occupied[army].remove(tile.board_position)
                    self.tiles[army].pop(index)
                    del self.position_index[army][tile.board_position]
                    return
        raise ValueError(f"No tile with ID '{id_tile}' found on the board.")

    def find_army_tile_at_position(self,
                                army_name: str,
                                position: Tuple[int, int, int]
                            ) -> Optional[Tile]:
        """
        Finds and returns the tile belonging to a specific army at
        a given position. Returns `None` if no tile is found

        Args:
            army_name (str): Name of the army
            position: Position of the tile to get. Cubique coordinates
        Raises:
            ValueError : if position not good
        """
        raise_wrong_cube_coordinate(position)
        tile = self.position_index[army_name].get(position)
        return tile

    def find_any_tile_at_position(self,  position: Tuple[int, int, int]
                                ) -> Optional[Tile]:
        """
        Finds and returns a tile from any army at the specified
        position. Returns `None` if no tile is found.

        Args:
            id_tile (int): id of the tile
        Raises:
            ValueError : if position not good
        """
        raise_wrong_cube_coordinate(position)
        for army_name in self.armies:
            tile = self.position_index[army_name].get(position)
            if tile:
                return tile
        return None

    def create_board(self) -> None:
        """
        Initializes the board by generating all valid positions
        based on the `board_limit`.
        """
        self.hexes = []
        index = 0

        for r in range(self.board_limit):
            x = 0
            y = -r
            z = +r

            self.hexes.append((x,y,z))
            index += 1

            for j in range(6):
                if j==5:
                    num_of_hexes_in_edge = r-1
                else:
                    num_of_hexes_in_edge = r
                for _ in range(num_of_hexes_in_edge):
                    x = x+self.cube_direction_vectors[j][0]
                    y = y+self.cube_direction_vectors[j][1]
                    z = z+self.cube_direction_vectors[j][2]

                    self.hexes.append((x,y,z))
                    index += 1


if __name__ == "__main__":
    deck = Deck("borgo")
    deck.init_deck()
