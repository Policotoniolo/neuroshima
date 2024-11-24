from typing import List

from model_script import HexBoard, Tile
from functions import next_element, calculate_position


class ModuleEvaluator:
    def __init__(self, board: HexBoard) -> None:
        self.board = board

    def apply_all_effect_modules(self):
        for army_name in self.board.armies:
            self._apply_prio_effect_modules_army(army_name)
            self._apply_non_prio_effect_modules_army(army_name)

    def clean_all_effect_modules(self):
        for tile in self.board.tiles[self.board.armies[0]]:
            for effect in tile.module_effects:
                self._clean_one_effect_on_tile(tile, effect)
        for tile in self.board.tiles[self.board.armies[1]]:
            for effect in tile.module_effects:
                self._clean_one_effect_on_tile(tile, effect)

    def apply_active_module_effect(self):
        self._clean_active_module_effect()
        modules = self._get_active_army_modules()
        for module in modules:
            if module.id_tile == "hegemony-transport":
                list_effects, list_effects_position = self._get_effects_modules([
                                                                                module])
                for index, effect in enumerate(list_effects):
                    effect_position = list_effects_position[index]
                    tile = self.board.find_any_tile_at_position(
                        effect_position)
                    if tile is not None:
                        tile.module_effects.append("transport")
                        tile.special_capacities.append("movement")

