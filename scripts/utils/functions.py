from typing import Tuple, List, TypeVar

from scripts.utils.config import (BOARD_PIXEL_TO_CUBE,
                        CUBE_DIRECTION_VECTORS,
                        DISPLAY_SIZE,
                        BOARD_LIMIT
                    )


def coordinates_cube_to_pixel(cube_coordinate: Tuple[int, int, int]
                            ) -> Tuple[int, int]:
    """
    Transforms cube coordinates into a pixel position.

    Args:
        cube_coordinates (Tuple[int, int, int]): Cube coordinates.

    Returns:
        pixel_position (Tuple[int, int]): Corresponding pixel position.

    Raises:
        KeyError:   If the cube coordinates do not 
                    match any pixel position.
    """
    # Validate input types and lengths
    raise_wrong_cube_coordinate(cube_coordinate)
    for pixel_position, cube_coord in BOARD_PIXEL_TO_CUBE.items():
        if cube_coord == cube_coordinate:
            return pixel_position
    raise KeyError("Invalid cube coordinates")


def coordinates_pixel_to_cube(pixel_position: Tuple[int, int]
                            ) -> Tuple[int, int, int]:
    """Transform pixels position into cube coordinates 

    Args:
        pixel_position (Tuple[int, int]): pixel position

    Returns:
        cube_position (Tuple[int, int, int]): Cube coordinates
    Raises:
        KeyError:   If the pixel coordinates do not match 
                    any cube position.
    """
    try:
        # Validate input types and lengths
        raise_wrong_pixel_coordinate(pixel_position)
        return BOARD_PIXEL_TO_CUBE[pixel_position]
    except KeyError:
        raise KeyError("Invalid pixel position")

T = TypeVar('T')
def next_element(elements: List[T], element: T):
    """
    return the next element of a list. 
    Restart from the begining if the iterator is exhausted

    Args:
        elements (List[T]): list of elements
        element (T): The element to start from.
    Returns:
        T:  The next element in the list, 
            or the first element if the given one is the last.
    """
    try: 
        idx = elements.index(element)
        return elements[0] if idx >= len(elements) - 1 else elements[idx + 1]
    except ValueError:
        raise ValueError(f"{element} not found in the list.")


def get_neighbors_hex_positions(cube_coordinates: Tuple[int, int, int]
                            ) -> List[Tuple[int, int, int]]:
    """
    Calculate the neighboring cube coordinates for a given position.

    Args:
        cube_coordinates (Tuple[int, int, int]):
            The initial cube coordinate.

    Returns:
        List[Tuple[int, int, int]]:
            List of neighboring cube coordinates.
    """
    try: 
        # Validate input types and lengths
        raise_wrong_cube_coordinate(cube_coordinates)
        # Not doing a loop because of pylint which is returning a
        # ReturnTypeError if so.
        neighbors = [(
                cube_coordinates[0] + direction[0],
                cube_coordinates[1] + direction[1],
                cube_coordinates[2] + direction[2]
            )
            for direction in CUBE_DIRECTION_VECTORS
        ]
        return neighbors
    except ValueError as ve:
        print(f"Error: {ve}")
        raise


def list_cubes_to_pixel(list_cube_coordinates: List[Tuple[int, int, int]]
                    ) -> List[Tuple[int, int]]:
    """Transforms a list of cube coordinates into a list of  pixel
    positions.

    Args:
        list_cube_coordinates (List[Tuple[int, int, int]]): 
            List of cube coordinates

    Raises:
        KeyError: If pixel position not valide

    Returns:
        List[Tuple[int, int]]:  List of pixel coordinates
    """
    try:
        # Validate input types and lengths
        [raise_wrong_cube_coordinate(x) for x in list_cube_coordinates]
        list_pixels_coordinates = [coordinates_cube_to_pixel(x)
            for x in list_cube_coordinates 
            if x in list(BOARD_PIXEL_TO_CUBE.values())
        ]
        return list_pixels_coordinates
    except KeyError:
        raise KeyError("Invalid cube position")


def calculate_position(start_position: Tuple[int, int, int],
                    direction: Tuple[int, int, int]
                    ) -> Tuple[int, int, int]:
    """
    Calculates the new position on a hexagonal grid by applying a
    directional offset.

    Args:
        start_position (Tuple[int, int, int]):
            The starting position in cube coordinates.
        direction (Tuple[int, int, int]):
            The directional vector in cube coordinates.

    Returns:
        new_position (Tuple[int, int, int]):
            The resulting position after adding the direction to the
            start position.
    """
    try:
        # Validate input types and lengths
        raise_wrong_cube_coordinate(start_position)
        raise_wrong_cube_coordinate(direction)
        # Not doing a loop because of pylint which is returning a
        # ReturnTypeError if so.
        return (start_position[0] + direction[0],
                start_position[1] + direction[1],
                start_position[2] + direction[2])

    except ValueError as ve:
        print(f"Error: {ve}")
        raise

def raise_wrong_cube_coordinate(cube_coordinate: Tuple[int, int, int],
                                board_limit= BOARD_LIMIT
                        ) -> None:
    """Validates a cube coordinate in a hexagonal
        grid system and raises a ValueError if invalid.

    Args:
        cube_coordinate (Tuple[int, int, int]): The cube coordinate
                                                to validate.

    Raises:
        ValueError: 
            Not a tuple.
        ValueError:
            Does not contain exactly three elements.
        ValueError:
            Contains non-integer elements
        ValueError:
            The sum of the three elements is not zero.
        ValueError:
            The position is outside the board according to the
            Value BOARD_LIMIT
    """

    if not isinstance(cube_coordinate, tuple):
        raise ValueError("Both start_position and direction must \
                    be tuples.")
    
    if not len(cube_coordinate) == 3:
        raise ValueError("Both start_position and direction must have \
                    exactly three elements.")
    
    if not all(isinstance(x, int) for x in cube_coordinate):
        raise ValueError("All elements in start_position and direction \
                    must be integers.")

    if not sum(cube_coordinate) == 0:
        raise ValueError("The sum of the three coordinates is not \
                    equal to 0.")

    if not all(abs(x) < board_limit for x in cube_coordinate):
        raise ValueError(f"The position {cube_coordinate} is outside \
                    of the board")

def raise_wrong_pixel_coordinate(pixel_coordinate: Tuple[int, int]
                        ) -> None:
    """Validates a pixel coordinate and raises a ValueError if invalid.

    Args:
        pixel_coordinate (Tuple[int, int, int]): The pixel coordinate
                                                to validate.

    Raises:
        ValueError: Not a tuple.
        ValueError: Does not contain exactly two elements.
        ValueError: Contains non-integer elements
        ValueError: Does not oversize the sreen
    """
    if not isinstance(pixel_coordinate, tuple):
        raise ValueError("Both start_position and direction must \
                    be tuples.")
    
    if not len(pixel_coordinate) == 2:
        raise ValueError("Both start_position and direction must have \
                    exactly two elements.")
    
    if not all(isinstance(x, int) for x in pixel_coordinate):
        raise ValueError("All elements in start_position and direction \
                    must be integers.")

    if not all(pixel_coordinate[i] <= DISPLAY_SIZE[i] for i in range(2)):
        raise ValueError("The pixel position must not exceed \
                        the display size.")
