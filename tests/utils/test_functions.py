import pytest

import scripts.utils.functions as functions
import scripts.utils.config as config

### tests coordinates_cube_to_pixel() ###

@pytest.mark.parametrize("cube_position, expected_pixel_position",[
                        ((0,0,0),(451, 327)),
                        ((0, 2, -2),(450, 499)),
                        ((2, 0, -2),(598, 413))
                        ])
def test_coordinates_cube_to_pixel(cube_position, expected_pixel_position):
    result = functions.coordinates_cube_to_pixel(cube_position)
    assert result == expected_pixel_position

def test_coordinates_cube_to_pixel_wrong_type_entry():
    with pytest.raises(ValueError):
        functions.coordinates_cube_to_pixel((1,1))

def test_coordinates_cube_to_pixel_wrong_value_entry():
    with pytest.raises(ValueError):
        functions.coordinates_cube_to_pixel((1,1,1))

def test_coordinates_cube_to_pixel_non_existant_entry():
    with pytest.raises(KeyError):
        #Delete a entry of BOARD_PIXEL_TO_CUBE dict
        with pytest.MonkeyPatch.context() as m:
            m.delitem(config.BOARD_PIXEL_TO_CUBE, (302, 241))
            functions.coordinates_cube_to_pixel((-2, 0, 2))


### tests coordinates_pixel_to_cube() ###

def test_coordinates_pixel_to_cube():
    result = functions.coordinates_pixel_to_cube((525, 284))
    assert result == (1, -1, 0)

def test_coordinates_pixel_to_cube_wrong_type_entry():
    with pytest.raises(ValueError):
        functions.coordinates_pixel_to_cube((250,300, 400))

def test_coordinates_pixel_to_cube_wrong_value_entry():
    with pytest.raises(KeyError):
        functions.coordinates_pixel_to_cube((500,600))


### tests list_pixel_to_cube() ###

def test_list_pixel_to_cube():
    result = functions.list_pixel_to_cube([(302,241),(301,326),(301,411)])
    assert result == [(-2, 0, 2),(-2, 1, 1),(-2, 2, 0)]

def test_list_pixel_to_cube_wrong_type():
    with pytest.raises(TypeError):
        functions.list_pixel_to_cube((302,241))


### tests list_cubes_to_pixel() ###

def test_list_cubes_to_pixel():
    result = functions.list_cubes_to_pixel([(-2, 0, 2),(-2, 1, 1),(-2, 2, 0)])
    assert result == [(302,241),(301,326),(301,411)]

def test_list_cubes_to_pixel_wrong_type():
    with pytest.raises(TypeError):
        functions.list_cubes_to_pixel((-2, 0, 2))


### tests next_element() ###

@pytest.mark.parametrize("list_elements, entry, expected_result",[
                                                (["a","b","c","d"],"d","a"),
                                                ([1,2,3,4],2,3)
                                            ]) 
def test_next_element(list_elements, entry, expected_result):
    result = functions.next_element(list_elements,entry)
    assert result == expected_result

def test_next_element_wrong_entry():
    with pytest.raises(ValueError):
        functions.next_element([1,2,3], "a")

### tests get_neighbors_hex_positions() ###

@pytest.mark.parametrize("position, expected_result", [
    ((-2,2,0), [(-2,1,1), (-1,1,0), (-1,2,-1)]),
    ((0,0,0), [(-1,0,1), (-1, 1, 0), (0,-1,1),(0,1,-1), (1,-1,0), (1,0,-1)])
])
def test_get_neighbors_hex_positions(position,expected_result):
    result = functions.get_neighbors_hex_positions(position)
    assert set(result) == set(expected_result)

### test calculate_position() ###

@pytest.mark.parametrize("start_position, direction, expected_result", [
                                ((0,0,0), (1,0,-1),(1,0,-1)),
                                ((2,0,-2), (0,-1,1), (2,-1,-1))
                            ])
def test_calculate_position(start_position, direction, expected_result):
    result = functions.calculate_position(start_position, direction)
    assert result == expected_result


### tests raise_wrong_cube_coordinate() ###

@pytest.mark.parametrize("coordinates", [
        ([1,1,1]), ((1,-1)), (("a",1, 0)), ((-1,1,1)), ((3,-2,-1))])
def test_raise_wrong_cube_coordinate(coordinates):
    with pytest.raises(ValueError):
        functions.raise_wrong_cube_coordinate(coordinates)

def test_raise_wrong_cube_coordinate_no_raise():
    functions.raise_wrong_cube_coordinate((0,0,0))

### tests raise_wrong_pixel_coordinate() ###

@pytest.mark.parametrize("coordinates", [
    ([10,10], ((300,300,300)), (("a")), ((2000,2000)))
])
def test_raise_wrong_pixel_coordinate(coordinates):
    with pytest.raises(ValueError):
        functions.raise_wrong_pixel_coordinate(coordinates)

def test_raise_wrong_pixel_coordinate_no_raise():
    functions.raise_wrong_pixel_coordinate((250,250))