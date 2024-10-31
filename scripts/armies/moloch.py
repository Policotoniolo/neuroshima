"""Module providing all tiles of the moloch army"""
moloch=[{"kind": "base",
            "army_name":"moloch",
            "id_tile":"moloch-qg",
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
            "net":None,
            "life_point":20,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-qg.png"},
        {"kind": "unite",
            "army_name":"moloch",
            "id_tile":"moloch-blocker1",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":3,
            "shields_position":[(0, -1, +1)],
            "special_capacities":None,
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-blocker.png"},
        {"kind": "unite",
            "army_name":"moloch",
            "id_tile":"moloch-blocker2",
            "initiative": [],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":3,
            "shields_position":[(0, -1, +1)],
            "special_capacities":None,
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-blocker.png"},
        {"kind": "unite",
            "army_name":"moloch",
            "id_tile":"moloch-hybrid1",
            "initiative": [3],
            "range_attacks_direction":[(0, -1, +1)],
            "range_attacks_power":[1],
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-hybrid.png"},
        {"kind": "unite",
            "army_name":"moloch",
            "id_tile":"moloch-hybrid2",
            "initiative": [3],
            "range_attacks_direction":[(0, -1, +1)],
            "range_attacks_power":[1],
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-hybrid.png"},
        {"kind": "unite",
            "army_name":"moloch",
            "id_tile":"moloch-canondegauss",
            "initiative": [1],
            "range_attacks_direction":[(-1,1,0)],
            "range_attacks_power":[1],
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":['gauss'],
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-canondegauss.png"},
        {"kind": "unite",
            "army_name":"moloch",
            "id_tile":"moloch-juggernaut",
            "initiative": [1],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":[(0, -1, +1)],
            "cac_attacks_power":[2],
            "net":None,
            "life_point":2,
            "shields_position":[(0,-1,1), (1,0,-1), (-1,1,0)],
            "special_capacities":None,
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-juggernaut.png"},
        {"kind": "unite",
        "army_name":"moloch",
        "id_tile":"moloch-chasseurtueur1",
            "initiative": [3],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":[(-1,1,0), (0,-1,1), (1,-1,0), (0,1,-1)],
            "cac_attacks_power":[1,1,1,1],
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-chasseurtueur.png"},
        {"kind": "unite",
        "army_name":"moloch",
        "id_tile":"moloch-chasseurtueur2",
            "initiative": [3],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":[(-1,1,0), (0,-1,1), (1,-1,0), (0,1,-1)],
            "cac_attacks_power":[1,1,1,1],
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-chasseurtueur.png"},
        {"kind": "unite",
        "army_name":"moloch",
        "id_tile":"moloch-protecteur",
            "initiative": [1],
            "range_attacks_direction":[(-1,0,1), (0,-1,1), (1,-1,0)],
            "range_attacks_power":[1,1,1],
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":2,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-protecteur.png"},
        {"kind": "unite",
            "army_name":"moloch",
            "id_tile":"moloch-chasseurblinde1",
            "initiative": [2],
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
            "net":None,
            "life_point":1,
            "shields_position":[(-1,0,1), (0,-1,1)],
            "special_capacities":None,
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-chasseurblinde.png"},
        {"kind": "unite",
            "army_name":"moloch",
            "id_tile":"moloch-chasseurblinde2",
            "initiative": [2],
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
            "net":None,
            "life_point":1,
            "shields_position":[(-1,0,1), (0,-1,1)],
            "special_capacities":None,
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-chasseurblinde.png"},
        {"kind": "unite",
        "army_name":"moloch",
        "id_tile":"moloch-gardeblinde",
            "initiative": [2],
            "range_attacks_direction":[(-1,0,1), (1,-1,0)],
            "range_attacks_power":[1,1],
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":[(0,-1,1)],
            "special_capacities":None,
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-gardeblinde.png"},
        {"kind": "unite",
        "army_name":"moloch",
        "id_tile":"moloch-garde",
            "initiative": [2],
            "range_attacks_direction":[(-1,0,1), (0,-1,1)],
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-garde.png"},
        {"kind": "unite",
            "army_name":"moloch",
            "id_tile":"moloch-clown",
            "initiative": [2],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":[(-1, 0, 1)],
            "cac_attacks_power":[1],
            "net":None,
            "life_point":2,
            "shields_position":None,
            "special_capacities":['explosion'],
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-clown.png"},
        {"kind": "unite",
            "army_name":"moloch",
            "id_tile":"moloch-eventreur",
            "initiative": [2],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":[0,-1,1],
            "cac_attacks_power":[2],
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-eventreur.png"},
        {"kind": "unite",
            "army_name":"moloch",
            "id_tile":"moloch-retiaire",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":[(-1,0,1), (0,-1,1)],
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-retiaire.png"},
        {"kind": "unite",
            "army_name":"moloch",
            "id_tile":"moloch-troupedassaut",
            "initiative": [2,1],
            "range_attacks_direction":[0,-1,1],
            "range_attacks_power":[1],
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":2,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":None,
            "url_image":"image/armies/moloch-troupedassaut.png"},
        {"kind": "module",
            "army_name":"moloch",
            "id_tile":"moloch-officier1",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":[{"cac_augment":[(-1, 0, 1),(0,1,-1), (1, -1, 0)]}],
            "action":None,
            "url_image":"image/armies/moloch-officier.png"},
        {"kind": "module",
            "army_name":"moloch",
            "id_tile":"moloch-cerveau1",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":[{"cac_augment":[(0,-1,1),(1,0,-1), (-1,1,0)]},
                    {"range_augment":[(0,-1,1),(1,0,-1), (-1,1,0)]}],
            "action":None,
            "url_image":"image/armies/moloch-officier.png"},
        {"kind": "module",
            "army_name":"moloch",
            "id_tile":"moloch-eclaireur1",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":[{"initiative_augment":[(0,-1,1),(1,0,-1), (-1,1,0)]}],
            "action":None,
            "url_image":"image/armies/moloch-eclaireur.png"},
        {"kind": "module",
            "army_name":"moloch",
            "id_tile":"moloch-medecin1",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":[{"medic":[(-1, 1, 0),(0, -1, +1), (1,0,-1)]}],
            "action":None,
            "url_image":"image/armies/moloch-medecin.png"},
        {"kind": "module",
            "army_name":"moloch",
            "id_tile":"moloch-medecin2",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":[{"medic":[(-1, 1, 0),(0, -1, +1), (1,0,-1)]}],
            "action":None,
            "url_image":"image/armies/moloch-medecin.png"},
        {"kind": "module",
            "army_name":"moloch",
            "id_tile":"moloch-cartemere1",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":[{"double_init":[(0, -1, +1)]}],
            "action":None,
            "url_image":"image/armies/moloch-cartemere.png"},
        {"kind": "action",
            "army_name":"moloch",
            "id_tile":"moloch-battle1",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":"battle",
            "url_image":"image/armies/moloch-battle.png"},
        {"kind": "action",
            "army_name":"moloch",
            "id_tile":"moloch-battle2",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":"battle",
            "url_image":"image/armies/moloch-battle.png"},
        {"kind": "action",
            "army_name":"moloch",
            "id_tile":"moloch-battle3",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":"battle",
            "url_image":"image/armies/moloch-battle.png"},
        {"kind": "action",
            "army_name":"moloch",
            "id_tile":"moloch-battle4",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":"battle",
            "url_image":"image/armies/moloch-battle.png"},
        {"kind": "action",
            "army_name":"moloch",
            "id_tile":"moloch-frappeaerienne1",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":"airstrike",
            "url_image":"image/armies/moloch-frappeaerienne.png"},
        {"kind": "action",
        "army_name":"moloch",
        "id_tile":"moloch-mouvement1",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":"movement",
            "url_image":"image/armies/moloch-mouvement.png"},
        {"kind": "action",
        "army_name":"moloch",
        "id_tile":"moloch-poussee1",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":"push",
            "url_image":"image/armies/moloch-poussee.png"},
        {"kind": "action",
        "army_name":"moloch",
        "id_tile":"moloch-poussee2",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":"push",
            "url_image":"image/armies/moloch-poussee.png"},
        {"kind": "action",
        "army_name":"moloch",
        "id_tile":"moloch-poussee3",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":"push",
            "url_image":"image/armies/moloch-poussee.png"},
        {"kind": "action",
        "army_name":"moloch",
        "id_tile":"moloch-poussee4",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":"push",
            "url_image":"image/armies/moloch-poussee.png"},
        {"kind": "action",
        "army_name":"moloch",
        "id_tile":"moloch-poussee5",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net":None,
            "life_point":1,
            "shields_position":None,
            "special_capacities":None,
            "module":None,
            "action":"push",
            "url_image":"image/armies/moloch-poussee.png"}
]
