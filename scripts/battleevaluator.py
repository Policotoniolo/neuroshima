import pygame
from typing import List, Tuple
import operator
import copy

from scripts.model import HexBoard, Tile
from moduleevaluator import ModuleEvaluator
from view import View
from functions import *


class BattleEvaluator:
    """
    BattleEvaluator is responsible for managing and 
    simulating combat actions between tiles.

    The class provides mechanisms for applying close-quarters combat
    and ranged attacks, handling special effects like converting 
    attack types, and resolving rounds based on tile initiatives.

    Attributes
    ----------
        board (HexBoard): The game board containing tiles and
                        their positions.
        module_evaluator (ModuleEvaluator): Evaluates and 
                                    applies module effects.
        view (View): Provides a graphical interface for
                    user interactions and feedback.

    Methods
    ----------
        fire(tilemodel: Tile):
            Executes both close-quarters combat (CQC) and 
            ranged attacks for a given tile.

        generate_attacks_with_quartiermaitre(
            tilemodel: Tile, event_list
        ):
            Handles special attacks triggered by
            the "quartiermaître" module effect.

        get_same_initiative_tiles(initiative: int) -> List[Tile]:
            Retrieves all tiles with the same initiative level.

        remove_dead_tile():
            Removes tiles from the board that have zero or 
            negative life points.

        battle_round(initiative_round: int, event_list):
            Executes a single round of combat for all tiles 
            with the same initiative.

        run_battle(event_list):
            Simulates the battle sequence by resolving rounds in
            descending initiative order.

    Private Methods
    ----------
        _get_max_initiative() -> int:
            Return the highest initiative among all tiles on the board.

        _get_enemy_army(army_name: str) -> str:
            Identifies the opposing army based on 
            the provided army name.

        _apply_cac_attacks(tilemodel: Tile, enemy_army_name: str):
            Executes all close-quarters attacks for a given tile.
            This function iterates over the cac attack directions 
            and powers defined for the attacking tile. 
            For each attack, it delegates the damage application
            to `_process_cac_attack`,handling the targeting and
            damage mechanics.

        _apply_range_attacks(tilemodel: Tile, enemy_army_name: str):
            Executes all ranged attacks from a tile 
            against an enemy army.
            This function iterates over the ranged attack directions 
            and powers defined for the attacking tile. 
            For each attack, it delegates the damage application 
            to `_process_range_attack`, 
            handling the targeting and damage mechanics.

        _process_cac_attack(tilemodel: Tile, 
                            enemy_army_name: str, 
                            cac_attack_direction: Tuple[int, int, int],
                            cac_attack_power: int
                        ):
            Processes a close-quarters combat (CQC) attack from a tile, 
            applying damage to an enemy tile in the specified direction.

            This function calculates the position of the target based 
            on the attacking tile's position and 
            the direction of the attack. 
            If an enemy tile is found at the calculated position, 
            it reduces the enemy's life points by 
            the specified attack power.

        _process_range_attack(tilemodel: Tile, 
                        enemy_army_name: str, 
                        range_attack_direction: Tuple[int, int, int],
                        range_attack_power: int
                            ):
            Processes a ranged attack from a tile and 
            applies damage to the enemy target if hit.

            This function simulates a ranged attack by iteratively 
            advancing in the specified direction 
            from the tile's current position. 
            If the attack encounters an enemy tile, it calculates 
            the damage, factoring in potential shield protection.

        _get_pixel_positions_cac_attacks(
                                tilemodel: Til
                            ) -> List[Tuple[int, int]] | None:
            Retrieves the pixel positions of all valid CQC attack directions.

        _get_pixel_positions_range_attacks(tilemodel: Tile) -> List[Tuple[int, int]] | None:
            Retrieves the pixel positions of all valid ranged attack directions.

        _is_within_board_range(cube_position: Tuple[int, int, int], max_range: int = 2) -> bool:
            Verifies whether a position is within the valid board range.

        _prompt_and_get_attacke_direction_convertion(tilemodel: Tile, 
                                                    attack_pixel_positions: List[Tuple[int, int]],
                                                    event_list
                                                ) -> Tuple[int, int, int] | None:
            Prompts the user to select an attack direction to convert and 
            returns the chosen direction.

        _converte_attacks_and_copy_tile(tilemodel: Tile, 
                                        range_attack_to_converte, 
                                        cac_attack_to_converte
                                    ) -> Tile:
            Creates a copy of the tile and converts a specified attack.

        _converte_range_attack(tilemodel: Tile, range_attack_to_converte):
            Converts a ranged attack into a CQC attack.

        _converte_cac_attack(tilemodel: Tile, cac_attack_to_converte):
            Converts a CQC attack into a ranged attack.
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
        """
        Executes both close-quarters combat (CQC) and ranged attacks for a given tile.

        Args:
            tilemodel (Tile): The tile initiating the attack.
        """
        if not isinstance(tilemodel, Tile):
            raise ValueError(f"Invalid tile object: {tilemodel}")

        enemy_army_name = self._get_enemy_army(tilemodel.army_name)

        # Gérer les attaques CAC
        self._apply_cac_attacks(tilemodel, enemy_army_name)

        # Gérer les attaques à distance
        self._apply_range_attacks(tilemodel, enemy_army_name)

    def generate_attacks_with_quartiermaitre(self,
                                            tilemodel: Tile,
                                            event_list: List[pygame.event.Event]
                                            ) -> None:
        """Handles special attacks triggered by the "quartiermaître" module effect.

        Args:
            tilemodel (Tile): The tile initiating the attack.
            event_list (List[pygame.event.Event]): Pygame events list
        """
        if not isinstance(tilemodel, Tile):
            raise ValueError(f"Invalid tile object: {tilemodel}")

        range_attack_pixel = self._get_pixel_positions_range_attacks(tilemodel)
        cac_attack_pixel = self._get_pixel_positions_cac_attacks(tilemodel)
        if range_attack_pixel:
            range_attack_to_converte = \
                self._prompt_and_get_attacke_direction_convertion(
                    tilemodel,
                    range_attack_pixel,
                    event_list)
        if cac_attack_pixel:
            cac_attack_to_converte = \
                self._prompt_and_get_attacke_direction_convertion(
                    tilemodel,
                    cac_attack_pixel,
                    event_list)
        tileconverted = self._converte_attacks_and_copy_tile(
            tilemodel, range_attack_to_converte, cac_attack_to_converte)

        self.fire(tileconverted)
        self.module_evaluator._clean_quartiermaitre_effect_on_tile(tilemodel)

    def get_same_initiative_tiles(self, initiative: int) -> List[Tile]:
        """Retrieves all tiles with the same initiative level.

        Args:
            initiative (int): Initiative number wanted

        Returns:
            List[Tile]: List of tile with same initiative
        """
        return [
            tile
            for army in self.board.armies
            for tile in self.board.tiles[army]
            if tile.initiative == initiative
        ]

    def remove_dead_tile(self) -> None:
        """Removes tiles from the board that have zero or negative life points."""
        for army in self.board.armies:
            for tile in self.board.tiles[army]:
                if tile.life_point < 0:
                    self.board.remove_tile_from_board(tile.id_tile)

    def battle_round(self,
                    initiative_round: int,
                    event_list: List[pygame.event.Event]
                    ) -> None:
        """Executes a single round of combat for all tiles with the same initiative.

        Args:
            initiative_round (int): initiative of the round
            event_list (List[pygame.event.Event]): Pygame events list
        """
        tiles = self.get_same_initiative_tiles(initiative_round)
        for tile in tiles:
            if "quartiermaitre" in tile.module_effects:
                self.generate_attacks_with_quartiermaitre(tile, event_list)
            else:
                self.fire(tile)
        self.remove_dead_tile()

    def run_battle(self, event_list: List[pygame.event.Event]) -> None:
        """Simulates the battle sequence by resolving rounds in descending initiative order.

        Args:
            event_list (List[pygame.event.Event]): Pygame events list
        """
        initiative_round = self._get_max_initiative()
        while initiative_round >= 0:
            self.module_evaluator.apply_all_effect_modules()
            self.battle_round(initiative_round=initiative_round,
                            event_list=event_list
                            )
            self.module_evaluator.clean_all_effect_modules()
            initiative_round -= 1

# --- MÉTHODES PRIVÉES ---

    def _get_max_initiative(self) -> int:
        """Return the highest initiative among all tiles on the board."""
        return max(
            max(tilemodel.initiative) for army in self.board.armies
            for tilemodel in self.board.tiles[army]
        )

    def _get_enemy_army(self, army_name: str) -> str:
        """Identifies the opposing army based on the provided army name."""
        return next_element(self.board.armies, army_name)

    def _apply_cac_attacks(self, tilemodel: Tile, enemy_army_name: str):
        """
        Executes all close-quarters attacks for a given tile.

        This function iterates over the cac attack directions and 
        powers defined for the attacking tile. 
        For each attack, it delegates the damage application to `_process_cac_attack`,
        handling the targeting and damage mechanics.

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

        This function iterates over the ranged attack directions and
        powers defined for the attacking tile. 
        For each attack, it delegates the damage application to `_process_range_attack`,
        handling the targeting and damage mechanics.

        Args:
            tilemodel (Tile): The attacking tile performing the ranged attacks.
            enemy_army_name (str): The name of the enemy army to target.
        """
        if tilemodel.range_attacks_direction:
            for index, range_attack_direction in \
                    enumerate(tilemodel.range_attacks_direction):
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
        Processes a close-quarters combat (CQC) attack from a tile,
        applying damage to an enemy tile in the specified direction.

        This function calculates the position of the target based
        on the attacking tile's position and 
        the direction ofthe attack. 
        If an enemy tile is found at the calculated position,
        it reduces the enemy's life points by 
        the specified attack power.

        Args:
            tilemodel (Tile): The attacking tile performing the close-combat attack.
            enemy_army_name (str): The name of the enemy army to target.
            cac_attack_direction (Tuple[int, int, int]): The direction of the attack
                                                        in cube coordinates.
            cac_attack_power (int): The power of the close-combat attack.
        """

        cac_attack_position = calculate_position(
            tilemodel.board_position, cac_attack_direction
        )
        enemy_tilemodel = self.board.find_army_tile_at_position(
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
            range_attack_direction (Tuple[int, int, int]): The direction of 
                                        the ranged attack in cube coordinates.
            range_attack_power (int): The base power of the ranged attack.
        """
        touched = False
        range_attack_position = tilemodel.board_position
        while self._is_within_board_range(range_attack_position) \
                or not touched:

            range_attack_position = calculate_position(
                range_attack_position, range_attack_direction
            )
            enemy_tilemodel = self.board.find_army_tile_at_position(
                enemy_army_name,
                range_attack_position
            )
            if enemy_tilemodel and enemy_tilemodel.life_point:
                if enemy_tilemodel.shields_position:
                    for shield in enemy_tilemodel.shields_position:
                        if range_attack_direction == \
                                tuple([z * -1 for z in shield]):
                            shield_point = 1

                    enemy_tilemodel.life_point -= (
                        range_attack_power - shield_point)
                    touched = True

    def _get_pixel_positions_cac_attacks(self,
                                        tilemodel: Tile
                                        ) -> List[Tuple[int, int]] | None:
        """Retrieves the pixel positions of all valid CQC attack directions of the tile.

        Args:
            tilemodel (Tile): Tile used

        Returns:
            List[Tuple[int, int]] | None: List of pixel positions or
                                        None if the tile had any CQC attacks
        """
        if tilemodel.range_attacks_direction:
            real_range_attack_directions = [
                calculate_position(x, tilemodel.board_position)
                for x in tilemodel.range_attacks_direction
            ]
            return list_cubes_to_pixel(real_range_attack_directions)

    def _get_pixel_positions_range_attacks(self,
                                        tilemodel: Tile
                                        ) -> List[Tuple[int, int]] | None:
        """Retrieves the pixel positions of all valid ranged attack directions.

        Args:
            tilemodel (Tile): Tile used

        Returns:
            List[Tuple[int, int]] | None: List of pixel positions or
            None if the tile had any ranged attacks
        """
        if tilemodel.cac_attacks_direction is not None:
            real_cac_attack_directions = [
                calculate_position(x, tilemodel.board_position)
                for x in tilemodel.cac_attacks_direction
            ]
            return list_cubes_to_pixel(real_cac_attack_directions)

    def _is_within_board_range(self,
                            cube_position: Tuple[int, int, int],
                            max_range: int = 2
                            ):
        """Verifies whether a position is within the valid board range."""
        return all(abs(coord) <= max_range for coord in cube_position)

    def _prompt_and_get_attacke_direction_convertion(
        self,
        tilemodel: Tile,
        attack_pixel_positions: List[Tuple[int, int]],
        event_list: List[pygame.event.Event]
    ) -> Tuple[int, int, int] | None:
        """
        Prompts the user to select an attack direction to convert and
        returns the chosen direction.

        Args:
            tilemodel (Tile): Tile for which to convert an attack .
            attack_pixel_positions (List[Tuple[int, int]]): List of the pixel position attacks
                                                        of the Tile 'tilemodel'.
            event_list (List[pygame.event.Event]e_): Pygame event list.

        Returns:
            Tuple[int, int, int] | None: Return the cube directions of the attack to convert.
        """
        for pixel_position in attack_pixel_positions:
            hex = self.view.boardzone.get_hexagone_by_position(
                pixel_position)
            if hex.attacks_range_click_button(event_list,
                                            self.view.boardzone.drawsurf
                                            ):
                cube_coord = coordinates_pixel_to_cube(
                    pixel_position)
                cube_coord = tuple(
                    map(operator.sub, cube_coord, tilemodel.board_position))
                return cube_coord

    def _converte_attacks_and_copy_tile(self,
                        tilemodel: Tile,
                        range_attack_to_converte: Tuple[int, int, int] | None,
                        cac_attack_to_converte: Tuple[int, int, int] | None
                    ) -> Tile:
        """Creates a copy of the tile and converts a specified attack.

        Args:
            tilemodel (Tile): Tile to copy and convert
            range_attack_to_converte (Tuple[int, int, int] | None): Ranged attack to convert. 
                                                                    None if any
            cac_attack_to_converte (Tuple[int, int, int] | None): CQC attack to convert.
                                                                    None if any

        Returns:
            Tile: The copied tile with converted attack
        """
        tilecopy = copy.deepcopy(tilemodel)
        if range_attack_to_converte:
            self._converte_range_attack(tilecopy, range_attack_to_converte)
        if cac_attack_to_converte:
            self._converte_cac_attack(tilecopy, cac_attack_to_converte)
        return tilecopy

    def _converte_range_attack(self,
                            tilemodel: Tile,
                            range_attack_to_converte: Tuple[int, int, int]
                            ) -> None:
        """Converts a ranged attack into a CQC attack.

        Args:
            tilemodel (Tile): Tile to convert.
            range_attack_to_converte (Tuple[int, int, int]): Attack direction to convert.
        """
        index_power = tilemodel.range_attacks_direction.index(
            range_attack_to_converte)
        tilemodel.range_attacks_direction.remove(range_attack_to_converte)
        power = tilemodel.range_attacks_power[index_power]
        tilemodel.cac_attacks_direction.append(range_attack_to_converte)
        tilemodel.cac_attacks_power.append(power)

    def _converte_cac_attack(self,
                            tilemodel: Tile,
                            cac_attack_to_converte: Tuple[int, int, int]
                            ) -> None:
        """Converts a CQC attack into a ranged attack.

        Args:
            tilemodel (Tile): Tile to convert.
            cac_attack_to_converte (Tuple[int, int, int]): Attack direction to convert.
        """
        index_power = tilemodel.cac_attacks_direction.index(
            cac_attack_to_converte)
        tilemodel.cac_attacks_direction.remove(cac_attack_to_converte)
        power = tilemodel.cac_attacks_power[index_power]
        tilemodel.range_attacks_direction.append(cac_attack_to_converte)
        tilemodel.range_attacks_power.append(power)
