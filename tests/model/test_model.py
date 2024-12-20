import pytest
import unittest.mock as mock

import scripts.model.model as models
import scripts.utils.functions as functions


### Tests Tile Class ###

class TestTile():
    def setup_method(self, method):
        print(f"Setting up {method}")
        self.tile = models.Tile(
            kind="unite",
            army_name="borgo",
            id_tile="borgo-mutant1",
            initiative=[0],
            range_attacks_direction=[(-1, 0, 1), (0, -1, +1), (1, -1, 0)],
            range_attacks_power=[1, 1, 1],
            cac_attacks_direction=[(-1, 0, 1), (0, -1, +1), (1, -1, 0)],
            cac_attacks_power=[1, 1, 1],
            net_directions=[(0, -1, +1)],
            life_point=1,
            shields_directions=[(0, -1, 1)],
            special_capacities=[],
            module=[{"cac_augment": [(-1, 0, 1), (0, -1, +1), (1, -1, 0)]},
                    {"range_augment": [(-1, 0, 1), (0, -1, +1), (1, -1, 0)]}],
            action=None,
            url_image="image/armies/borgo-mutant.png",
            board_position=(-1, -1, -1)
        )

    def teardown_method(self, method):
        print(f"Tearing down {method}\n")
        del self.tile

    # tests

    def test__direction_positive_rotation(self):
        result = self.tile._direction_positive_rotation((0, -1, 1))
        assert result == (1, -1, 0)

    def test_rotation_direction(self):
        result = self.tile._directions_rotation([(0, 0, 0)], 2)
        assert result == [(0, 0, 0)]

    def test_rotation_positive(self):
        self.tile.rotate_tile(2)
        assert self.tile.rotational_index == 2
        assert self.tile.cac_attacks_direction == [
            (1, -1, 0), (1, 0, -1), (0, 1, -1)]
        assert self.tile.range_attacks_direction == [
            (1, -1, 0), (1, 0, -1), (0, 1, -1)]
        assert self.tile.shields_directions == [(1, 0, -1)]
        assert self.tile.net_directions == [(1, 0, -1)]
        assert self.tile.module == [
            {"cac_augment": [(1, -1, 0), (1, 0, -1), (0, 1, -1)]},
            {"range_augment": [
                (1, -1, 0), (1, 0, -1), (0, 1, -1)]}
        ]

    def test_rotation_negative(self):
        self.tile.rotate_tile(2)
        self.tile.rotate_tile(0)
        assert self.tile.rotational_index == 0
        assert self.tile.cac_attacks_direction == [
            (-1, 0, 1), (0, -1, +1), (1, -1, 0)]
        assert self.tile.range_attacks_direction == [
            (-1, 0, 1), (0, -1, +1), (1, -1, 0)]
        assert self.tile.shields_directions == [(0, -1, +1)]
        assert self.tile.net_directions == [(0, -1, +1)]
        assert self.tile.module == [
            {"cac_augment": [(-1, 0, 1), (0, -1, +1), (1, -1, 0)]},
            {"range_augment": [
                (-1, 0, 1), (0, -1, +1), (1, -1, 0)]}
        ]

    def test_rotation_wrong(self):
        with pytest.raises(
            ValueError, match="new_rotation_direction must be between 0 and 5."
        ):
            self.tile.rotate_tile(8)

    def test_rotation_same(self):
        self.tile.rotate_tile(self.tile.rotational_index)


### Tests Deck Class ###

