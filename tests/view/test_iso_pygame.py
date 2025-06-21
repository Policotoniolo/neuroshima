import pytest
import unittest.mock as mock
from unittest.mock import MagicMock



# Mock the entire pygame module
@pytest.fixture(autouse=True)
def pygame_mock():
    pygame_mock = mock.Mock()

    # Mocking Surface
    mock_surface = MagicMock()
    mock_surface.get_size.return_value = (200, 173)
    mock_surface.subsurface.return_value = mock_surface
    pygame_mock.Surface = MagicMock(return_value=mock_surface)

    # Properly mocking Rect
    def mock_rect(x, y, width, height):
        rect = MagicMock()
        rect.topleft = (x, y)
        rect.width = width
        rect.height = height
        rect.get_size.return_value = (width, height)
        # Mocking __contains__ for rectangle containment checks
        rect.__contains__.side_effect = lambda pos: (x <= pos[0] <= x + width) and (y <= pos[1] <= y + height)
        return rect

    pygame_mock.Rect = mock_rect  # Define Rect as a callable function

    # Mocking other pygame components
    pygame_mock.event.Event = MagicMock(return_value=MagicMock())
    pygame_mock.transform.smoothscale = MagicMock(return_value=mock_surface)
    pygame_mock.transform.rotate = MagicMock(return_value=mock_surface)
    pygame_mock.image.load = MagicMock(return_value=mock_surface)
    pygame_mock.MOUSEBUTTONDOWN = 1
    pygame_mock.MOUSEBUTTONUP = 2
    pygame_mock.MOUSEMOTION = 3

    # Apply the mock globally and within scripts.view.view
    with mock.patch.dict("sys.modules", {"pygame": pygame_mock}):
        with mock.patch("scripts.view.view.pygame", pygame_mock):
            yield pygame_mock

# Import after applying the mock
import scripts.view.view as view

class TestTileManipulator:
    def setup_method(self, pygame_mock):
        # Now pygame_mock.Rect is callable and works as expected
        self.mock_sprite = MagicMock()
        self.mock_sprite.rect = pygame_mock.Rect(100, 100, 50, 50)  # This should now work
        self.mock_sprite.angle_index = 0
        self.mock_sprite.url_image = "path/to/image.png"
        self.tile_manipulator = view.TileManipulator(self.mock_sprite)

    def teardown_method(self):
        del self.mock_sprite
        del self.tile_manipulator

    def test_dragging_start(self, pygame_mock):
        event = pygame_mock.event.Event(pygame_mock.MOUSEBUTTONDOWN, {"pos": (110, 110), "button": 1})
        self.tile_manipulator.update([event])
        assert self.tile_manipulator.dragging is True
        assert self.tile_manipulator.rel_pos == (10, 10)

    def test_dragging_motion(self, pygame_mock):
        self.tile_manipulator.dragging = True
        self.tile_manipulator.rel_pos = (10, 10)
        event = pygame_mock.event.Event(pygame_mock.MOUSEMOTION, {"pos": (120, 120)})
        self.tile_manipulator.update([event])
        assert self.mock_sprite.rect.topleft == (110, 110)

    def test_dragging_end(self, pygame_mock):
        self.tile_manipulator.dragging = True
        event = pygame_mock.event.Event(pygame_mock.MOUSEBUTTONUP, {})
        self.tile_manipulator.update([event])
        assert self.tile_manipulator.dragging is False

    def test_rotation_update(self, pygame_mock):
        self.tile_manipulator.dragging = True
        event = pygame_mock.event.Event(pygame_mock.MOUSEBUTTONDOWN, {"pos": (110, 110), "button": 3})
        self.tile_manipulator.update([event])
        assert self.mock_sprite.angle_index == 1

    @mock.patch("scripts.view.view.pygame.transform.smoothscale")
    @mock.patch("scripts.view.view.pygame.transform.rotate")
    @mock.patch("scripts.view.view.pygame.image.load")
    def test_preload_rotated_image(self, mock_load, mock_rotate, mock_smoothscale, pygame_mock):
        """Test the _preload_rotated_image method."""
        # Mock transformation steps
        mock_surface = pygame_mock.Surface((300, 300))
        mock_load.return_value = mock_surface
        mock_rotate.return_value = mock_surface
        mock_smoothscale.return_value = pygame_mock.Surface((81, 70))

        # Call method and force if condition
        self.tile_manipulator.sprite.angle_index = 1
        result = self.tile_manipulator._preload_rotated_image()

        # Assertions
        mock_load.assert_called_once_with("path/to/image.png")
        mock_rotate.assert_called_once_with(mock_surface, -60)

        args, _ = mock_smoothscale.call_args
        assert isinstance(args[0], MagicMock)  # Ensure the mocked Surface is passed
        assert args[0].get_size() == (200, 173)
        assert args[1] == (81, 70)

        # Test of subsurface
        subsurface_area = mock_surface.subsurface((25, 42, 200, 173)).get_size()
        assert subsurface_area == (200, 173)

        # Test result
        assert isinstance(result, MagicMock)
        assert result.get_size() == (81, 70)