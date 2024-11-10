"""
docstring
"""
import random
import importlib
import sys

from typing import List, Literal

# lien entre l'index de la direction de la rotaion et les coordonnées.
# Ce sont les coordonnées en imaginant que la tuile est au centre.
ROTATIONS =  {(0, -1, 1): 0,
            (1, -1, 0): 1,
            (1, 0, -1): 2,
            (0, 1, -1): 3,
            (-1, 1, 0): 4,
            (-1, 0, 1): 5}


class Tile:
    """Class representing a tile
    Args:
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
                initiative: List[int]|None,
                range_attacks_direction: List[tuple]|None,
                range_attacks_power: List[int]|None,
                cac_attacks_direction: List[tuple]|None,
                cac_attacks_power: List[int]|None,
                net: List[tuple]|None,
                life_point: int|None,
                shields_position: List[tuple]|None,
                special_capacities: List[str]|None,
                module: List[dict]|None,
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
        self.net = net
        self.life_point = life_point
        self.shields_position = shields_position
        self.special_capacities = special_capacities
        self.board_position = None
        self.rotational_direction = 0
        self.module = module
        self.action = action
        self.is_netted = False
        self.url_image = url_image

    def _coordinates_positive_rotation(self,coordinnates: tuple[int, int, int]
                                    ) -> tuple[int, int, int]:
        """Return the rotated coordinnates with a angle of +60°

        Args:
            coordinnates (tuple[int, int, int]):  cube coordinnates to rotate. 
            Cube coordinnates define on the hexaboard

        Returns:
            tuple: rotated
        """
        q,r,s = coordinnates[0], coordinnates[1], coordinnates[2]
        return ((-r, -s, -q))

    def _coordinates_negative_rotation(self,coordinnates: tuple[int, int, int]
                                    ) -> tuple[int, int, int]:
        """Return the rotated coordinnates with a angle of -60°

        Args:
            coordinnates (tuple[int, int, int]): cube coordinnates to rotate. 
            Cube coordinnates define on the hexaboard

        Returns:
            tuple: coordinnates rotated
        """
        q,r,s = coordinnates[0], coordinnates[1], coordinnates[2]
        return ((-s, -q, -r))

    def _rotate_shield(self, new_rotation_direction: int) -> None:
        """Rotate shields directions of a tile base on a new rotate direction.

        Args:
            new_rotation_direction (_type_): New direction of the tile. Beetwen 1 and 6
        """
        rotation_diff = new_rotation_direction - self.rotational_direction
        if rotation_diff == 0:
            return

        for _ in range(abs(rotation_diff)):
            if self.shields_position is not None:
                new_shield_posistion = []

                for shield in self.shields_position:
                    if rotation_diff > 0:
                        new_shield_posistion.append(self._coordinates_positive_rotation(shield))
                    else:
                        new_shield_posistion.append(self._coordinates_negative_rotation(shield))
                self.shields_position = new_shield_posistion

    def _rotate_attacks(self, new_rotation_direction: int) -> None:
        """Rotate attacks directions of a tile base on a new rotate direction

        Args:
            new_rotation_direction (int): New direction of the tile. Beetwen 1 and 6
        """
        rotation_diff = new_rotation_direction - self.rotational_direction

        if rotation_diff == 0:
            return None

        for _ in range(abs(rotation_diff)):

            if self.range_attacks_direction is not None:
                new_range_attacks_direction = []

                for range_attack in self.range_attacks_direction:

                    if rotation_diff > 0:
                        new_range_attacks_direction.append(
                            self._coordinates_positive_rotation(range_attack)
                            )
                    else:
                        new_range_attacks_direction.append(
                            self._coordinates_negative_rotation(range_attack)
                            )
                self.range_attacks_direction = new_range_attacks_direction


            if self.cac_attacks_direction is not None:
                new_cac_attacks_direction = []

                for cac_attack in self.cac_attacks_direction:

                    if rotation_diff > 0:
                        new_cac_attacks_direction.append(
                            self._coordinates_positive_rotation(cac_attack)
                            )
                    elif rotation_diff < 0:
                        new_cac_attacks_direction.append(
                            self._coordinates_negative_rotation(cac_attack)
                            )
                self.cac_attacks_direction = new_cac_attacks_direction

    def _rotate_net(self, new_rotation_direction: int):
        """Rotate net directions of a tile base on a new rotate direction.

        Args:
            new_rotation_direction (_type_): New direction of the tile. Beetwen 1 and 6
        """
        rotation_diff = new_rotation_direction - self.rotational_direction
        if rotation_diff == 0:
            return

        for _ in range(abs(rotation_diff)):
            if self.net is not None:
                new_net_posistion = []

                for net in self.net:
                    if rotation_diff > 0:
                        new_net_posistion.append(self._coordinates_positive_rotation(net))
                    else:
                        new_net_posistion.append(self._coordinates_negative_rotation(net))
                self.net = new_net_posistion

    def rotate_tile(self, new_rotation_direction: int) -> None:
        """generate all the rotation (attacks, shields) of a tile

        Args:
            new_rotation_direction (int): New direction of the tile. Beetwen 1 and 6
        """

        self._rotate_attacks(new_rotation_direction)
        self._rotate_shield(new_rotation_direction)
        self._rotate_net(new_rotation_direction)

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
                    net=dict_tile['net'],
                    life_point=dict_tile['life_point'],
                    shields_position=dict_tile['shields_position'],
                    special_capacities=dict_tile['special_capacities'],
                    module=dict_tile['module'],
                    action=dict_tile['action'],
                    url_image=dict_tile['url_image']
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
    def __init__(self, board_limit: int, deltas: list[list[int]], armies: List[str]) -> None:
        self.board_limit = board_limit
        self.deltas = deltas
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

    def get_tile_by_position(self, position: Tuple[int, int, int]) -> Tile|None:
        """get a tile from the board according to the position

        Args:
            id_tile (int): id of the tile
        """
        for tile in self.tiles[self.armies[0]]:
            if tile.board_position == position:
                return tile
        for tile in self.tiles[self.armies[1]]:
            if tile.board_position == position:
                return tile


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
                    x = x+self.deltas[j][0]
                    y = y+self.deltas[j][1]
                    z = z+self.deltas[j][2]

                    self.hexes.append((x,y,z))
                    index += 1

        self.hexes = tuple(self.hexes)


if __name__ == "__main__":
    deck = Deck("borgo")
    deck.init_deck()
