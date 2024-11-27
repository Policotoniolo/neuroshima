"""
docstring
"""
import random
import importlib

from typing import List, Literal, Tuple, Optional

class Tile:
    """Class representing a tile

    Attributes
    ----------
        army_name (str): Name of the army of the tile
        kind (Literal['base', 'unite', 'module', 'fondation']): type of tile. 
        Accepte "base", "unite", "module" or "fondation"
        initiative (List[int] | None): Liste of initiative of the tile. None for module and action
        range_attacks_direction (tuple | None): all attacks directions of the tile.
        range_attacks_power (List[int] | None): all the range attacks power of the tile.
        The index of this list correspond with the index of the range_attacks_direction list.
        cac_attacks_direction (tuple[int, int, int] | None): 
        all cac range attacks directions of the tile.
        cac_attacks_power (List[int] | None):  all the cac attacks power of the tile. 
        The index of this list correspond with the index of the range_attacks_direction list.
        life_point (int | None): Number of life points. None for action
        shields_position (tuple[int, int, int] | None): all the shields posisition of the tile.
        special_capacities (List[str] | None): Liste of speciale capacites of the tile.
    """
    def __init__(self,
                army_name: str,
                id_tile:str,
                kind: Literal['base', 'unite', 'module', 'fondation'],
                initiative: Optional[List[int]],
                range_attacks_direction: List[tuple],
                range_attacks_power: List[int],
                cac_attacks_direction: List[tuple],
                cac_attacks_power: List[int],
                net_directions: Optional[List[tuple]],
                life_point: Optional[int],
                shields_directions:  Optional[List[tuple]],
                special_capacities: List[str],
                board_position: Tuple[int, int, int],
                module: Optional[List[dict]],
                action : str,
                url_image: str):

        self.kind = kind
        self.army_name = army_name
        self.id_tile = id_tile
        self.initiative = initiative
        self.range_attacks_direction = range_attacks_direction
        self.range_attacks_power = range_attacks_power
        self.cac_attacks_direction = cac_attacks_direction
        self.cac_attacks_power = cac_attacks_power
        self.net_directions = net_directions
        self.life_point = life_point
        self.shields_position = shields_directions
        self.special_capacities = special_capacities
        self.module = module
        self.action = action
        self.board_position = board_position
        self.url_image = url_image
        self.is_netted: bool = False
        self.module_effects: List = []
        self.rotational_direction:Literal[0,1,2,3,4,5] = 0 #ecrire dans la dostring

    def _direction_positive_rotation(self,direction: tuple[int, int, int]
                                    ) -> tuple[int, int, int]:
        """Return the rotated direction with a angle of +60°

        Args:
            coordinnates (tuple[int, int, int]):  cube coordinnates to rotate. 
            Cube coordinnates define on the hexaboard

        Returns:
            tuple: rotated
        """
        q,r,s = direction
        return (-r, -s, -q)

    def _direction_negative_rotation(self,direction: tuple[int, int, int]
                                    ) -> tuple[int, int, int]:
        """Return the rotated direction with a angle of -60°

        Args:
            coordinnates (tuple[int, int, int]): cube coordinnates to rotate. 
            Cube coordinnates define on the hexaboard

        Returns:
            tuple: coordinnates rotated
        """
        q,r,s = direction
        return (-s, -q, -r)

    def _directions_rotation(self, directions: List[Tuple[int, int, int]], rotation_diff: int) -> List[Tuple[int, int, int]]:
        return [
                    (
                    self._direction_positive_rotation(direction)
                    if rotation_diff > 0
                    else self._direction_negative_rotation(direction)
                ) 
            for _ in range(abs(rotation_diff)) for direction in directions
            ]

    def _rotate_shield(self, rotation_diff: int) -> None:
        """Rotate shields directions of a tile base on a new rotate direction.

        Args:
            new_rotation_direction (_type_): New direction of the tile. Beetwen 1 and 6
        """
        if self.shields_position:
            self.shields_position = self._directions_rotation(
                                                self.shields_position,
                                                rotation_diff
                                            )

    def _rotate_attacks(self, rotation_diff: int) -> None:
        """Rotate attacks directions of a tile base on a new rotate direction

        Args:
            new_rotation_direction (int): New direction of the tile. Beetwen 1 and 6
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
        """Rotate net directions of a tile base on a new rotate direction.

        Args:
            new_rotation_direction (_type_): New direction of the tile. Beetwen 1 and 6
        """
        if self.net_directions:
            self.net_directions = self._directions_rotation(
                            self.net_directions,
                            rotation_diff
                        )

    def _rotate_module(self, rotation_diff: int) -> None:
        if self.module:
            for index, effect in enumerate(self.module):
                effect_name = list(effect.keys())[0]
                self.module[index][effect_name] = self._directions_rotation(
                            list(effect.values())[0],
                            rotation_diff
                        )

    def rotate_tile(self, new_rotation_direction: Literal[0,1,2,3,4,5]) -> None:
        """generate all the rotation (attacks, shields) of a tile

        Args:
            new_rotation_direction (int): New direction of the tile. Beetwen 0 and 5
        """
        if not 0 <= new_rotation_direction <= 5:
            raise ValueError("new_rotation_direction must be between 0 and 5.")

        rotation_diff = new_rotation_direction - self.rotational_direction
        if rotation_diff == 0:
            return

        self._rotate_attacks(new_rotation_direction)
        self._rotate_shield(new_rotation_direction)
        self._rotate_net(new_rotation_direction)
        self._rotate_module(new_rotation_direction)
        self.rotational_direction = new_rotation_direction


class Deck:
    """Class representing a deck
    """
    def __init__(self, army_name: str):
        self.tiles = []
        self.army_name = army_name
        self.defausse = []


    def _get_army(self) -> List[dict]:
        """Get army from armies file and return a list of dicts.
        Each dict represente a tile

        Returns:
            List[dict]: _description_
        """

        modulename = "armies"
        submodulename = self.army_name
        what = self.army_name
        module = importlib.import_module(modulename + "." + submodulename)
        army = getattr(module,what)

        return army

    def shuffle_deck(self) -> None:
        """shuffle the deck
        """
        random.shuffle(self.tiles)

    def init_deck(self) -> None:
        """collect and add tiles from the army in the deck
        """
        army = self._get_army()

        for dict_tile in army:
            self.tiles.append(
                Tile(
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
                    board_position = (-1,-1,-1) # init with impossible cube position
                ))

    def remove_top_deck_tile(self) -> Tile|None:
        """Return the first tile from the deck and remove it.
        First tile of deck is HQ if not shuffle
        """
        if self.tiles:
            return self.tiles.pop(0)


class Hand:
    """Describe the hand of a player
    """
    def __init__(self):
        self.tiles = []

    def add_tile(self, tile: Tile) -> None:
        """add a tile in the hand

        Args:
            tile (Tile): Tile to add in the hand
        """
        self.tiles.append(tile)

    def discard_tile(self, tiles: List[Tile]):
        """remove a tile from the hand

        Args:
            index (int): index to remove
        """
        for tile in tiles:
            self.tiles.remove(tile)

    def get_tile_by_id(self, id_tile : str) -> Tile|None:
        """get a tile from the hand according to the id tile

        Args:
            id_tile (str): id tile

        Returns:
            Tile: tile corresponding to the id tile
        """
        for tile in self.tiles:
            if tile.id_tile == id_tile:
                return tile

class Player:
    """Describe a player with his hand and his deck
    Args:
        name (str): player name
        army_name (str): army name
    """
    def __init__(self, name: str, army_name: str):
        self.name = name
        self.hand = Hand()
        self.deck = Deck(army_name)

    def get_tiles(self, number_tiles_to_get: int) -> None:
        """get tiles in hand player
        """
        nb_tiles_in_hand = len(self.hand.tiles)
        nb_tiles_to_draw = number_tiles_to_get - nb_tiles_in_hand

        if nb_tiles_to_draw != 0:
            for i in range (0, nb_tiles_to_draw) :
                tile = self.deck.remove_top_deck_tile()
                if tile is not None:
                    self.hand.add_tile(tile)
                i+=1

    def discard_tiles_hand(self, id_tiles_to_keep: List):
        """discard tiles from Hand player

        Args:
            id_tiles_to_keep (List): List of id tile
        """
        tiles_to_discard = []
        if len(self.hand.tiles)>0:
            for tile in self.hand.tiles:
                if tile.id_tile not in id_tiles_to_keep:
                    tiles_to_discard.append(tile)

            self.deck.defausse.append(self.hand.discard_tile(tiles_to_discard))


class HexBoard():
    """Describe the model Board
    """
    def __init__(self, board_limit: int, cube_direction_vectors: list[Tuple[int, int, int]], armies: List[str]) -> None:
        self.board_limit = board_limit
        self.cube_direction_vectors = cube_direction_vectors
        self.armies = armies
        self.tiles = {armies[0]:[], armies[1]:[]}
        self.hexes = []
        self.occupied = {armies[0]:[], armies[1]:[]}


    def add_tile_to_board(self, tile: Tile|None):
        """add a tile to the board. Do notthing if tile is None

        Args:
            tile (Tile): Instace of Tile Class
        """
        if tile is None:
            return
        army = tile.army_name
        if tile in self.tiles[army]:
            return
        self.occupied[army].append(tile.board_position)
        self.tiles[army].append(tile)

    def remove_tile_from_board(self, id_tile: str):
        """remove a tile from the board

        Args:
            id_tile (int): id of the tile
        """
        for index, tile in enumerate(self.tiles[self.armies[0]]):
            if tile.id_tile == id_tile:
                self.occupied[self.armies[0]].remove(tile.board_position)
                self.tiles[self.armies[0]].pop(index)
                return
        for index, tile in enumerate(self.tiles[self.armies[1]]):
            if tile.id_tile == id_tile:
                self.occupied[self.armies[1]].remove(tile.board_position)
                self.tiles[self.armies[1]].pop(index)
                return

    def find_army_tile_at_position(self, army_name: str, position: Tuple[int, int, int]) -> Tile|None:
        """get a tile of a specific army from the board according to the position

        Args:
            army_name (str): Name of the army
            position: Position of the tile to get. Cubique coordinates
        """
        for tile in self.tiles[army_name]:
            if tile.board_position == position:
                return tile
        return None

    def find_any_tile_at_position(self,  position: Tuple[int, int, int]) -> Tile|None:
        """get a tile of all army from the board according to the position

        Args:
            id_tile (int): id of the tile
        """
        for army_name in self.armies:
            for tile in self.tiles[army_name]:
                if tile.board_position == position:
                    return tile
        return None

    def create_board(self):
        """Create the hexa board
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

        self.hexes = tuple(self.hexes)


if __name__ == "__main__":
    deck = Deck("borgo")
    deck.init_deck()
