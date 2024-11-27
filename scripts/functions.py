from typing import Tuple, List, TypeVar

from scripts.config import BOARD_PIXEL_TO_CUBE, CUBE_DIRECTION_VECTORS


def coordinates_cube_to_pixel(cube_coordinates: Tuple[int, int, int]
                            ) -> Tuple[int, int]:
    """
    Transforms cube coordinates into a pixel position.

    Args:
        cube_coordinates (Tuple[int, int, int]): Cube coordinates.

    Returns:
        Tuple[int, int]: Corresponding pixel position.

    Raises:
        KeyError: If the cube coordinates do not match any pixel position.
    """
    for pixel_position, cube_coord in BOARD_PIXEL_TO_CUBE.items():
        if cube_coord == cube_coordinates:
            return pixel_position
    raise KeyError("Invalid cube coordinates")



def coordinates_pixel_to_cube(pixel_position:tuple) -> tuple:
    """Transform pixels position into cube coordinates 

    Args:
        pixel_position (tuple): pixel position

    Returns:
        Tuple: Cube coordinates
    """
    try:
        return BOARD_PIXEL_TO_CUBE[pixel_position]
    except KeyError:
        print("pixel position not good!")
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

def list_cubes_to_pixel(list_cube_coordinates: List[tuple]) -> List[Tuple[int, int]]|None:
    list_pixels_coordinates = [coordinates_cube_to_pixel(x) for x in list_cube_coordinates if x in list(BOARD_PIXEL_TO_CUBE.values())]
    return list_pixels_coordinates

def calculate_position( start_position: Tuple[int, int, int],
                        direction: Tuple[int, int, int]
                        ) -> Tuple[int, int, int]:
    """
    Calculates the new position on a hexagonal grid by applying a directional offset.

    Args:
        start_position (Tuple[int, int, int]): The starting position in cube coordinates.
        direction (Tuple[int, int, int]): The directional vector in cube coordinates.

    Returns:
        Tuple[int, int, int]: The resulting position after adding the direction to the start position.
    """
    return tuple(
        map(sum, zip(start_position, direction))
    )  # type: ignore