# --- MÉTHODES PRIVÉES ---

    def _apply_medic_effect_on_tile(self, tilemodel: Tile) -> None:
        tilemodel.module_effects.append("medic")

    def _apply_cac_augment_effect_on_tile(self, tilemodel: Tile) -> None:
        tilemodel.module_effects.append("cac_augment")
        if tilemodel.cac_attacks_power is not None:
            tilemodel.cac_attacks_power = (
                [cac_attack_power + 1 for cac_attack_power in tilemodel.cac_attacks_power]
            )

    def _apply_range_augment_effect_on_tile(self, tilemodel: Tile) -> None:
        tilemodel.module_effects.append("range_augment")
        if tilemodel.range_attacks_power is not None:
            tilemodel.range_attacks_power = (
                [range_attack_power +
                    1 for range_attack_power in tilemodel.range_attacks_power]
            )

    def _apply_initiative_augment_effect_on_tile(self, tilemodel: Tile) -> None:
        tilemodel.module_effects.append("initiative_augment")
        if tilemodel.initiative is not None:
            tilemodel.initiative = (
                [initiative + 1 for initiative in tilemodel.initiative]
            )

    def _apply_double_initiative_effect_on_tile(self, tilemodel: Tile) -> None:
        tilemodel.module_effects.append("double_initiative")
        if tilemodel.initiative is not None:
            min_init = min(tilemodel.initiative)
            new_init = min_init - 1
            tilemodel.initiative.append(new_init)

    def _apply_saboteur_effect_on_tile(self, tilemodel: Tile) -> None:
        tilemodel.module_effects.append("saboteur")
        if tilemodel.initiative is not None:
            for index, init in enumerate(tilemodel.initiative):
                tilemodel.initiative[index] = init-1

    def _apply_scoper_effect_on_tile(self, tilemodel: Tile) -> None:
        if tilemodel.kind == "module":
            tilemodel.module_effects.append("scoper")
            self.board.remove_tile_from_board(tilemodel.id_tile)
            tilemodel.army_name = next_element(
                self.board.armies, tilemodel.army_name)
            self.board.add_tile_to_board(tilemodel)

    def _apply_quartiermaitre_effect_on_tile(self, tilemodel: Tile) -> None:
        tilemodel.module_effects.append("quartiermaitre")

    def _apply_one_effect_on_tile(self, tilemodel: Tile, effect_type: str) -> None:
        if effect_type == "medic":
            self._apply_medic_effect_on_tile(tilemodel)
        elif effect_type == "cac_augment":
            self._apply_cac_augment_effect_on_tile(tilemodel)
        elif effect_type == "range_augment":
            self._apply_range_augment_effect_on_tile(tilemodel)
        elif effect_type == "initiative_augment":
            self._apply_initiative_augment_effect_on_tile(tilemodel)
        elif effect_type == "double_initiative":
            self._apply_double_initiative_effect_on_tile(tilemodel)
        elif effect_type == "saboteur":
            self._apply_saboteur_effect_on_tile(tilemodel)
        elif effect_type == "scoper":
            self._apply_scoper_effect_on_tile(tilemodel)
        elif effect_type == "quartiermaitre":
            self._apply_quartiermaitre_effect_on_tile(tilemodel)

    def _get_prio_army_modules(self, army_name: str):
        modules_prio = []
        for tile in self.board.tiles[army_name]:
            if tile.kind == "module":
                if tile.id_tile == "outpost-derivateur":
                    modules_prio.append(tile)
        return modules_prio

    def _get_effects_modules(self, modules: List[Tile]):
        liste_effects_prio = []
        liste_effects_position_prio = []
        for module_tile in modules:
            if module_tile.module is not None and module_tile.board_position is not None:
                for effect in module_tile.module:
                    effect_type = list(effect.keys())[0]
                    affected_position = list(effect.values())[0]
                    affected_position = [calculate_position(x, module_tile.board_position )
                                        for x in affected_position]
                    liste_effects_prio.append(effect_type)
                    liste_effects_position_prio.append(affected_position)
        return (liste_effects_prio, liste_effects_position_prio)

    def _get_non_prio_army_modules(self, army_name: str):
        modules = []
        for tile in self.board.tiles[army_name]:
            if tile.kind == "module":
                if tile.id_tile != "outpost-derivateur":
                    modules.append(tile)
        return modules

    def _apply_prio_effect_modules_army(self, army_name: str):
        modules_prio = self._get_prio_army_modules(army_name)
        list_effects_prio, list_effects_position_prio = self._get_effects_modules(
            modules_prio)
        for index, effect_prio in enumerate(list_effects_prio):
            effect_position_prio = list_effects_position_prio[index]
            tile = self.board.find_army_tile_at_position(
                army_name, effect_position_prio)
            if tile is not None:
                self._apply_one_effect_on_tile(tile, effect_prio)

    def _apply_non_prio_effect_modules_army(self, army_name: str):
        modules_non_prio = self._get_non_prio_army_modules(army_name)
        list_effects_non_prio, list_effects_position_non_prio = self._get_effects_modules(
            modules_non_prio)
        for index, effect_non_prio in enumerate(list_effects_non_prio):
            effect_position_non_prio = list_effects_position_non_prio[index]
            tile = self.board.find_army_tile_at_position(
                army_name, effect_position_non_prio)
            if tile is not None:
                self._apply_one_effect_on_tile(tile, effect_non_prio)

    def _clean_medic_effect_on_tile(self, tilemodel: Tile) -> None:
        tilemodel.module_effects.remove("medic")

    def _clean_cac_augment_effect_on_tile(self, tilemodel: Tile) -> None:
        tilemodel.module_effects.remove("cac_augment")
        if tilemodel.cac_attacks_power is not None:
            tilemodel.cac_attacks_power = (
                [cac_attack_power - 1 for cac_attack_power in tilemodel.cac_attacks_power]
            )

    def _clean_range_augment_effect_on_tile(self, tilemodel: Tile) -> None:
        tilemodel.module_effects.remove("range_augment")
        if tilemodel.range_attacks_power is not None:
            tilemodel.range_attacks_power = (
                [range_attack_power -
                    1 for range_attack_power in tilemodel.range_attacks_power]
            )

    def _clean_initiative_augment_effect_on_tile(self, tilemodel: Tile) -> None:
        tilemodel.module_effects.remove("initiative_augment")
        if tilemodel.initiative is not None:
            tilemodel.initiative = (
                [initiative - 1 for initiative in tilemodel.initiative]
            )

    def _clean_double_initiative_effect_on_tile(self, tilemodel: Tile) -> None:
        tilemodel.module_effects.remove("double_initiative")
        if tilemodel.initiative is not None and len(tilemodel.initiative) >= 2:
            min_init = min(tilemodel.initiative)
            tilemodel.initiative.remove(min_init)

    def _clean_saboteur_effect_on_tile(self, tilemodel: Tile) -> None:
        tilemodel.module_effects.remove("saboteur")
        if tilemodel.initiative is not None:
            for index, init in enumerate(tilemodel.initiative):
                tilemodel.initiative[index] = init+1

    def _clean_scoper_effect_on_tile(self, tilemodel: Tile) -> None:
        if tilemodel.kind == "module":
            tilemodel.module_effects.remove("scoper")
            self.board.remove_tile_from_board(tilemodel.id_tile)
            tilemodel.army_name = next_element(
                self.board.armies, tilemodel.army_name)
            self.board.add_tile_to_board(tilemodel)

    def _clean_quartiermaitre_effect_on_tile(self, tilemodel: Tile) -> None:
        tilemodel.module_effects.remove("quartiermaitre")

    def _clean_one_effect_on_tile(self, tilemodel: Tile, effect_type: str) -> None:
        if effect_type == "medic":
            self._clean_medic_effect_on_tile(tilemodel)
        elif effect_type == "cac_augment":
            self._clean_cac_augment_effect_on_tile(tilemodel)
        elif effect_type == "range_augment":
            self._clean_range_augment_effect_on_tile(tilemodel)
        elif effect_type == "initiative_augment":
            self._clean_initiative_augment_effect_on_tile(tilemodel)
        elif effect_type == "double_initiative":
            self._clean_double_initiative_effect_on_tile(tilemodel)
        elif effect_type == "saboteur":
            self._clean_saboteur_effect_on_tile(tilemodel)
        elif effect_type == "scoper":
            self._clean_scoper_effect_on_tile(tilemodel)
        elif effect_type == "quartiermaitre":
            self._clean_quartiermaitre_effect_on_tile(tilemodel)

    def _get_active_army_modules(self):
        modules_active = []
        for army_name in self.board.armies:
            tiles = self.board.tiles[army_name]
            for tile in tiles:
                if tile.kind == "module":
                    if tile.id_tile == "hegemony-transport":
                        modules_active.append(tile)
        return modules_active

    def _clean_active_module_effect(self):
        for tile in self.board.tiles[self.board.armies[0]]:
            if "transport" in tile.module_effects:
                tile.module_effects.append("transport")
                tile.special_capacities.append("movement")
        for tile in self.board.tiles[self.board.armies[1]]:
            if "transport" in tile.module_effects:
                tile.module_effects.append("transport")
                tile.special_capacities.append("movement")