class TestDeck:

    def mock_get_army(self):
        return [{"kind": "base",
                "army_name": "armytest",
                "id_tile": "armytest-qg",
                "initiative": [0],
                "range_attacks_direction": None,
                "range_attacks_power": None,
                "cac_attacks_direction": [(0, -1, +1),
                                        (1, -1, 0),
                                        (1, 0, -1),
                                        (0, 1, -1),
                                        (-1, 1, 0),
                                        (-1, 0, 1)
                                        ],
                "cac_attacks_power": [1, 1, 1, 1, 1, 1],
                "net_directions": None,
                "life_point": 20,
                "shields_directions": None,
                "special_capacities": [],
                "module": None,
                "action": None,
                "url_image": "image/armies/armytest-qg.png"},
            {"kind": "unite",
                "army_name": "armytest",
                "id_tile": "armytest1",
                "initiative": [2],
                "range_attacks_direction": None,
                "range_attacks_power": None,
                "cac_attacks_direction": [(-1, 0, 1), (0, -1, +1), (1, -1, 0)],
                "cac_attacks_power": [1, 1, 1],
                "net_directions": None,
                "life_point": 1,
                "shields_directions": None,
                "special_capacities": [],
                "module": None,
                "action": None,
                "url_image": "image/armies/armytest-mutant.png"},
            {"kind": "unite",
                "army_name": "armytest",
                "id_tile": "armytest2",
                "initiative": [2],
                "range_attacks_direction": None,
                "range_attacks_power": None,
                "cac_attacks_direction": [(-1, 0, 1), (0, -1, +1), (1, -1, 0)],
                "cac_attacks_power": [1, 1, 1],
                "net_directions": None,
                "life_point": 1,
                "shields_directions": None,
                "special_capacities": [],
                "module": None,
                "action": None,
                "url_image": "image/armies/armytest-mutant.png"}
                ]

    def setup_method(self, method):
        print(f"Setting up {method}")
        with pytest.MonkeyPatch.context() as m:
            m.setattr(models.Deck, "_get_army", self.mock_get_army)
            self.deck = models.Deck("TestArmy")

    def teardown_method(self, method):
        print(f"Tearing down {method}\n")
        del self.deck


    def test_deck_initialization(self):
        assert len(self.deck.tiles) == 2
        assert self.deck.hq_tile.kind == "base"

    def test_init_hq_tile_wrong(self):
        with pytest.raises(ValueError):
            # already init, hq tile not in deck tiles list
            self.deck._init_hq_tile()

    def test_deck_remove_top_tile(self):
        initial_size = len(self.deck.tiles)
        top_tile = self.deck.remove_top_deck_tile()
        assert (top_tile.id_tile == "armytest1" or
                top_tile.id_tile == "armytest2")
        assert len(self.deck.tiles) == initial_size - 1

    def test_deck_shuffle(self):
        original_order = [tile.id_tile for tile in self.deck.tiles]
        self.deck._shuffle_deck()
        shuffled_order = [tile.id_tile for tile in self.deck.tiles]
        assert set(original_order) == set(shuffled_order)
        assert len(original_order) == len(shuffled_order)

    def test_dict_to_tile_wrong(self):
        wrong_dic_type = ["some wrong data"]
        with pytest.raises(TypeError):
            self.deck._dict_to_tile(wrong_dic_type)

    @mock.patch("importlib.import_module")
    def test_get_army_success(self, mock_import_module):
        mock_module = mock.MagicMock()
        setattr(mock_module, "TestArmy", self.mock_get_army)
        mock_import_module.return_value = mock_module
        result = self.deck._get_army()

        mock_import_module.assert_called_once_with("scripts.armies.TestArmy")
        assert result == self.mock_get_army

    @mock.patch("importlib.import_module", side_effect=ModuleNotFoundError)
    def test_get_army_module_not_found(self, mock_import_module):
        with pytest.raises(
                ValueError, match="Army module 'TestArmy' not found."
            ):
            self.deck._get_army()
        mock_import_module.assert_called_once_with("scripts.armies.TestArmy")

    @mock.patch("importlib.import_module")
    def test_get_army_attribute_not_found(self, mock_import_module):
        mock_module = mock.MagicMock()
        del mock_module.TestArmy
        mock_import_module.return_value = mock_module

        with pytest.raises(
            ValueError, match="Army 'TestArmy' not defined in the module."
        ):
            self.deck._get_army()
        mock_import_module.assert_called_once_with("scripts.armies.TestArmy")


### Tests Deck Class ###

