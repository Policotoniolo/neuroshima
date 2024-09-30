"""docstring
"""
import pygame
from typing import List

# pylint: disable = no-member
# pylint: disable=c-extension-no-member


#Board view variables
BOARD_PIXEL_TO_CUBE = {(302,241): (-2,0,2),
                (301,326): (-2,1,1),
                (301,411): (-2,2,0),
                (377,198): (-1,-1,0),
                (376,284): (-1,0,-1),
                (376,369): (-1,1,0),
                (376,455): (-1,2,-1,),
                (451,155): (0,-2,2),
                (451,241): (0,-1,1),
                (451,327): (0,0,0),
                (450,413): (0,1,-1),
                (450,499): (0,2,-2),
                (525,199): (1,-2,1),
                (525,284): (1,-1,0),
                (525,370): (1,0,-1),
                (524,455): (1,1,-2),
                (599,242): (2,-2,0),
                (598,328): (2,-1,-1),
                (598,413): (2,0,-2)
                }
BOARD_POSITION = {1:[(302,241), (-2,0,2)],
2:[(301,326), (-2,1,1)],
3:[(301,411), (-2,2,0)],
4:[(377,198), (-1,-1,0)],
5:[(376,284), (-1,0,-1)],
6:[(376,369), (-1,1,0)],
7:[(376,455), (-1,2,-1,)],
8:[(451,155), (0,-2,2)],
9:[(451,241), (0,-1,1)],
10:[(451,327), (0,0,0)],
11:[(450,413), (0,1,-1)],
12:[(450,499), (0,2,-1)],
13:[(525,199), (1,-2,1)],
14:[(525,284), (1,-1,0)],
15:[(525,370), (1,0,-1)],
16:[(524,455), (1,1,-2)],
17:[(599,242), (2,-2,0)],
18:[(598,328), (2,-1,1)],
19:[(598,413), (2,0,-2)]}

CUBE_DIRECTION_VECTORS =  [
    (+1, 0, -1), (+1, -1, 0), (0, -1, +1), 
    (-1, 0, +1), (-1, +1, 0), (0, +1, -1), 
] #Used for finding neighbors

def coordinates_cube_to_pixel(cube_coordinates:tuple) -> tuple:
    """Transform cube coordinates into pixel position

    Args:
        cube_coordinates (tuple): cube coordinates

    Returns:
        Tuple: Pixels posistion
    """
    return [k for k, v in BOARD_PIXEL_TO_CUBE.items() if v == cube_coordinates][0]


def coordinates_pixel_to_cube(pixel_position:tuple) -> tuple:
    """Transform pixels position into cube coordinates 

    Args:
        pixel_position (tuple): pixel position

    Returns:
        Tuple: Cube coordinates
    """
    return BOARD_PIXEL_TO_CUBE[pixel_position]

def next_element(list, element):
    """return the next element of a list. 
    Restart from the begining if the iterator is exhausted

    Args:
        list (List): list of elements
        element (Objct): Start element
    """
    idx = list.index(element)
    if idx >= len(list)-1:
        return list[0]
    return list[idx+1]

def get_neighbors(cube_coordinates: tuple) -> list:
    """get all neighbors of a cube coordinates position

    Args:
        cube_coordinates (tuple): initale ube coordinate to looking for

    Returns:
        list: List of cube coordinates neighbors
    """
    neighbors = [tuple(map(sum, zip(x, cube_coordinates)))
                    for x in CUBE_DIRECTION_VECTORS]
    return neighbors

def list_cubes_to_pixel(list_cube_coordinates: List[tuple]) -> List[tuple]:
    list_pixels_coordinates = [coordinates_cube_to_pixel(x) for x in list_cube_coordinates]
    return list_pixels_coordinates
