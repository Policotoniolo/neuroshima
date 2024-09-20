class BattleEvaluator:
    """_summary_
    """
    def __init__(self, board) -> None:
        self.board = board

    def higher_initiative(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        initiatives = []
        for tile in self.board.tiles:
            initiatives.append(tile.initiative)
        return max(initiatives)

    def fire(self, player_tile):
        """_summary_

        Args:
            player_tile (_type_): _description_
        """
        player_name = player_tile.player_name

        for index, cac_attack_direction in enumerate(player_tile.cac_attacks_direction):
            cac_attack_position = tuple(map(sum, zip(cac_attack_direction, player_tile.board_position))) 
            
            for enemy_tile in self.board.tiles:
                if enemy_tile.player_name == player_name:
                    continue
                if enemy_tile.board_position == cac_attack_position:
                    enemy_tile.life_point -= player_tile.cac_attack_power[index]
        
        for range_attack_direction in player_tile.range_attacks_direcion:
            touched = False
            range_attack_position = tuple(map(sum, zip(range_attack_direction, player_tile.board_position)))
            while (abs(range_attack_position[0])<=2 and abs(range_attack_position[1])<=2 and abs(range_attack_position[2])<=2) or touched == False:
                for tile in self.board.tiles:
                    if tile.player_name == player_name:
                        continue
                    if tile.board_position == range_attack_position:

                        for shield in tile.shields_position:
                            if range_attack_direction == tuple([z * -1 for z in shield]):
                                shield_point = 1
                        
                        tile.life_point -= range_attack_direction[3] + shield_point
                        touched = True
                    # else:
                        # range_attack_position = tuple(map(sum, zip(range_attack_direction, range_attack_position)))
            

    def battle_round(self, initiative_round: int):
        tiles = [item for item in self.board.tiles if initiative_round in item.initiative]
        for tile in tiles:
            self.fire(tile)
        
        for index, tile in enumerate(self.board.tiles) :
            if tile.life_point < 0:
                self.board.remove_tile_from_board(index)

    def start_battle(self):
        initiative_round = self.higher_initiative()

        while initiative_round >= 0 :
            self.battle_round(initiative_round=initiative_round)
            initiative_round -= 1
            for base_tile in [item for item in self.board.tiles if item["kind"] == "base"]:
                if base_tile.life_point <= 0:
                    loser = base_tile.player_name
                    # self.stop_game(self.board) ## A CREER 