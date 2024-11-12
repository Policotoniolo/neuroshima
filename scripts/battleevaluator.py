import sys
from typing import List
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
        """_summary_

        Args:
            tilemodel (_type_): _description_
        """
        army_name = tilemodel.army_name
        enemy_army_name = next_element(self.board.armies, army_name)

        if tilemodel.cac_attacks_direction is not None:
            for index, cac_attack_direction in \
                enumerate(tilemodel.cac_attacks_direction):
                
                cac_attack_position = tuple(
                    map(sum, zip(cac_attack_direction, tilemodel.board_position)) # type: ignore
                    )
                
                for enemy_tilemodel in self.board.tiles[enemy_army_name]:
                    if enemy_tilemodel.board_position == cac_attack_position:
                        enemy_tilemodel.life_point -= tilemodel.cac_attacks_power[index] # type: ignore

        if tilemodel.range_attacks_direction is not None:
            for index, range_attack_direction in enumerate(tilemodel.range_attacks_direction):
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
                            
                            tile.life_point -= (tilemodel.cac_attacks_power[index] - shield_point) # type: ignore
                            touched = True
                        else:
                            range_attack_position = tuple(map(sum, zip(range_attack_direction, range_attack_position)))

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

    def get_same_initiative_tiles(self, initiative) -> List[Tile]:
        tiles = []
        for tile in self.board.tiles[self.board.armies[0]]:
            if tile.initiative == initiative:
                tiles.append(tile)
        for tile in self.board.tiles[self.board.armies[1]]:
            if tile.initiative == initiative:
                tiles.append(tile)
        return tiles

    def remove_dead_tile(self) -> None:
        for tile in self.board.tiles[self.board.armies[0]]:
            if tile.life_point < 0:
                self.board.remove_tile_from_board(tile.id_tile)
        for tile in self.board.tiles[self.board.armies[1]]:
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