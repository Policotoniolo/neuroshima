"""docstring
"""
import pygame

from typing import Literal

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
12:[(450,499), (0,2,-2)],
13:[(525,199), (1,-2,1)],
14:[(525,284), (1,-1,0)],
15:[(525,370), (1,0,-1)],
16:[(524,455), (1,1,-2)],
17:[(599,242), (2,-2,0)],
18:[(598,328), (2,-1,-1)],
19:[(598,413), (2,0,-2)]}


def coordinates_cube_to_pixel(cube_coordinates:tuple):
    """Transform cube coordinates into pixel position

    Args:
        cube_coordinates (tuple): cube coordinates

    Returns:
        Tuple: Pixels posistion
    """
    try:
        return [k for k, v in BOARD_PIXEL_TO_CUBE.items() if v == cube_coordinates]
    except ValueError:
        print("cube coordinates not good!")


def coordinates_pixel_to_cube(pixel_position:tuple):
    """Transform pixels position into cube coordinates 

    Args:
        pixel_position (tuple): pixel position

    Returns:
        Tuple: Cube coordinates
    """
    try:
        return BOARD_PIXEL_TO_CUBE[pixel_position]
    except ValueError:
        print("pixel position not good!")
