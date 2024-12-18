"""Module providing all tile of the borgo army"""
import sys
borgo=[{"kind": "base",
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
            "url_image":"image/armies/borgo-mutant.png"},
        {"kind": "unite",
            "army_name":"borgo",
            "id_tile":"borgo-mutant3",
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
            "id_tile":"borgo-mutant4",
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
            "id_tile":"borgo-mutant5",
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
            "id_tile":"borgo-mutant6",
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
        "id_tile":"borgo-bagarreur1",
            "initiative": [1],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":[(0, -1, +1)],
            "cac_attacks_power":[2],
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":None,
            "url_image":"image/armies/borgo-bagarreur.png"},
        {"kind": "unite",
        "army_name":"borgo",
        "id_tile":"borgo-bagarreur2",
            "initiative": [1],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":[(0, -1, +1)],
            "cac_attacks_power":[2],
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":None,
            "url_image":"image/armies/borgo-bagarreur.png"},
        {"kind": "unite",
        "army_name":"borgo",
        "id_tile":"borgo-boucher1",
            "initiative": [3],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":[(-1, 0, +1), (-1,1,0)],
            "cac_attacks_power":[1, 1],
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":None,
            "url_image":"image/armies/borgo-boucher.png"},
        {"kind": "unite",
            "army_name":"borgo",
            "id_tile":"borgo-boucher2",
            "initiative": [3],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":[(-1, 0, +1), (-1,1,0)],
            "cac_attacks_power":[1, 1],
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":None,
            "url_image":"image/armies/borgo-boucher.png"},
        {"kind": "unite",
            "army_name":"borgo",
            "id_tile":"borgo-boucher3",
            "initiative": [3],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":[(-1, 0, +1), (-1,1,0)],
            "cac_attacks_power":[1, 1],
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":None,
            "url_image":"image/armies/borgo-boucher.png"},
        {"kind": "unite",
        "army_name":"borgo",
        "id_tile":"borgo-boucher4",
            "initiative": [3],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":[(-1, 0, +1), (-1,1,0)],
            "cac_attacks_power":[1, 1],
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":None,
            "url_image":"image/armies/borgo-boucher.png"},
        {"kind": "unite",
        "army_name":"borgo",
        "id_tile":"borgo-supermutant",
            "initiative": [2],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":[(-1, 0, 1),(0, -1, +1), (1, -1, 0)],
            "cac_attacks_power":[1, 2, 1],
            "net_directions":None,
            "life_point":2,
            "shields_directions":[(-1, 0, 1),(0, -1, +1), (1, -1, 0)],
            "special_capacities":[],
            "module":None,
            "action":None,
            "url_image":"image/armies/borgo-supermutant.png"},
        {"kind": "unite",
            "army_name":"borgo",
            "id_tile":"borgo-assassin1",
            "initiative": [3],
            "range_attacks_direction":[(-1, 0, 1)],
            "range_attacks_power":[1],
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":['movement'],
            "module":None,
            "action":None,
            "url_image":"image/armies/borgo-assassin.png"},
        {"kind": "unite",
            "army_name":"borgo",
            "id_tile":"borgo-assassin2",
            "initiative": [3],
            "range_attacks_direction":[(-1, 0, 1)],
            "range_attacks_power":[1],
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":['movement'],
            "module":None,
            "action":None,
            "url_image":"image/armies/borgo-assassin.png"},
        {"kind": "module",
            "army_name":"borgo",
            "id_tile":"borgo-medecin",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":[{"medic":[(-1, 0, 1),(0, -1, +1), (1, -1, 0)]}],
            "action":None,
            "url_image":"image/armies/borgo-medecin.png"},
        {"kind": "module",
            "army_name":"borgo",
            "id_tile":"borgo-officiersuperieur",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":2,
            "shields_directions":None,
            "special_capacities":[],
            "module":[{"cac_augment":[(-1, 0, 1),(0, -1, +1), (1, -1, 0)]}],
            "action":None,
            "url_image":"image/armies/borgo-officiersuperieur.png"},
        {"kind": "module",
            "army_name":"borgo",
            "id_tile":"borgo-officier1",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":[{"cac_augment":[(-1, 0, 1),(0, -1, +1), (1, -1, 0)]}],
            "action":None,
            "url_image":"image/armies/borgo-officier.png"},
        {"kind": "module",
            "army_name":"borgo",
            "id_tile":"borgo-officier2",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":[{"cac_augment":[(-1, 0, 1),(0, -1, +1), (1, -1, 0)]}],
            "action":None,
            "url_image":"image/armies/borgo-officier.png"},
        {"kind": "module",
            "army_name":"borgo",
            "id_tile":"borgo-eclaireur1",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":[{"initiative_augment":[(-1, 0, 1),(0, -1, +1), (1, -1, 0)]}],
            "action":None,
            "url_image":"image/armies/borgo-eclaireur.png"},
        {"kind": "module",
            "army_name":"borgo",
            "id_tile":"borgo-eclaireur2",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":[{"initiative_augment":[(-1, 0, 1),(0, -1, +1), (1, -1, 0)]}],
            "action":None,
            "url_image":"image/armies/borgo-eclaireur.png"},
        {"kind": "action",
            "army_name":"borgo",
            "id_tile":"borgo-battle1",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":None,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":"battle",
            "url_image":"image/armies/borgo-battle.png"},
        {"kind": "action",
            "army_name":"borgo",
            "id_tile":"borgo-battle2",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":"battle",
            "url_image":"image/armies/borgo-battle.png"},
        {"kind": "action",
            "army_name":"borgo",
            "id_tile":"borgo-battle3",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":"battle",
            "url_image":"image/armies/borgo-battle.png"},
        {"kind": "action",
            "army_name":"borgo",
            "id_tile":"borgo-battle4",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":"battle",
            "url_image":"image/armies/borgo-battle.png"},
        {"kind": "action",
            "army_name":"borgo",
            "id_tile":"borgo-battle5",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":"battle",
            "url_image":"image/armies/borgo-battle.png"},
        {"kind": "action",
            "army_name":"borgo",
            "id_tile":"borgo-battle6",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":"battle",
            "url_image":"image/armies/borgo-battle.png"},
        {"kind": "action",
            "army_name":"borgo",
            "id_tile":"borgo-grenade",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":"grenade",
            "url_image":"image/armies/borgo-grenade.png"},
        {"kind": "action",
        "army_name":"borgo",
        "id_tile":"borgo-mouvement1",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":"movement",
            "url_image":"image/armies/borgo-mouvement.png"},
        {"kind": "action",
        "army_name":"borgo",
        "id_tile":"borgo-mouvement2",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":"movement",
            "url_image":"image/armies/borgo-mouvement.png"},
        {"kind": "action",
        "army_name":"borgo",
        "id_tile":"borgo-mouvement3",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":"movement",
            "url_image":"image/armies/borgo-mouvement.png"},
        {"kind": "action",
        "army_name":"borgo",
        "id_tile":"borgo-mouvement4",
            "initiative": None,
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":None,
            "cac_attacks_power":None,
            "net_directions":None,
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":"movement",
            "url_image":"image/armies/borgo-mouvement.png"},
        {"kind": "unite",
        "army_name":"borgo",
        "id_tile":"borgo-retiaire1",
            "initiative": [1],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":[(1, 0, -1)],
            "cac_attacks_power":[1],
            "net_directions":[(1, 0, -1)],
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":None,
            "url_image":"image/armies/borgo-retiaire.png"},
        {"kind": "unite",
        "army_name":"borgo",
        "id_tile":"borgo-retiaire2",
            "initiative": [1],
            "range_attacks_direction":None,
            "range_attacks_power":None,
            "cac_attacks_direction":[(1, 0, -1)],
            "cac_attacks_power":[1],
            "net_directions":[(1, 0, -1)],
            "life_point":1,
            "shields_directions":None,
            "special_capacities":[],
            "module":None,
            "action":None,
            "url_image":"image/armies/borgo-retiaire.png"}]

def test():
    return borgo

if __name__ == "__main__":
    print(sys.path)