class TestHand():
    @mock.patch('scripts.model.model.Tile', autospec=True)
    def setup_method(self, method, mocktile):
        print(f"Setting up {method}")

        self.hand = models.Hand()

        mocktile.id_tile = 'test_tile'
        self.mocktile = mocktile
        self.hand.hand_tiles.append(mocktile)

    def teardown_method(self, method):
        print(f"Tearing down {method}\n")
        del self.hand
        del self.mocktile

    # tests

    @mock.patch('scripts.model.model.Tile')
    def test_add_tile_success(self, newmocktile):
        newmocktile.id_tile = 'new_test_tile'
        self.hand.add_tile(newmocktile)
        assert len(self.hand.hand_tiles) == 2
        assert newmocktile in self.hand.hand_tiles
        assert self.mocktile in self.hand.hand_tiles

    @mock.patch('scripts.model.model.Tile')
    def test_add_tile_wrong(self, newmocktile):
        self.hand.add_tile(newmocktile)
        self.hand.add_tile(newmocktile)
        with pytest.raises(ValueError):
            self.hand.add_tile(newmocktile)

    def test_discard_tile_success(self):
        self.hand.discard_tile([self.mocktile])
        assert len(self.hand.hand_tiles) == 0

    @mock.patch('scripts.model.model.Tile')
    def test_discard_tile_wrong(self, mockwrongtile):
        mockwrongtile.id_tile = "wrong_tile"
        with pytest.raises(
            ValueError, match="Tile wrong_tile not found in hand."
        ):
            self.hand.discard_tile([mockwrongtile])

    def test_get_tile_by_id_success(self):
        id_tile = self.mocktile.id_tile
        result = self.hand.get_tile_by_id(id_tile)
        assert result == self.mocktile

    def test_get_tile_by_id_wrong(self):
        with pytest.raises(ValueError):
            self.hand.get_tile_by_id(id_tile="wrong_id")


### Tests Player Class ###

class TestPlayer():
    def mock_get_army(self):
        return [{"kind": "base",
                "army_name": "armytest",
                "id_tile": "armytest-qg",
                "initiative": [0],
                "range_attacks_direction": None,
                "range_attacks_power": None,
                "cac_attacks_direction": [(0, -1, +1),
                                        (1, -1, 0),
                                        (1, 0, -1),
                                        (0, 1, -1),
                                        (-1, 1, 0),
                                        (-1, 0, 1)
                                        ],
                "cac_attacks_power": [1, 1, 1, 1, 1, 1],
                "net_directions": None,
                "life_point": 20,
                "shields_directions": None,
                "special_capacities": [],
                "module": None,
                "action": None,
                "url_image": "image/armies/armytest-qg.png"},
            {"kind": "unite",
                "army_name": "armytest",
                "id_tile": "armytest1",
                "initiative": [2],
                "range_attacks_direction": None,
                "range_attacks_power": None,
                "cac_attacks_direction": [(-1, 0, 1), (0, -1, +1), (1, -1, 0)],
                "cac_attacks_power": [1, 1, 1],
                "net_directions": None,
                "life_point": 1,
                "shields_directions": None,
                "special_capacities": [],
                "module": None,
                "action": None,
                "url_image": "image/armies/armytest-mutant.png"},
            {"kind": "unite",
                "army_name": "armytest",
                "id_tile": "armytest2",
                "initiative": [2],
                "range_attacks_direction": None,
                "range_attacks_power": None,
                "cac_attacks_direction": [(-1, 0, 1), (0, -1, +1), (1, -1, 0)],
                "cac_attacks_power": [1, 1, 1],
                "net_directions": None,
                "life_point": 1,
                "shields_directions": None,
                "special_capacities": [],
                "module": None,
                "action": None,
                "url_image": "image/armies/armytest-mutant.png"}
                ]

    def setup_method(self, method):
        print(f"Setting up {method}")
        with pytest.MonkeyPatch.context() as m:
            m.setattr(models.Deck, "_get_army", self.mock_get_army)
            self.player = models.Player("testname", "testarmy")

    def teardown_method(self, method):
        print(f"Tearing down {method}\n")
        del self.player

    def test_get_tiles_success(self):
        tile_to_draw = self.player.deck.tiles[0]
        self.player.get_tiles(1)

        assert tile_to_draw in self.player.hand.hand_tiles
        assert tile_to_draw not in self.player.deck.tiles
        assert len(self.player.hand.hand_tiles) == 1

    def test_get_tiles_wrong_value(self):
        with pytest.raises(ValueError):
            self.player.get_tiles(4)

    def test_get_tiles_zero_ask(self):
        old_hand = self.player.hand.hand_tiles.copy()
        old_deck = self.player.deck.tiles.copy()
        self.player.get_tiles(0)
        assert self.player.hand.hand_tiles == old_hand
        assert self.player.deck.tiles == old_deck

    def test_discard_tiles_hand_empty(self):
        self.player.hand.hand_tiles = []
        old_deck = self.player.deck.tiles.copy()
        assert self.player.discard_tiles_hand() is None
        assert self.player.hand.hand_tiles == []
        assert self.player.deck.tiles == old_deck

    @mock.patch('scripts.model.model.Tile')
    @mock.patch('scripts.model.model.Tile')
    def test_discard_tiles_hand_success(self, mocktile1, mocktile2):
        mocktile1.id_tile = 'id_tile_1'
        mocktile2.id_tile = 'id_tile_2'
        self.player.hand.hand_tiles = [mocktile1, mocktile2]
        self.player.deck.defausse = []
        self.player.discard_tiles_hand(['id_tile_1'])
        assert self.player.hand.hand_tiles == [mocktile1]
        assert self.player.deck.defausse == [mocktile2]


