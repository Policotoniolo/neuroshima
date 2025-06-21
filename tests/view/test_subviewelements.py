import pytest
import pygame
import unittest
from unittest.mock import MagicMock
import unittest.mock as mock
import math

import scripts.view.view as view

# Mocking pygame.image.load with a surface of the size of a
# tile (200, 173) for all the tests in this file.
@pytest.fixture(autouse=True)
def mock_pygame_load():
    with mock.patch('scripts.view.view.pygame.image.load',
            return_value=pygame.Surface((200, 173))) as mocked_image_load:
        yield mocked_image_load

class TestTileManipulator():
    def setup_method(self):
        pygame.init()
        self.mock_sprite = MagicMock()
        self.mock_sprite.rect = pygame.Rect(100, 100, 50, 50)
        self.mock_sprite.angle_index = 0
        self.mock_sprite.url_image = "path/to/image.png"
        self.tile_manipulator = view.TileManipulator(self.mock_sprite)

    def teardown_method(self):
        pygame.quit()
        del self.mock_sprite
        del self.tile_manipulator

    def test_dragging_start(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (110, 110), "button": 1})
        self.tile_manipulator.update([event])
        assert self.tile_manipulator.dragging is True
        assert self.tile_manipulator.rel_pos == (10, 10)

    def test_dragging_motion(self):
        self.tile_manipulator.dragging = True
        self.tile_manipulator.rel_pos = (10, 10)
        event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (120, 120)})
        self.tile_manipulator.update([event])
        assert self.mock_sprite.rect.topleft == (110, 110)

    def test_dragging_end(self):
        self.tile_manipulator.dragging = True
        event = pygame.event.Event(pygame.MOUSEBUTTONUP, {})
        self.tile_manipulator.update([event])
        assert self.tile_manipulator.dragging is False

    def test_rotation_update(self):
        self.tile_manipulator.dragging = True
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (110, 110), "button": 3})
        self.tile_manipulator.update([event])
        assert self.mock_sprite.angle_index == 1

    @mock.patch("scripts.view.view.pygame.transform.smoothscale")
    @mock.patch('scripts.view.view.pygame.transform.rotate')
    @mock.patch('scripts.view.view.pygame.image.load')
    def test_preload_rotated_image(self, mock_load, mock_rotate, mock_smoothscale):
        """Test la méthode _preload_rotated_image."""
        # Mock des étapes de transformation
        mock_surface = pygame.Surface((300, 300))
        mock_load.return_value = mock_surface
        mock_rotate.return_value = mock_surface
        mock_smoothscale.return_value = pygame.Surface((81, 70))

        # call method and force if condition
        self.tile_manipulator.sprite.angle_index = 1
        result = self.tile_manipulator._preload_rotated_image()

        # Assertions
        mock_load.assert_called_once_with("path/to/image.png")
        mock_rotate.assert_called_once_with(mock_surface, -60)
        
        args, _ = mock_smoothscale.call_args
        assert isinstance(args[0], pygame.Surface)
        assert args[0].get_size() == (200, 173)
        assert args[1] == (81, 70)

        # test of subsurface. This method cannot be mock (immutable type)
        subsurface_area = mock_surface.subsurface((25, 42,200,173)).get_size()
        assert subsurface_area == (200, 173)
        # Test result
        assert isinstance(result, pygame.Surface)
        assert result.get_size() == (81, 70)


class TestTileView:
    def setup_method(self, method):
        print(f"Setting up {method}")
        pygame.init()
        self.id_tile = "test_tile"
        self.position = (100, 100)
        self.angle_index = 0
        self.tile_view = view.TileView(self.id_tile, self.position, self.angle_index)

    def teardown_method(self, method):
        print(f"Tearing down{method}")
        del self.tile_view
        del self.id_tile
        del self.position
        del self.angle_index
        pygame.quit()

    def test_initialization(self):
        assert self.tile_view.id_tile == self.id_tile
        assert self.tile_view.rect.topleft == self.position
        assert self.tile_view.angle_index == self.angle_index

    def test_update_position(self):
        mock_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": (110, 110), "button": 1}
        )
        self.tile_view.update([mock_event])
        assert self.tile_view.manipulator.dragging is True
        assert self.tile_view.angle_index == 0

    def test_update_angle(self):
        mock_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": (110, 110), "button": 3}
        )
        self.tile_view.update([mock_event])
        assert self.tile_view.manipulator.dragging is True
        assert self.tile_view.angle_index == 1

    def test_clean_position(self):
        self.tile_view.rect.topleft = (440, 405)
        self.tile_view._clean_postition()
        assert self.tile_view.rect.topleft == (450, 413)  # Assurez-vous que la position est alignée.

    def test_click_tile(self):
        mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (110, 110)})
        surface = pygame.Surface((800, 600))
        self.tile_view.button.enable = True
        result = self.tile_view.click_tile([mock_event], surface)
        assert result in [True, False]


