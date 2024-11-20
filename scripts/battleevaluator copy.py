import sys
from typing import List, Tuple, Optional
import pygame

from model_script import HexBoard, Tile
from moduleevaluator import ModuleEvaluator
from view import View
from functions import *

class BattleEvaluator:
    """_summary_
    """
    def __init__(self, 
            board: HexBoard,
            module_evaluator: ModuleEvaluator,
            view: View
            ) -> None:
        self.board = board
        self.module_evaluator = module_evaluator
        self.view = view

    def fire(self, tilemodel: Tile):
        """Applique les attaques (CAC et à distance) d'une tuile."""
        army_name = tilemodel.army_name
        enemy_army_name = self._get_enemy_army(tilemodel.army_name)

        # Gérer les attaques CAC
        self._apply_cac_attacks(tilemodel, enemy_army_name)

        # Gérer les attaques à distance
        self._apply_range_attacks(tilemodel, enemy_army_name)

    def spec_fire(self, tilemodel: Tile, range_attack_to_convert=None, cac_attack_to_convert=None):
        """_summary_

        Args:
            tilemodel (_type_): _description_
        """
        army_name = tilemodel.army_name
        enemy_army_name = next_element(self.board.armies, army_name)

        cac_attack_directions = tilemodel.cac_attacks_direction
        cac_attack_powers = tilemodel.cac_attacks_power

        range_attack_directions = tilemodel.range_attacks_direction
        range_attack_powers = tilemodel.range_attacks_power

        if range_attack_to_convert is not None and range_attack_directions is not None and range_attack_powers is not None:
            for index, attack in enumerate(range_attack_directions):
                if attack == range_attack_to_convert:
                    range_attack_directions.remove(range_attack_to_convert)
                    power = range_attack_powers[index]
                    range_attack_powers.pop(index)
                    cac_attack_directions.append(range_attack_to_convert)
                    cac_attack_powers.append(power)

        if cac_attack_to_convert is not None and cac_attack_directions is not None and cac_attack_powers is not None:
            for index, attack in enumerate(cac_attack_directions):
                if attack == range_attack_to_convert:
                    cac_attack_directions.remove(cac_attack_to_convert)
                    power = cac_attack_powers[index]
                    cac_attack_powers.pop(index)
                    range_attack_directions.append(cac_attack_to_convert)
                    range_attack_powers.append(power)

        if cac_attack_directions is not None:
            for index, cac_attack_direction in \
                enumerate(cac_attack_directions):
                
                cac_attack_position = tuple(
                    map(sum, zip(cac_attack_direction, tilemodel.board_position)) # type: ignore
                    )
                
                for enemy_tilemodel in self.board.tiles[enemy_army_name]:
                    if enemy_tilemodel.board_position == cac_attack_position:
                        enemy_tilemodel.life_point -= cac_attack_powers[index] # type: ignore

        if range_attack_directions is not None:
            for index, range_attack_direction in enumerate(range_attack_directions):
                touched = False
                range_attack_position = tuple(
                    map(sum, zip(range_attack_direction, tilemodel.board_position)) # type: ignore
                    )
                while (abs(range_attack_position[0])<=2 and 
                        abs(range_attack_position[1])<=2 and 
                        abs(range_attack_position[2])<=2
                    ) or touched == False:

                    for tile in self.board.tiles[enemy_army_name]:  
                        if tile.board_position == range_attack_position:
                            for shield in tile.shields_position:
                                if range_attack_direction == tuple([z * -1 for z in shield]):
                                    shield_point = 1
                            
                            tile.life_point -= (range_attack_powers - shield_point) # type: ignore
                            touched = True
                        else:
                            range_attack_position = tuple(map(sum, zip(range_attack_direction, range_attack_position)))

    def quartiermaitre_fire(self, tilemodel: Tile, event_list) ->  None:
        if tilemodel.range_attacks_direction is not None:
            real_range_attack_directions = [tuple(
                                map(
                                    sum,zip(
                                        x, 
                                        tilemodel.\
                                            board_position # type:ignore
                                            
                                        )
                                    )
                                ) for x in tilemodel.range_attacks_direction]
        if tilemodel.cac_attacks_direction is not None:
            real_cac_attack_directions = [tuple(
                                map(
                                    sum,zip(
                                        x, 
                                        tilemodel.\
                                            board_position # type:ignore
                                        )
                                    )
                                ) for x in tilemodel.cac_attacks_direction]

        range_attack_pixel = list_cubes_to_pixel(real_range_attack_directions)
        cac_attack_pixel = list_cubes_to_pixel(real_cac_attack_directions)

        all_pixel = range_attack_pixel + cac_attack_pixel
        for pixel in all_pixel:
            if pixel in range_attack_pixel:
                hex = self.view.boardzone.get_hexagone_by_position(pixel) # type: ignore
                if hex.attacks_range_click_button(event_list, self.view.boardzone.drawsurf): # type: ignore
                    range_pos_to_change = pixel 
                    cube_coord_range = coordinates_pixel_to_cube(range_pos_to_change) # type: ignore
                    cube_coord_range = tuple(map(operator.sub, cube_coord_range, tilemodel.board_position)) # type: ignore
                    self.spec_fire(tilemodel, range_attack_to_convert=cube_coord_range)
                    self.module_evaluator._clean_quartiermaitre_effect_on_tile(tilemodel)
            if pixel in cac_attack_pixel:
                hex = self.view.boardzone.get_hexagone_by_position(pixel) # type: ignore
                if hex.attacks_cac_click_button(event_list, self.view.boardzone.drawsurf): # type: ignore
                    cac_pos_to_change = pixel
                    cube_coord_cac = coordinates_pixel_to_cube(cac_pos_to_change) # type: ignore
                    cube_coord_cac =  tuple(map(operator.sub, cube_coord_range, tilemodel.board_position)) # type: ignore
                    self.spec_fire(tilemodel, cac_attack_to_convert=cube_coord_cac)
                    self.module_evaluator._clean_quartiermaitre_effect_on_tile(tilemodel)

    def get_same_initiative_tiles(self, initiative: int) -> List[Tile]:
        """return all tiles with same initiative."""
        return [
            tile
            for army in self.board.armies
            for tile in self.board.tiles[army]
            if tile.initiative == initiative
        ]

    def remove_dead_tile(self) -> None:
        """Remove tiles with hit points below zero."""
        for army in self.board.armies:
            for tile in self.board.tiles[army]:
                if tile.life_point < 0:
                    self.board.remove_tile_from_board(tile.id_tile)

    def battle_round(self, initiative_round: int, event_list):
        tiles = self.get_same_initiative_tiles(initiative_round)
        for tile in tiles:
            if "quartiermaitre" in tile.module_effects:
                self.quartiermaitre_fire(tile, event_list)
            else:
                self.fire(tile)
        self.remove_dead_tile()

    def run_battle(self, event_list):
        initiative_round = 10
        while initiative_round >= 0 :
            self.battle_round(initiative_round=initiative_round,
                event_list=event_list)
            initiative_round -= 1