### Tests HexBoard ###

class TestHexBoard():
    def setup_method(self, method):
        print(f"Setting up {method}")

        self.mock_hq_tile1 = mock.MagicMock(
            spec=models.Tile)
        self.mock_hq_tile2 = mock.MagicMock(
            spec=models.Tile)

        self.mock_tiles_army1 = [
            mock.MagicMock(spec=models.Tile) for _ in range(5)]
        self.mock_tiles_army2 = [
            mock.MagicMock(spec=models.Tile) for _ in range(5)]

        self.mock_deck1 = mock.MagicMock(tiles=self.mock_tiles_army1,
                                        hq_tile=self.mock_hq_tile1)
        self.mock_deck2 = mock.MagicMock(tiles=self.mock_tiles_army2,
                                        hq_tile=self.mock_hq_tile2)

        self.mock_player1 = mock.MagicMock(deck=self.mock_deck1)
        self.mock_player2 = mock.MagicMock(deck=self.mock_deck2)

        self.hexboard = models.HexBoard(board_limit=3,
                                        armies=["Army1", "Army2"],
                                        players=[self.mock_player1,
                                                self.mock_player2]
                                        )

    def teardown_method(self, method):
        print(f"Tearing down {method}\n")
        del self.hexboard
        del self.mock_hq_tile1
        del self.mock_hq_tile2
        del self.mock_tiles_army1
        del self.mock_tiles_army2
        del self.mock_deck1
        del self.mock_deck2
        del self.mock_player1
        del self.mock_player2

    def test_wrong_board_limit_init_hexboard(self):
        with pytest.raises(ValueError, match="board_limit must be 3 or 4"):
            models.HexBoard(board_limit=5,
                            armies=["Army1", "Army2"],
                            players=[self.mock_player1,
                                    self.mock_player2])

    def test_wrong_armies_init_hexboard(self):
        with pytest.raises(
            ValueError, match="At least two armies must be specified."
            ):
            models.HexBoard(board_limit=3,
                            armies=["Army1"],
                            players=[self.mock_player1,
                                    self.mock_player2])

    def test_create_board(self):
        result = self.hexboard.hexes
        expected_result = [(-2, 0, 2), (-2, 1, 1), (-2, 2, 0), (-1, -1, 2),
                        (-1, 0, 1), (-1, 1, 0), (-1, 2, -1,), (0, -2, 2),
                        (0, -1, 1), (0, 0, 0), (0, 1, -1), (0, 2, -2),
                        (0, 2, -2), (1, -2, 1), (1, -1, 0), (1, 0, -1),
                        (1, 1, -2), (2, -2, 0), (2, -1, -1), (2, -1, -1),
                        (2, 0, -2)
                        ]
        assert set(result) == set(expected_result)

    def test_init_all_tiles(self):
        expected_result = self.mock_tiles_army1 + self.mock_tiles_army2 + \
            [self.mock_hq_tile1, self.mock_hq_tile2]
        assert set(self.hexboard.all_tile) == set(expected_result)
        assert len(expected_result) == len(self.hexboard.all_tile)

    def test_add_tile_to_board_success(self):
        assert self.hexboard.tiles["Army1"] == []
        assert (1, 0, -1) not in self.hexboard.occupied["Army1"]
        assert self.hexboard.position_index["Army1"].get((1, 0, -1)) is None

        tile_to_add = self.mock_tiles_army1[0]
        tile_to_add.army_name = "Army1"
        tile_to_add.board_position = (1, 0, -1)

        self.hexboard.add_tile_to_board(tile_to_add)

        assert self.hexboard.tiles["Army1"] == [tile_to_add]
        assert (1, 0, -1) in self.hexboard.occupied["Army1"]
        assert self.hexboard.position_index["Army1"].get(
            (1, 0, -1)) == tile_to_add

    def test_add_tile_to_board_wrong_type(self):
        with pytest.raises(ValueError, match="tile is not a Tile instance"):
            self.hexboard.add_tile_to_board("wrong_type_arg")

    def test_add_tile_to_board_wrong_position(self):
        tile_to_add = self.mock_tiles_army1[0]
        tile_to_add.board_position = (4, 0, -3)
        with pytest.raises(
                ValueError,
                match=r'tile position not on the board: \(4, 0, -3\)'
            ):
            self.hexboard.add_tile_to_board(tile_to_add)

    def test_add_tile_to_board_occupied_postition(self):
        tile_board = self.mock_tiles_army1[0]
        tile_board.army_name = "Army1"
        tile_board.board_position = (1, 0, -1)
        self.hexboard.add_tile_to_board(tile_board)

        tile_to_add = self.mock_tiles_army1[1]
        tile_to_add.army_name = "Army1"
        tile_to_add.board_position = (1, 0, -1)
        with pytest.raises(ValueError,
                        match=r'Position \(1, 0, -1\) is already occupied.'):
            self.hexboard.add_tile_to_board(tile_to_add)

    def test_add_tile_to_board_already_on_board(self):
        tile_to_add = self.mock_tiles_army1[0]
        tile_to_add.army_name = "Army1"
        tile_to_add.board_position = (1, 0, -1)
        self.hexboard.add_tile_to_board(tile_to_add)
        self.hexboard.add_tile_to_board(tile_to_add)
        assert self.hexboard.tiles["Army1"] == [tile_to_add]

    def test_add_tile_to_board_default_position(self):
        tile_to_add = self.mock_tiles_army1[0]
        tile_to_add.army_name = "Army1"
        tile_to_add.board_position = (-1, -1, -1)
        self.hexboard.add_tile_to_board(tile_to_add)
        assert tile_to_add not in self.hexboard.tiles["Army1"]
        assert (-1, -1, -1) not in self.hexboard.occupied["Army1"]
        assert self.hexboard.position_index["Army1"].get((-1, -1, -1)) is None

    def test_remove_tile_from_board_success(self):
        tile_to_add = self.mock_tiles_army1[0]
        tile_to_add.id_tile = "id_tile_to_add"
        tile_to_add.army_name = "Army1"
        tile_to_add.board_position = (1, 0, -1)
        self.hexboard.add_tile_to_board(tile_to_add)
        self.hexboard.remove_tile_from_board("id_tile_to_add")
        assert tile_to_add not in self.hexboard.tiles["Army1"]
        assert (-1, -1, -1) not in self.hexboard.occupied["Army1"]
        assert self.hexboard.position_index["Army1"].get((-1, -1, -1)) is None

    def test_remove_tile_from_board_wrong_id_tile(self):
        with pytest.raises(
                ValueError,
                match="No tile with ID 'wrong_id_tile' found on the board."):
            self.hexboard.remove_tile_from_board("wrong_id_tile")

    def test_find_army_tile_at_position_no_tile(self):
        result = self.hexboard.find_army_tile_at_position("Army1", (0, 0, 0))
        assert result is None

    def test_find_army_tile_at_position_success(self):
        tile = self.mock_tiles_army1[0]
        tile.army_name = "Army1"
        tile.board_position = (1, 0, -1)
        self.hexboard.add_tile_to_board(tile)
        result = self.hexboard.find_army_tile_at_position("Army1", (1, 0, -1))
        assert result == tile

    def test_find_any_tile_at_position_no_tile(self):
        result = self.hexboard.find_any_tile_at_position((0, 0, 0))
        assert result is None

    def test_find_any_tile_at_position_success(self):
        tile = self.mock_tiles_army1[0]
        tile.army_name = "Army1"
        tile.board_position = (1, 0, -1)
        self.hexboard.add_tile_to_board(tile)
        result = self.hexboard.find_any_tile_at_position((1, 0, -1))
        assert result == tile
