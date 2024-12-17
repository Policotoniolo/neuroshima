import pytest

import scripts.model.model as model
import scripts.utils.config as config


### Tests Tile Class ###

class TestTile():
    def setup_method(self, method):
        print(f"Setting up {method}")
        self.tile = model.Tile(
            kind="unite",
            army_name="borgo",
            id_tile="borgo-mutant1",
            initiative=[0],
            range_attacks_direction=[(-1, 0, 1),(0, -1, +1), (1, -1, 0)],
            range_attacks_power=[1,1,1],
            cac_attacks_direction=[(-1, 0, 1),(0, -1, +1), (1, -1, 0)],
            cac_attacks_power=[1,1,1],
            net_directions=[(0, -1, +1)],
            life_point=1,
            shields_directions=[(0,-1,1)],
            special_capacities=[],
            module=[{"cac_augment":[(-1, 0, 1),(0, -1, +1), (1, -1, 0)]},
                    {"range_augment":[(-1, 0, 1),(0, -1, +1), (1, -1, 0)]}],
            action=None,
            url_image="image/armies/borgo-mutant.png",
            board_position=(-1, -1, -1)
            )

    def teardown_method(self, method):
        print(f"Tearing down {method}\n")
        del self.tile

    ### Test rotations ###
    
    def test__direction_positive_rotation(self):
        result = self.tile._direction_positive_rotation((0,-1,1))
        assert result == (1,-1,0)
    
    def test_rotation_direction(self):
        result = self.tile._directions_rotation([(0,0,0)], 2)
        assert result == [(0,0,0)]
    
    def test_rotation_positive(self):
        self.tile.rotate_tile(2)
        assert self.tile.rotational_index == 2
        assert self.tile.cac_attacks_direction==[(1,-1,0),(1,0,-1),(0,1,-1)]
        assert self.tile.range_attacks_direction==[(1,-1,0),(1,0,-1),(0,1,-1)]
        assert self.tile.shields_directions==[(1,0,-1)]
        assert self.tile.net_directions==[(1,0,-1)]
        assert self.tile.module == [
                            {"cac_augment":[(1,-1,0),(1,0,-1),(0,1,-1)]},
                            {"range_augment":[(1,-1,0),(1,0,-1),(0,1,-1)]}
        ]

    def test_rotation_negative(self):
        self.tile.rotate_tile(2)
        self.tile.rotate_tile(0)
        assert self.tile.rotational_index == 0
        assert self.tile.cac_attacks_direction==[(-1, 0, 1),(0, -1, +1), (1, -1, 0)]
        assert self.tile.range_attacks_direction==[(-1, 0, 1),(0, -1, +1), (1, -1, 0)]
        assert self.tile.shields_directions==[(0, -1, +1)]
        assert self.tile.net_directions==[(0, -1, +1)]
        assert self.tile.module == [
                            {"cac_augment":[(-1, 0, 1),(0, -1, +1), (1, -1, 0)]},
                            {"range_augment":[(-1, 0, 1),(0, -1, +1), (1, -1, 0)]}
        ]


    def test_rotation_wrong(self):
        with pytest.raises(ValueError):
            self.tile.rotate_tile(8)

    def test_rotation_same(self):
        self.tile.rotate_tile(self.tile.rotational_index)


### Tests Deck Class ###

class TestDeck:
    def setup_method(self, method):
        print(f"Setting up {method}")
        def mock_get_army(self):
            return [{"kind": "base",
            "army_name":"borgo",
            "id_tile":"borgo-qg",
            "initiative": [0],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":[(0, -1, +1), 
                                    (1, -1, 0),
                                    (1, 0, -1),
                                    (0, 1, -1),
                                    (-1, 1, 0),
                                    (-1, 0, 1)
                                    ],
            "cac_attacks_power":[1,1,1,1,1,1],
            "net_directions":None,
            "life_point":20,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":None,
            "url_image":"image/armies/borgo-qg.png"},
        {"kind": "unite",
            "army_name":"borgo",
            "id_tile":"borgo-mutant1",
            "initiative": [2],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":[(-1, 0, 1),(0, -1, +1), (1, -1, 0)],
            "cac_attacks_power":[1,1,1],
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":None,
            "url_image":"image/armies/borgo-mutant.png"},
        {"kind": "unite",
            "army_name":"borgo",
            "id_tile":"borgo-mutant2",
            "initiative": [2],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":[(-1, 0, 1),(0, -1, +1), (1, -1, 0)],
            "cac_attacks_power":[1,1,1],
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":None,
            "url_image":"image/armies/borgo-mutant.png"}
            ]
        with pytest.MonkeyPatch.context() as m:
            m.setattr(model.Deck, "_get_army", mock_get_army)
            self.deck = model.Deck("TestArmy")

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
        assert (top_tile.id_tile == "borgo-mutant1" or
                top_tile.id_tile == "borgo-mutant2")
        assert len(self.deck.tiles) == initial_size - 1

    def test_deck_shuffle(self):
        original_order = [tile.id_tile for tile in self.deck.tiles]
        self.deck._shuffle_deck()
        shuffled_order = [tile.id_tile for tile in self.deck.tiles]
        assert set(original_order) == set(shuffled_order)
        assert len(original_order) == len(shuffled_order)