# --- MÉTHODES PRIVÉES ---

    def _get_enemy_army(self, army_name: str) -> str:
        """Return the enemey name of army_name"""
        return next_element(self.board.armies, army_name)

    def _calculate_position(self,
                            start_position: Tuple[int, int, int],
                            direction: Tuple[int, int, int]
                            ) -> Tuple[int, int, int]:
        """
        Calculates the new position on a hexagonal grid by applying a directional offset.

        Args:
            start_position (Tuple[int, int, int]): The starting position in cube coordinates.
            direction (Tuple[int, int, int]): The directional vector in cube coordinates.

        Returns:
            Tuple[int, int, int]: The resulting position after adding the direction to the start position.
        """
        return  tuple(
                    map(sum, zip(start_position, direction))
                    ) # type: ignore

    def _apply_cac_attacks(self, tilemodel: Tile, enemy_army_name: str):
        """
        Executes all cac attacks from a tile against an enemy army.

        This function iterates over the cac attack directions and powers defined for the attacking tile. 
        For each attack, it delegates the damage application to `_process_cac_attack`, handling the targeting and damage mechanics.

        Args:
            tilemodel (Tile): The attacking tile performing the cac attacks.
            enemy_army_name (str): The name of the enemy army to target.
        """
        if tilemodel.cac_attacks_direction:
            for index, cac_attack_direction in \
                    enumerate(tilemodel.cac_attacks_direction):
                self._process_cac_attack(tilemodel,
                                        enemy_army_name,
                                        cac_attack_direction,
                                        tilemodel.cac_attacks_power[index]
                                    )

    def _apply_range_attacks(self, tilemodel: Tile, enemy_army_name: str):
        """
        Executes all ranged attacks from a tile against an enemy army.

        This function iterates over the ranged attack directions and powers defined for the attacking tile. 
        For each attack, it delegates the damage application to `_process_range_attack`, handling the targeting and damage mechanics.

        Args:
            tilemodel (Tile): The attacking tile performing the ranged attacks.
            enemy_army_name (str): The name of the enemy army to target.
        """
        if tilemodel.range_attacks_direction:
            for index, range_attack_direction in enumerate(tilemodel.range_attacks_direction):
                self._process_range_attack(tilemodel,
                                        enemy_army_name,
                                        range_attack_direction,
                                        tilemodel.range_attacks_power[index]
                                    )

    def _process_cac_attack(self,
                            tilemodel: Tile,
                            enemy_army_name: str,
                            cac_attack_direction: Tuple[int, int, int],
                            cac_attack_power: int
                            ):
        """
        Processes a close-quarters combat (CQC) attack from a tile, applying damage to an enemy tile in the specified direction.

        This function calculates the position of the target based on the attacking tile's position and the direction of the attack. 
        If an enemy tile is found at the calculated position, it reduces the enemy's life points by the specified attack power.

        Args:
            tilemodel (Tile): The attacking tile performing the close-combat attack.
            enemy_army_name (str): The name of the enemy army to target.
            cac_attack_direction (Tuple[int, int, int]): The direction of the attack in cube coordinates.
            cac_attack_power (int): The power of the close-combat attack.
        """

        cac_attack_position = self._calculate_position(
            tilemodel.board_position, cac_attack_direction
        )
        enemy_tilemodel = self.board.find_tile_at_position(
            enemy_army_name, cac_attack_position
        )
        if enemy_tilemodel and enemy_tilemodel.life_point:
            enemy_tilemodel.life_point -= \
                cac_attack_power

    def _process_range_attack(self,
                            tilemodel: Tile,
                            enemy_army_name: str,
                            range_attack_direction: Tuple[int, int, int],
                            range_attack_power: int
                            ):
        """
        Processes a ranged attack from a tile and applies damage to the enemy target if hit.

        This function simulates a ranged attack by iteratively advancing in the specified
        direction from the tile's current position. If the attack encounters an enemy tile,
        it calculates the damage, factoring in potential shield protection.

        Args:
            tilemodel (Tile): The attacking tile performing the ranged attack.
            enemy_army_name (str): The name of the enemy army to target.
            range_attack_direction (Tuple[int, int, int]): The direction of the ranged attack in cube coordinates.
            range_attack_power (int): The base power of the ranged attack.
        """
        touched = False
        range_attack_position = tilemodel.board_position
        while self._is_within_board_range(range_attack_position) or not touched:

            range_attack_position = self. _calculate_position(
                range_attack_position,range_attack_direction 
                )
            enemy_tilemodel = self.board.find_tile_at_position(
                                                    enemy_army_name, 
                                                    range_attack_position
                                                    )
            if enemy_tilemodel and enemy_tilemodel.life_point:
                if enemy_tilemodel.shields_position:
                    for shield in enemy_tilemodel.shields_position:
                        if range_attack_direction == tuple([z * -1 for z in shield]):
                            shield_point = 1
                    
                    enemy_tilemodel.life_point -= (range_attack_power - shield_point)
                    touched = True

    def _is_within_board_range(self, cube_position: Tuple[int, int, int], max_range: int = 2):
        """Checks if a cube coordinate position is within the board's valid range."""
        return all(abs(coord) <= max_range for coord in cube_position)