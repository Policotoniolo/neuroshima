import pytest
import pygame
from unittest.mock import MagicMock
import unittest.mock as mock

from scripts.view.view import TileManipulator, TileView

class TestTileManipulator():
    def setup_method(self):
        pygame.init()
        self.mock_sprite = MagicMock()
        self.mock_sprite.rect = pygame.Rect(100, 100, 50, 50)
        self.mock_sprite.angle_index = 0
        self.mock_sprite.url_image = "path/to/image.png"
        self.tile_manipulator = TileManipulator(self.mock_sprite)

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

    @mock.patch.object(TileManipulator, "_preload_rotated_image")
    def test_rotation_update(self, mock_preload_rotated_image):
        mock_preload_rotated_image.return_value = pygame.surface.Surface((0,50))
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

@pytest.fixture(autouse=True)
def mock_pygame_load():
    with mock.patch('scripts.view.view.pygame.image.load', return_value=pygame.Surface((200, 173))) as mocked_image_load:
        yield mocked_image_load

class TestTileView:
    def setup_method(self, method):
        print(f"Setting up {method}")
        pygame.init()
        self.id_tile = "test_tile"
        self.position = (100, 100)
        self.angle_index = 0
        self.tile_view = TileView(self.id_tile, self.position, self.angle_index)

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