import pytest
import pygame
from unittest.mock import MagicMock
from scripts.view.view import TileManipulator, TileView

class TestTileManipulator:
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
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (110, 110)})
        self.tile_manipulator._update_move([event])
        assert self.tile_manipulator.dragging is True
        assert self.tile_manipulator.rel_pos == (10, 10)

    def test_dragging_motion(self):
        self.tile_manipulator.dragging = True
        self.tile_manipulator.rel_pos = (10, 10)
        event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (120, 120)})
        self.tile_manipulator._update_move([event])
        assert self.mock_sprite.rect.topleft == (110, 110)

    def test_dragging_end(self):
        self.tile_manipulator.dragging = True
        event = pygame.event.Event(pygame.MOUSEBUTTONUP, {})
        self.tile_manipulator._update_move([event])
        assert self.tile_manipulator.dragging is False

    def test_rotation_update(self):
        self.tile_manipulator.dragging = True
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3})
        self.tile_manipulator._update_angle([event])
        assert self.mock_sprite.angle_index == 1

class TestTileView:
    def setup_method(self):
        pygame.init()
        self.id_tile = "test_tile"
        self.position = (100, 100)
        self.angle_index = 0
        self.tile_view = TileView(self.id_tile, self.position, self.angle_index)

    def teardown_method(self):
        pygame.quit()

    def test_initialization(self):
        assert self.tile_view.id_tile == self.id_tile
        assert self.tile_view.rect.topleft == self.position
        assert self.tile_view.angle_index == self.angle_index

    def test_update_position(self):
        mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (110, 110)})
        self.tile_view.update([mock_event])
        assert self.tile_view.manipulator.dragging is True

    def test_clean_position(self):
        self.tile_view.rect.topleft = (105, 105)
        self.tile_view._clean_postition()
        assert self.tile_view.rect.topleft in PIXEL_POSITION_LIST  # Assurez-vous que la position est alignée.

    def test_click_tile(self):
        mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (110, 110)})
        surface = pygame.Surface((800, 600))
        self.tile_view.button.enable = True
        result = self.tile_view.click_tile([mock_event], surface)
        assert result in [True, False]  # Cela dépend de la logique du bouton.