class TestHexagone(unittest.TestCase):
    def setup_method(self, method):
        print(f"Setting up {method}")
        pygame.init()
        self.position = (450, 413)
        self.radius = 50
        self.hexagone = view.Hexagone(self.position)

    def teardown_method(self, method):
        print(f"Tearing down{method}")
        del self.hexagone
        del self.radius
        del self.position
        pygame.quit()

    def test_initialization(self):
        """
        Test the initialization of the Hexagone class.
        """
        self.assertEqual(self.hexagone.position, self.position)
        self.assertEqual(self.hexagone.radius, self.radius)
        self.assertIsInstance(self.hexagone.image, pygame.Surface)
        self.assertIsInstance(self.hexagone.rect, pygame.Rect)
        self.assertEqual(self.hexagone.rect.topleft,
                        (self.position[0]+15, self.position[1]+10))

    def test_compite_vertice(self):
        excepted_result = 42*math.cos(math.radians(30))
        self.assertEqual(self.hexagone._minimal_radius(),
                        excepted_result)

    def test_compute_vertice(self):
        x,y = self.position[0]+19, self.position[1]
        minimal_radius = 42*math.cos(math.radians(30))
        half_radius = 42/2
        excepted_result = [
            (x, y),
            (x - half_radius, y + minimal_radius),
            (x, y + 2 * minimal_radius),
            (x + 42, y + 2 * minimal_radius),
            (x + 3 * half_radius, y + minimal_radius),
            (x + 42, y),
        ]
        self.assertEqual(self.hexagone.vertices,excepted_result)

    @mock.patch('scripts.view.view.pygame.draw.polygon')
    def test_render(self, mock_draw_polygon):
        surface = pygame.Surface((800, 600))
        self.hexagone.render(surface, (0, 0, 0, 0), (1,1,1,1), 5)
        calls = [mock.call(surface, (0, 0, 0, 0), self.hexagone.vertices),
                mock.call(surface, (1, 1, 1, 1), self.hexagone.vertices, 5)]
        mock_draw_polygon.assert_has_calls(calls, any_order=False)

    def test_click_button_non_success(self):
        position_ouside_button = (0, 0)
        mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": position_ouside_button, 
                                                                "button": 1})
        surface = pygame.Surface((800, 600))
        result = self.hexagone.click_button([mock_event], surface)
        self.assertFalse(result)

    def test_click_button_success(self):
        position_inside_button = self.hexagone.button.rect.center
        mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": position_inside_button, 
                                                                "button": 1})
        surface = pygame.Surface((800, 600))
        result = self.hexagone.click_button([mock_event], surface)
        self.assertTrue(result)

    def test_attacks_cac_click_button_success(self):
        position_inside_button = self.hexagone.cac_attacks_button.rect.center
        mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": position_inside_button, 
                                                                "button": 1})
        surface = pygame.Surface((800, 600))
        result = self.hexagone.attacks_cac_click_button([mock_event], surface)
        self.assertTrue(result)

    def test_attacks_cac_click_button_non_success(self):
        position_ouside_button = (0, 0)
        mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": position_ouside_button, 
                                                                "button": 1})
        surface = pygame.Surface((800, 600))
        result = self.hexagone.attacks_cac_click_button([mock_event], surface)
        self.assertFalse(result)

    def test_range_attacks_click_button_success(self):
        position_inside_button = self.hexagone.range_attacks_button.rect.center
        mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": position_inside_button, 
                                                                "button": 1})
        surface = pygame.Surface((800, 600))
        result = self.hexagone.attacks_range_click_button([mock_event], surface)
        self.assertTrue(result)

    def test_range_attacks_click_button_non_success(self):
        position_ouside_button = (0, 0)
        mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": position_ouside_button, 
                                                                "button": 1})
        surface = pygame.Surface((800, 600))
        result = self.hexagone.attacks_range_click_button([mock_event], surface)
        self.assertFalse(result)


class TestEndButton(unittest.TestCase):
    def setup_method(self, method):
        print(f"Setting up {method}")
        pygame.init()
        self.surface = pygame.Surface((800, 600))
        self.end_button = view.EndButton(self.surface)

    def teardown_method(self, method):
        print(f"Tearing down{method}")
        del self.end_button
        del self.surface
        pygame.quit()

    def test_initialization(self):
        self.assertIsInstance(self.end_button.image, pygame.Surface)
        self.assertIsInstance(self.end_button.rect, pygame.Rect)
        self.assertIsInstance(self.end_button.surface, pygame.Surface)

    def test_isvalidated_non_success(self):
        position_ouside_button = (0, 0)
        mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": position_ouside_button, 
                                                                "button": 1})
        surface = pygame.Surface((800, 600))
        result = self.end_button.isvalidated([mock_event])
        self.assertFalse(result)

    def test_isvalidated_success(self):
        position_inside_button = self.end_button.rect.center
        mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": position_inside_button, 
                                                                "button": 1})
        surface = pygame.Surface((800, 600))
        result = self.end_button.isvalidated([mock_event])
        self.assertTrue(result)

    def test_render(self):
        self.end_button.render()



######## exemple de fonction de test ########

    @mock.patch('scripts.view.view.pygame.Surface')
    def test_draw_board(self, mock_surface):
        mock_surface.blit.return_value = None
        mock_surface.subsurface.return_value = mock_surface
        mock_surface.get_size.return_value = (200, 173)

        res = mock_surface.blit()
        assert res is None
