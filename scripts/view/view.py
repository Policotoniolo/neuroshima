from __future__ import annotations

import random
import math
from typing import List, Tuple, Literal, Optional
import pygame
from pygame.event import Event

from scripts.utils.config import ANGLES, DISPLAY_SIZE, FPS, PIXEL_POSITION_LIST


class TileManipulator:
    """
    Handles dragging and rotation of a sprite TileView object.
    
    Attributes
    ----------
    sprite (TileView): Srite to handle
    dragging (bool): Indicates whether the object is moving
    rel_pos (Tuple[int, int]): Save initial position of the movement
    
    Methods
    ----------
    update(self, event_list : List[Event]) -> None:
        Handles both dragging and rotation based on events.
    
    Private Methods
    ----------
    _update_move(self, event_list: List[Event]) -> None:
        Update position tile by dragging it.
    _preload_rotated_image(self) -> pygame.Surface:
        Preloads rotated image of the sprite image.
    _update_angle(self, event_list: List[Event]) -> None:
        Updates the tile's angle when right-clicked.
    """
    def __init__(self, sprite: TileView) -> None:
        """Initiate the class with a given sprite TileView

        Args:
            sprite (TileView): Instance of TileView
        """
        self.sprite = sprite
        self.dragging: bool = False
        self.rel_pos: Tuple[int, int] = (0, 0)

    def update(self, event_list : List[Event]) -> None:
        """Handles both dragging and rotation based on events.

        Args:
            event_list (List[Event]): pygame event
        """
        self._update_move(event_list)
        self._update_angle(event_list)

    # --- MÉTHODES PRIVÉES ---

    def _update_move(self, event_list: List[Event]) -> None:
        """
        Update position tile by dragging it.

        Args:
            event_list (List[Event]): Pygame events list.
        """
        for event in event_list:
            # Click on the tile and get initial pixel position of the
            # mouse.
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.dragging = self.sprite.rect.collidepoint(event.pos)
                self.rel_pos = (event.pos[0] - self.sprite.rect.x,
                                event.pos[1] - self.sprite.rect.y)
            # Drag the tile and recalculate position with initial mouse
            # position.
            if event.type == pygame.MOUSEMOTION and self.dragging:
                self.sprite.rect.topleft = (event.pos[0] - self.rel_pos[0],
                                            event.pos[1] - self.rel_pos[1])
            # Realase Tile
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

    def _preload_rotated_image(self) -> pygame.Surface:
        """
        Preloads rotated image of the sprite image.
        
        Return:
            _ (List[pygame.Surface]): Rotated image
        """
        #Rotate image
        rotated_image = pygame.transform.rotate(
                    pygame.image.load(self.sprite.url_image),
                    angle = ANGLES[self.sprite.angle_index]
                    )

        #Reshape image to avoid weird transfo. The image is not a square
        if self.sprite.angle_index not in [0,3]:
            rotated_image = rotated_image.subsurface((25, 42,200,173))

        #Resize image
        rotated_image = pygame.transform.smoothscale(rotated_image, (81,70))
        return rotated_image

    def _update_angle(self, event_list: List[Event]) -> None:
        """
        Updates the tile's angle when right-clicked.

        Args:
            event_list (List[Event]): Pygame events list
        """
        for event in event_list:
            if all([event.type == pygame.MOUSEBUTTONDOWN,
                    self.dragging]):
                if event.button == 3:

                    self.sprite.angle_index = (self.sprite.angle_index+1)%6
                    rotated_image = self._preload_rotated_image()
                    new_rect = rotated_image.get_bounding_rect()
                    new_rect.topleft = self.sprite.rect.topleft
                    self.sprite.image = rotated_image
                    self.sprite.rect = new_rect


class TileView(pygame.sprite.Sprite):
    """
    Represents a visual tile in the game, managing its graphical
    representation, position, rotation, and interaction.
    This class extends `pygame.sprite.Sprite`.
    
    Attributes
    ----------
    id_tile : str
        Unique identifier for the tile.
    angle_index : int
        Index representing the tile's rotation angle (0 to 5 for
        hexagonal angles).
    url_image : str
        Path to the tile's image asset.
    image : pygame.Surface
        The visual representation of the tile, loaded and scaled.
    rect : pygame.Rect
        The rectangular boundary of the tile for positioning and
        collision detection.
    manipulator : TileManipulator
        Handles dragging and rotation of the tile.
    button : Button
        Represents an interactive button associated with the tile.

    Methods
    ---------
    update(event_list: List[Event]) -> None:
        Updates the tile's position and rotation based on user input
        events.
    click_tile(event_list: List[Event], surface: pygame.Surface
            )-> Optional[bool]:
        Displays a button on the tile and returns True if the button
        is clicked.

    Private Methods
    ----------
    _generate_image_url(id_tile: str) -> str:
        Generates the URL path for the tile's image asset based on
        its ID.
    _load_and_scale_image(url_image: str) -> pygame.Surface:
        Loads the image from the provided URL and scales it to fit
        the tile dimensions.
    _clean_position() -> None:
        Aligns the tile's position to the nearest predefined valid
        pixel position.
    """
    def __init__(self,
                id_tile: str,
                position: Tuple[int, int]=(0,0),
                angle_index: Literal[0,1,2,3,4,5] = 0
            ):
        """
        Generate the tile Sprite.

        Args:
            id_tile (str):
                ID of the tile
            position (Tuple[int, int], optional): 
                Pixel position. Defaults to (0,0).
            angle_index (Literal[0,1,2,3,4,5], optional): 
                Rotational index of the tile. Defaults to 0.
        """
        super().__init__()

        self.id_tile = id_tile
        self.angle_index = angle_index
        self.url_image: str = self._generate_image_url(id_tile)
        self.image: pygame.Surface = self._load_and_scale_image(self.url_image)
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.topleft = position
        self.manipulator = TileManipulator(self)
        self.button = Button(self.rect.topleft)

    def update(self, event_list: List[Event]) -> None:
        """
        Update position and rotation of tile. It calls methods from
        Tile Manipulator class

        Args:
            event_list (List[Event]): pygame event list
        """
        self.manipulator.update(event_list)
        self.image = self.image if self.manipulator.dragging else self.image
        self._clean_postition()

    def click_tile(self, event_list: List[Event], surface: pygame.Surface
                ) -> Optional[bool]:
        """
        prompt button on tile. Return True if click on it.
        This method calls methods from Button class.

        Args:
            event_list (List[Event]): pygame event list
            surface (pygame.Surface): surface on which displayed
        """
        self.button.enable = True
        self.button.render(surface)
        return self.button.isvalidated(event_list)

    # --- MÉTHODES PRIVÉES ---

    def _generate_image_url(self, id_tile: str) -> str:
        """
        Generates the URL path for the tile's image asset based on
        its ID.

        Args:
            id_tile (str): ID of the tile

        Returns:
            str: URL path 
        """
        for number in range(1, 8):
            id_tile = id_tile.replace(str(number), "")
        return "image/armies/"+id_tile+".png"

    def _load_and_scale_image(self, url_image: str) -> pygame.Surface:
        """
        Loads the image from the provided URL and scales it to fit
        the tile dimensions.

        Args:
            url_image (str): URL path of the image

        Returns:
            pygame.Surface: Pygame Surface
        """
        image = pygame.image.load(url_image)
        return pygame.transform.smoothscale(image, (81, 70))

    def _clean_postition(self) -> None:
        """
        Aligns the tile's position to the nearest predefined valid
        pixel position define in PIXEL_POSITION_LIST in the
        scripte/config file
        """
        # Compute all distance
        pos_relative = [((self.rect.topleft[0] - position[0])**2) +
                        (self.rect.topleft[1] - position[1])**2
                        for position in PIXEL_POSITION_LIST
                    ]
        # Find the smallest one
        index_min = min(range(len(pos_relative)), key=pos_relative.__getitem__)

        # Check if small enough
        if pos_relative[index_min] < 750:
            self.rect.topleft = PIXEL_POSITION_LIST[index_min]
            self.button.rect.topleft = self.rect.topleft


class Hexagone(pygame.sprite.Sprite):
    """
    Represente a hexagone cell on the board game,  managing its
    graphical representation, interactive features, and ability to
    highlight specific areas during gameplay.
    This class extends `pygame.sprite.Sprite`.
    
    Attributes
    ----------
    image : pygame.Surface
        The graphical surface representing the hexagon.
    rect : pygame.Rect
        The rectangular boundary of the hexagon for positioning and
        interactions.
    position : Tuple[int, int]
        The (x, y) position of the hexagon on the board in pixels.
    radius_hexa : int
        The radius of the hexagon, defining its size.
    collide : bool
        A flag indicating if the hexagon is currently involved in a
        collision or interaction.
    vertices : List[Tuple[int, int]]
        The list of vertices defining the hexagon's shape.
    button : Button
        A button associated with the hexagon for general interaction.
    cac_attacks_button : Button
        A button for melee attack actions, located on the hexagon.
    range_attacks_button : Button
        A button for ranged attack actions, located on the hexagon.

    Methods
    -------
    render(self, drawsurf: pygame.Surface,\
                colour: Tuple[int, int, int, int],\
                colour_highlight: Tuple[int, int, int, int],\
                width: int) -> None:
        Renders the hexagon on the given surface with the specified
        colors and line width.
    click_button(event_list: List[Event], surface: pygame.Surface\
            ) -> bool:
        Displays the general interaction button and returns True if
        clicked.
    attacks_cac_click_button(event_list: List[Event],\
                            surface: pygame.Surface\
                        ) -> bool:
        Displays the melee attack button and returns True if clicked.
    attacks_range_click_button(event_list: List[Event],\
                            surface: pygame.Surface\
                        ) -> bool:
        Displays the ranged attack button and returns True if clicked.

    Private Methods
    ---------------
    _minimal_radius() -> float
        Computes the minimal diameter or the diameter of the inscribed
        circle.
    _compute_vertice() -> List[Tuple[float, float]]
        Computes the vertices of the hexagon based on its position and
        radius.
    """
    def __init__(self, position: Tuple[int, int]) -> None:
        """Generate the hexagone according to the pixel position.

        Args:
            position (Tuple[int, int]): Pixel position of the hexagone.
        """
        super().__init__()
        self.image = pygame.Surface((50,50), pygame.SRCALPHA, 32)  
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.topleft = (position[0]+15, position[1]+10)

        self.radius_hexa = 42
        self.collide = False
        self.vertices = self._compute_vertice()

        self.button = Button(self.rect.topleft)
        self.cac_attacks_button = Button(
            (position[0]+2, position[1]+20),
            image="cac_attack")
        self.range_attacks_button = Button(
            (position[0]+42, position[1]+20), 
            image="range_attack")

    def render(self, drawsurf: pygame.Surface,
            colour: Tuple[int, int, int, int],
            colour_highlight: Tuple[int, int, int, int],
            width: int
        ) -> None:
        """
        Renders the hexagon on the given surface with the specified
        colors and line width.
        
        Args:
            drawsurf (pygame.Surface):
                The surface on which to draw the hexagon.
            colour (Tuple[int, int, int, int]):
                The fill RGBA color of the hexagon.
            colour_highlight (Tuple[int, int, int, int]):
                The RGBA color of the hexagon's border
            width (int):
                The width of the hexagon's border lines.
        """
        pygame.draw.polygon(drawsurf, colour, self.vertices)
        pygame.draw.polygon(drawsurf, colour_highlight, self.vertices, width)

    def click_button(self, event_list : List[Event], surface: pygame.Surface
                ) -> bool:
        """Displays a general interaction button on the hexagon and
        returns True if clicked.
        
        Args:
            event_list (List[Event]):
                A list of Pygame events to process.
        surface (pygame.Surface)
            The surface on which to render the button.

        Returns:
            _ (bool):
                True if the button is clicked, otherwise False.
        """
        self.button.enable = True
        self.button.render(surface)
        return self.button.isvalidated(event_list)

    def attacks_cac_click_button(self,
                                event_list : List[Event],
                                surface: pygame.Surface
                            ) -> bool:
        """
        Displays the melee attack button and returns True if clicked.

        Args:
            event_list (List[Event]):
                A list of Pygame events to process.
            surface (pygame.Surface):
                The surface on which to render the button.

        Returns:
            _ (bool):
                True if the button is clicked, otherwise None.
        """
        self.cac_attacks_button.enable = True
        self.cac_attacks_button.render(surface)
        return self.cac_attacks_button.isvalidated(event_list)

    def attacks_range_click_button(self, event_list, surface):
        """
        Displays the range attack button and returns True if clicked.

        Args:
            event_list (List[Event]):
                A list of Pygame events to process.
            surface (pygame.Surface):
                The surface on which to render the button.

        Returns:
            _ (bool):
                True if the button is clicked, otherwise None.
        """
        self.range_attacks_button.enable = True
        self.range_attacks_button.render(surface)
        return self.range_attacks_button.isvalidated(event_list)

    # --- MÉTHODES PRIVÉES ---

    def _minimal_radius(self) -> float:
        """
        The minimal diameter or the diameter of the inscribed circle
        
        Returns:
            _ (float):
                The minimal diameter

        """
        # https://en.wikipedia.org/wiki/Hexagon#Parameters
        return self.radius_hexa* math.cos(math.radians(30))

    def _compute_vertice(self) -> List[Tuple[float, float]]:
        """Computes the vertices of the hexagon based on its position
        and radius.

        Returns:
            Liste of the vertices of the hexagone
        """
        x, y = self.position[0] + 19, self.position[1]
        half_radius = self.radius_hexa/ 2
        minimal_radius = self._minimal_radius()
        return [
            (x, y),
            (x - half_radius, y + minimal_radius),
            (x, y + 2 * minimal_radius),
            (x + self.radius_hexa, y + 2 * minimal_radius),
            (x + 3 * half_radius, y + minimal_radius),
            (x + self.radius_hexa, y),
        ]


class EndButton(pygame.sprite.Sprite):
    """
    Represents a button to signal the end of a player's turn in the
    game. 

    This button is displayed on the screen and can be activated through
    a mouse click or specific keyboard inputs (Enter or Space).
    The class handles rendering, interaction detection, and validation
    of button clicks.

    This class extends `pygame.sprite.Sprite`.

    Attributes:
    ----------
    image (pygame.Surface):
        The visual representation of the button loaded from an image
        file.
    rect (pygame.Rect):
        The rectangle defining the button's position and dimensions.
    surface (pygame.Surface):
        The surface on which the button will be rendered.
    validated (bool):
        Indicates whether the button has been validated
        (clicked or triggered).

    Methods:
    -------
    isvalidated(event_list: List[pygame.event.Event]) -> bool:
        Checks if the button has been activated through a mouse click or 
        specific key press (Enter or Space).

    render() -> None:
        Draws the button on the specified surface.
    """
    def __init__(self, surface: pygame.Surface) -> None:
        """Initializes the EndButton on a specified rendering surface.

        Args:
            surface (pygame.Surface): 
                The surface on which the button is rendered.
        """
        super().__init__()
        self.image: pygame.Surface = pygame.image.load("image/endbutton.png")
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.topleft = (700, 585)
        self.surface = surface
        self.validated: bool = False

    def isvalidated(self, event_list: List[Event]):
        """Checks if the button has been activated through a mouse click
        or specific key press (Enter or Space).

        Args:
            event_list (pygame.event.Event): Pygame event list

        Returns:
            bool: True if click on button
        """
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return True
    def render(self):
        """Draws the button on the specified surface."""
        self.surface.blit(self.image, self.rect)


class DiscardZone(pygame.sprite.Sprite):
    """
    Represents the discard zone for tiles in the game.

    This class manages the graphical representation of the discard
    zone where tiles can be placed after being removed from play.
    It includes functionality for rendering the zone and tracking
    the tiles currently in it.

    This class extends `pygame.sprite.Sprite`.

    Attributes:
    ----------
    image (pygame.Surface):
        The visual representation of the discard zone loaded from an
        image file.
    rect (pygame.Rect):
        The rectangle defining the zone's position and dimensions.
    surface (pygame.Surface):
        The surface on which the discard zone is rendered.
    tiles (pygame.sprite.Group):
        A group containing all the tiles currently in the discard
        zone in attribut.

    Methods:
    -------
    render() -> None:
        Draws the discard zone on the specified surface.
    """
    def __init__(self, surface) -> None:
        """Initializes the KeepZone on a specified rendering surface.

        Args:
            surface (pygame.Surface): 
                The surface on which the button is rendered.e.
        """
        super().__init__()
        self.image = pygame.image.load("image/discardzone.png")
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.topleft = (150, 150)
        self.surface = surface
        self.tiles = pygame.sprite.Group()

    def render(self):
        """Draws the discard zone on the specified surface in attribut.
        """
        self.surface.blit(self.image, self.rect)


class KeepZone(pygame.sprite.Sprite):
    """
    Represents the keep zone for tiles in the game.

    The keep zone is a designated area where tiles can be retained for
    later use.
    This class handles the graphical representation of the zone and its
    rendering on the game surface.

    This class extends `pygame.sprite.Sprite`.

    Attributes:
    ----------
    image (pygame.Surface):
        The visual representation of the keep zone, loaded from an image
        file.
    rect (pygame.Rect):
        The rectangle defining the position and dimensions of the keep
        zone.
    surface (pygame.Surface):
        The surface on which the keep zone is rendered.

    Methods:
    -------
    render() -> None:
        Draws the keep zone on the specified surface in attribut.
    """
    def __init__(self, surface: pygame.Surface) -> None:
        """Initializes the KeepZone on a specified rendering surface.

        Args:
            surface (pygame.Surface): 
                The surface on which the button is rendered.e.
        """
        super().__init__()
        self.image: pygame.Surface = pygame.image.load("image/keepzone.png")
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.topleft = (745, 150)
        self.surface = surface

    def render(self):
        """Draws the keep zone on the specified surface in attribut."""
        self.surface.blit(self.image, self.rect)


class RerollButton(pygame.sprite.Sprite):
    """
    Represents a button to trigger a reroll action during the game.

    This button allows players to reroll their turn. It includes
    graphical representation, click detection, and rendering logic.

    This class extends `pygame.sprite.Sprite`.

    Attributes:
    ----------
    image (pygame.Surface):
        The visual representation of the reroll button, loaded from an
        image file.
    rect (pygame.Rect):
        The rectangle defining the button's position and dimensions.
    surface (pygame.Surface):
        The surface on which the button is rendered.
    validated (bool):
        Indicates if the button has been clicked and validated.
    enable (bool):
        Determines whether the button is active and visible.

    Methods:
    -------
    isvalidated(event_list: List[pygame.event.Event]) -> bool:
        Checks if the button has been clicked.
    
    render() -> None:
        Renders the button on the surface if it is enabled.
    """

    def __init__(self, surface: pygame.Surface, enable: bool =True) -> None:
        """Initializes the RerollButton on a specified rendering surface.

        Args:
            surface (pygame.Surface): 
                The surface on which the button is rendered.
            enable (bool, optional): 
                Indicates if the button has been clicked and validated.
                Defaults to True.
        """
        super().__init__()
        self.image: pygame.Surface= pygame.image.load("image/rerollbutton.png")
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.topleft = (800, 585)
        self.surface: pygame.Surface = surface
        self.validated: bool = False
        self.enable: bool = enable

    def isvalidated(self, event_list: List[Event]):
        """Checks if the button has been clicked.

        Args:
            event_list (pygame.event): Pygame event list

        Returns:
            bool: True if the button has been clicked, otherwise False.
        """
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    return True

    def render(self):
        """Renders the button on the surface if it is enabled."""
        if self.enable:
            self.surface.blit(self.image, self.rect)


class BoardZone():
    """
    Manages the hexagonal cells of the board with Hegagone Class,
    including their generation, rendering, collision detection, and
    highlighting.

    The `BoardZone` class is responsible for creating and managing a
    grid of hexagonal sprites. It provides functionality to render the
    board, highlight specific zones, and detect interactions or
    collisions with other sprites.

    Attributes
    ----------
    hexagones (pygame.sprite.Group):
        A group containing all hexagonal sprites on the board. Each
        hexagone is an instance of class Hexagone
    drawsurf (pygame.Surface):
        A surface used for rendering transparent overlays on the board.
    green_highlight (Tuple[int, int, int, int]):
        RGBA color for highlighted green borders.
    green (Tuple[int, int, int, int]):
        RGBA color for green hexagons.
    red_highlight (Tuple[int, int, int, int]):
        RGBA color for highlighted red borders.
    red (Tuple[int, int, int, int]):
        RGBA color for red hexagons.
    empty_color (Tuple[int, int, int, int]):
        RGBA color for empty or transparent areas.
    
    Methods
    ---------
    get_hexagone_by_position(position: tuple) -> Hexagone:
        Retrieves a hexagon at the specified pixel position.
    get_multiple_hexa(positions: List[tuple]) -> List[Hexagone]:
        Retrieves multiple hexagons by their positions.
    single_collision(sprite: pygame.sprite._SpriteSupportsGroup\
                ) -> bool:
        Checks if a sprite collides with any hexagon on the board.
    collision(group: pygame.sprite.Group) -> None:
        Updates collision status for all hexagons based on interactions 
        with a group of sprites.
    displaygreenboard() -> None:
        Renders a green transparent layer over the entire board.
    highlight_hexagones(positions_list: List[tuple]) -> None:
        Highlights specific hexagons in green by it pixel position.
    highlight_and_click_hexagones(positions_list: List[tuple],\
                    event_list: List[pygame.event.Event]) -> Hexagone:
        Highlights hexagons and checks for click events on them.
    get_neighbors_hexagone(hexagone: Hexagone) -> List[Hexagone]:
        Retrieves neighboring hexagons for a given hexagon.
    highlight_neighbors_hexagone(hexagone: Hexagone, color: str\
                            ) -> None:
        Highlights the neighbors of a hexagon in a specified color.
    highlight_non_empty(group: pygame.sprite.Group) -> None:
        Highlights hexagons colliding with any sprite in a group.
    highlight_board_empty(group: pygame.sprite.Group) -> None:
        Highlights hexagons that do not collide with any sprite in a
        group.
    
    Private Methods
    ---------
    _generate_sprite() -> None:
        Generates all hexagons for the board and adds them to the
        hexagones group.
    """
    def __init__(self) -> None:
        """
        Initializes the board zone by creating a grid of hexagonal sprites 
        and preparing the rendering surface.
        """
        self.hexagones = pygame.sprite.Group()
        self.drawsurf = pygame.Surface(DISPLAY_SIZE, pygame.SRCALPHA)
        self.drawsurf.fill(pygame.Color('#00000000'))
        self.green_highlight = (0,255,0,255)
        self.green = (0,255,0,100)
        self.red_highlight = (255,0,0,255)
        self.red = (255,0,0,100)
        self.empty_color = (0,0,0,0)
        self._generate_sprite()

    def get_hexagone_by_position(self, position: Tuple[int, int]) -> Hexagone:
        """
        Retrieves a hexagon at the specified pixel position.

        Args:
            position (tuple): The (x, y) position of the hexagon.

        Returns:
            Hexagone: The hexagon at the given position.

        Raises:
            StopIteration: If no hexagon matches the given position.
        """
        for hexagone in self.hexagones:
            if hexagone.position == position:
                return hexagone
        raise StopIteration("Any valide position")

    def get_multiple_hexa(self, positions: List[tuple]) -> List[Hexagone]:
        """
        Retrieves multiple hexagons by their pixel positions.

        Args:
            positions (List[tuple]): List of (x, y) positions.

        Returns:
            List[Hexagone]: List of hexagons corresponding to the
            positions.
        """
        return [self.get_hexagone_by_position(position)
                for position in positions
            ]

    def single_collision(self, sprite: pygame.sprite._SpriteSupportsGroup
                        ) -> bool:
        """
        Checks if a sprite collides with any hexagon on the board.

        Args:
            sprite (pygame.sprite.Sprite): The sprite to test for
            collisions.

        Returns:
            bool: True if the sprite collides with any hexagon,
            False otherwise.

        Raises:
            ValueError: If sprite is not a instance of Sprite.
        """

        if not isinstance(sprite, pygame.sprite.Sprite):
            raise ValueError(
                "Argument sprite is not a instance of pygame.sprite.Sprite"
                )

        if pygame.sprite.spritecollide(sprite, self.hexagones, False) != []:
            return True
        return False

    def collision(self, group: pygame.sprite.Group) -> None:
        """
        Updates collision status for all hexagons based on interactions
        with a group of sprites.

        Args:
            group (pygame.sprite.Group):
                The group of sprites to check for collisions.

        Raises:
            ValueError: If group is not a instance of Group. 
        """
        if not isinstance(group, pygame.sprite.Group):
            raise ValueError(
                "Argument group is not a instance of pygame.sprite.Group"
                )
        for hexagone in self.hexagones:
            if pygame.sprite.spritecollideany(hexagone, group) is not None:
                hexagone.collide = True
            else:
                hexagone.collide = False

    def displaygreenboard(self) -> None:
        """
        Renders a green transparent layer over the entire board.
        """
        self.drawsurf.fill(pygame.Color('#00000000'))
        border = pygame.image.load("image/boardgreenboarder.png")
        for hexagone in self.hexagones:
            hexagone.render(self.drawsurf,
                            (0,255,0,50),
                            (0,255,0,50),
                            width=20
                        )
        self.drawsurf.blit(border,(290,143))

    def highlight_hexagones(self, positions_list: List[Tuple[int, int]]
                        ) -> None:
        """
        Highlights specific hexagons in green by it pixel position.

        Args:
            positions_list (List[tuple]):
                List of positions of hexagons to highlight.
        """
        self.drawsurf.fill(pygame.Color('#00000000'))
        for position in positions_list:
            hexagone = self.get_hexagone_by_position(position)
            if hexagone:
                hexagone.render(self.drawsurf,
                            (0,255,0,70),
                            (0,255,0,255),
                            width=3
                        )

    def highlight_and_click_hexagones(self,
                                    positions_list: List[Tuple[int, int]],
                                    event_list: List[Event]
                                ) -> Optional[Hexagone]:
        """
        Highlights hexagons and checks for click events on them. Return
        hexagone clicked if so.

        Args:
            positions_list (List[tuple]):
                Positions of hexagons to highlight.
            event_list (List[pygame.event.Event]):
                List of Pygame events.

        Returns:
            Hexagone: The hexagon that was clicked, if any.
        """
        self.drawsurf.fill(pygame.Color('#00000000'))
        for position in positions_list:
            hexagone = self.get_hexagone_by_position(position)
            if hexagone:
                hexagone.render(self.drawsurf,
                                (0,255,0,70),
                                (0,255,0,255),
                                width=3
                            )
                if hexagone.click_button(event_list, self.drawsurf):
                    return hexagone

    def get_neighbors_hexagone(self, hexagone: Hexagone) -> List[Hexagone]:
        """
        Retrieves neighboring hexagons for a given hexagon.

        Args:
            hexagone (Hexagone): The hexagon to find neighbors for.

        Returns:
            List[Hexagone]: List of neighboring hexagons.
        """
        hexagones_collided = [
                            hex 
                            for hex in self.hexagones 
                            if pygame.sprite.collide_circle(hexagone, hex)
                        ]
        return hexagones_collided

    def highlight_neighbors_hexagone(self,
                                    hexagone: Hexagone,
                                    color:Literal["green", "red"]
                                ) -> None:
        """
        Highlights the neighbors of a hexagon in a specified color.

        Args:
            hexagone (Hexagone): The central hexagon.
            color (str): The color for highlighting ("green" or "red").
        """
        hexagones_collided = self.get_neighbors_hexagone(hexagone)
        for hex in hexagones_collided:
            if color == "green":
                hex.render(self.drawsurf, (0,255,0,70), (0,255,0,255), width=3)
            elif color == "red":
                hex.render(self.drawsurf, (255,0,0,70), (255,0,0,255), width=3)

    def highlight_board_non_empty(self, group: pygame.sprite.Group) -> None:
        """
        Highlights hexagons colliding with any sprite in a group.

        Args:
            group (pygame.sprite.Group):
                Group of sprites to check for collisions.
        """
        self.drawsurf.fill(pygame.Color('#00000000'))
        for hexagone in self.hexagones:
            if pygame.sprite.spritecollideany(hexagone, group):
                hexagone.render(self.drawsurf,
                                self.green,
                                self.green_highlight,
                                width=5
                            )

    def highlight_board_empty(self, group: pygame.sprite.Group) -> None:
        """
        Highlights hexagons that do not collide with any sprite in a
        group.

        Args:
            group (pygame.sprite.Group): 
                Group of sprites to check for collisions.
        """
        self.drawsurf.fill(pygame.Color('#00000000'))
        self.collision(group)
        for hexagone in self.hexagones:
            if not hexagone.collide:
                hexagone.render(self.drawsurf,
                                self.green,
                                self.green_highlight,
                                width=5
                            )

    # --- MÉTHODES PRIVÉES ---

    def _generate_sprite(self) -> None:
        """
        Generates all the hexagons for the board and adds them to the
        hexagones group.
        """
        for position in PIXEL_POSITION_LIST:
            hexagone = Hexagone(position=position)
            self.hexagones.add(hexagone)


class Button(pygame.sprite.Sprite):
    """
    Represents a simple interactive button in a Pygame application.

    The `Button` class manages the graphical representation and user
    interaction for a button sprite, including rendering and detecting
    clicks.

    Attributes
    ----------
    image (pygame.Surface):
        The visual representation of the button.
    rect (pygame.Rect):
        The rectangular boundary of the button used for positioning and
        collision detection.
    validated (bool):
        Indicates whether the button has been clicked and validated.
    enable (bool):
        Determines whether the button is active and should be displayed.

    Methods
    -------
    __init__(position: Tuple[int, int], image: str = "rerollbutton",\
        size: Tuple[int, int] = (35, 35), enable: bool = False):
        Initializes the button with a position, image, size, and
        activation state.
    isvalidated(event_list: List[pygame.event.Event]) -> bool:
        Checks if the button was clicked and returns `True` if validated
    render(surface: pygame.Surface) -> None:
        Displays the button on the specified surface if it is enabled.
    """
    def __init__(self,
                position: Tuple[int, int],
                image:str = "rerollbutton",
                size: tuple = (35,35),
                enable=False
            ) -> None:
        """
        Initializes the button with a position, image, size, and
        activation state.

        Args:
        ----
        position (tuple):
            The top-left position of the button on the screen.
        image (str, optional):
            The name of the image file (excluding path and extension)
            used for the button. 
            Default is "rerollbutton".
        size (tuple, optional):
            The size of the button as (width, height).
            Default is (35, 35).
        enable (bool, optional):
            Whether the button is active and can be clicked.
            Default is `False`.
        """
        super().__init__()
        self.image = pygame.image.load(f"image/{image}.png")
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.validated = False
        self.enable = enable

    def isvalidated(self, event_list: List[Event]) -> bool:
        """
        Checks whether the button has been clicked.

        If the button is clicked, it is deactivated (disabled) and
        returns `True`.

        Args:
        ----
        event_list (List[pygame.event.Event]):
            The list of Pygame events to process.

        Returns:
        -------
        bool:
            `True` if the button was clicked; otherwise, `False`.
        """
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.enable = False
                    return True
        return False

    def render(self, surface: pygame.Surface):
        """
        Displays the button on the given surface if it is enabled.

        Args:
        ----
        surface (pygame.Surface):
            The surface on which to render the button.
        """
        if self.enable:
            surface.blit(self.image, self.rect)


class View():
    """
    Manages the graphical interface for the Neuroshima game, including
    rendering the board, tiles, and interactive elements. Handles
    updating and displaying the game state such as tiles on hand, board,
    and deck, as well as user input for interactions with the game
    environment.

    Attributes
    ----------
    fps (int)
        The frames per second target for the game.
    framepersec (pygame.time.Clock):
        Pygame clock to regulate the frame rate.
    displaysurf (pygame.Surface):
        The surface where all sprite and graphics are rendered.
    background (pygame.Surface):
        Background image for the board area.
    tiles_hand (pygame.sprite.Group):
        A sprite group for holding the tiles currently in the player's
        hand.
    tiles_board (pygame.sprite.Group):
        A sprite group for the tiles placed on the game board.
    tiles_deck (pygame.sprite.Group):
        A sprite group for the deck of tiles.
    tiles_board_moving (pygame.sprite.Group):
        A sprite group for tiles that are currently abled to move on the
        board.
    discardzone (DiscardZone):
        The discard zone for discarded tiles (instance of the
        `DiscardZone` class).
    endbutton (EndButton):
        The button that allows the player to end their turn (instance of
        the `EndButton` class).
    rerollbutton (RerollButton):
        The button for rerolling tiles (instance of the `RerollButton`
        class).
    keepzone (KeepZone):
        The zone where tiles can be kept (instance of the `KeepZone`
        class).
    boardzone (BoardZone):
        The hexagonal grid area of the game board (instance of the
        `BoardZone` class).
    allsprite (pygame.sprite.Group):
        A master sprite group containing all elements of the game
        (board, tiles, buttons, etc.).

    Methods
    -------
    display_screen() -> None:
        Renders the background image and updates the screen at a 
        consistent frame rate.
    hand_tile_to_board() -> List[str]:
        Moves tiles from the player's hand to the board and returns their tile IDs.
    get_tile_to_discard() -> None:
        Moves tiles to the discard zone if they collide with it.
    get_id_tile_to_keep() -> List[int]:
        Returns the list of tile IDs to keep based on their interaction
        with the keep zone.
    get_tiles_hand(id_tiles) -> None:
        Adds tiles to the player's hand sprite group based on their IDs.
        Manage also the position of the tile on the board for the
        display.
    get_tiles_deck(deck_size: int) -> None:
        Adds face hidden tiles to the deck sprite group with random
        positions.
        It is used for prompting the remaining tiles on the board.
    generate_all_sprite_group() -> None:
        Compiles all game elements into single sprite groups for easier
        rendering and updating.
    display_all_sprite() -> None:
        Renders the all sprite groups to the display surface.
    move_tile_hand(event_list) -> None:
        Handles moving tiles of the player's hand sprite group.
    move_tile_board(event_list) -> None:
        Handles moving tiles of the tiles_board_moving sprite group.
    remove_tiles_board_moving() -> None:
        Move tiles from tile_board_moving group the tiles_board group
    
    Private Methods
    ----------
    _display_tiles_hand() -> None:
        Renders the tiles in the player's hand sprite group to the
        display surface.
    _display_tiles_board() -> None:
        Renders the tiles placed on the board sprite group to the 
        display surface
    _display_tiles_deck() -> None:
        Renders the tiles in the deck sprite group to the display
        surface.
    """
    def __init__(self) -> None:
        """
        Initializes the game view, including setting up the display
        surface, loading background image, and initializing sprite
        groups for tiles, buttons, and zones.
        """
        pygame.init()
        self.fps: int = FPS
        self.framepersec = pygame.time.Clock()
        self.displaysurf = pygame.display.set_mode(DISPLAY_SIZE)
        self.background = pygame.image.load("image/board.jpg")
        self.tiles_hand = pygame.sprite.Group()
        self.tiles_board = pygame.sprite.Group()
        self.tiles_deck = pygame.sprite.Group()
        self.tiles_board_moving = pygame.sprite.Group()
        self.discardzone = DiscardZone(self.displaysurf)
        self.endbutton = EndButton(self.displaysurf)
        self.rerollbutton = RerollButton(self.displaysurf, enable=False)
        self.keepzone = KeepZone(self.displaysurf)
        self.boardzone = BoardZone()
        self.allsprite = pygame.sprite.Group()
        pygame.display.set_caption("Neuroshima")

    def display_screen(self) -> None:
        """
        Renders the background image and updates the screen at a
        consistent frame rate.
        """
        self.displaysurf.blit(self.background, (0,0))
        self.framepersec.tick(144)

    def hand_tile_to_board(self)-> List[str]:
        """
        Moves tiles from the player's hand to the board and returns
        their tile IDs.

        Returns:
            List[str]: A list of tile IDs that were moved to the board.
        """
        tile_ids_board = []
        for tile in self.tiles_hand:
            self.tiles_board.add(tile)
            self.tiles_hand.remove(tile)
            tile_ids_board.append(tile.id_tile)
        return tile_ids_board   # Useless return, maybe suppr/Change 
                                # this method

    def get_tile_to_discard(self) -> None:
        """
        Moves tiles to the discard zone if they collide with it.
        """
        for tile in self.tiles_hand:
            if pygame.sprite.collide_rect(tile, self.discardzone):
                self.discardzone.tiles.add(tile)
                self.tiles_hand.remove(tile)

    def get_id_tile_to_keep(self) -> List[str]:
        """
        Returns the list of tile IDs to keep based on their interaction
        with the keep zone.

        Returns:
            List[int]: A list of tile IDs that the player wants to keep.
        """
        indexes_keep = [
                    tile.id_tile
                    for tile in self.tiles_hand
                    if pygame.sprite.collide_rect(tile, self.keepzone)
                ]
        return indexes_keep

    def get_tiles_hand(self, id_tiles: List[str]) -> None:
        """
        Adds tiles to the player's hand sprite group based on their IDs.
        Manage also the position of the tile on the board for the
        display.

        Args:
            id_tiles (List[str]): A list of tile IDs to add to the hand.
        """
        self.tiles_hand.clear(self.displaysurf, self.displaysurf)
        self.tiles_hand.empty()
        i = 0
        for id_tile in id_tiles:
            tile = TileView(id_tile=id_tile, position=(150,240 + i*85))
            self.tiles_hand.add(tile)
            i+=1

    def get_tiles_deck(self, deck_size: int) -> None:
        """
        Adds face hidden tiles to the deck sprite group with random
        positions.
        It is used for prompting the remaining tiles on the board.

        Args:
            deck_size (int): The actual number of tiles in deck during
            the game.
        """
        self.tiles_deck.clear(self.displaysurf, self.displaysurf)
        self.tiles_deck.empty()
        i=0
        for i in range (0,deck_size):
            tile = TileView(id_tile="borgo-qg",
                            position=(
                                10+ i*15 +random.randint(-5, 5), 
                                600 + random.randint(-10, 10)
                                )
                            )
            self.tiles_deck.add(tile)

    def generate_all_sprite_group(self) -> None:
        """Compiles all game elements into single sprite groups for
        easier rendering and updating.
        """
        self.allsprite.clear(self.displaysurf, self.displaysurf)
        self.allsprite.empty()
        self.allsprite.add(self.tiles_board)
        self.allsprite.add(self.tiles_board_moving)
        self.allsprite.add(self.tiles_hand)
        self.allsprite.add(self.tiles_deck)
        self.allsprite.add(self.endbutton)
        self.allsprite.add(self.discardzone)
        self.allsprite.add(self.keepzone)

    def display_all_sprite(self) -> None:
        """Renders the all sprite groups to the display surface.
        """
        self.allsprite.draw(self.displaysurf)

    def move_tile_hand(self, event_list: List[Event]) -> None:
        """Handles moving tiles of the player's hand sprite group.

        Args:
            event_list (List[pygame.event.Event]): liste of pygame Event
        """
        self.tiles_hand.update(event_list)
        self.display_screen()
        self.tiles_hand.draw(self.displaysurf)


    def move_tile_board(self, event_list: List[Event]) -> None:
        """Handles moving tiles of the tiles_board_moving sprite group.

        Args:
            event_list (List[pygame.event.Event]): liste of pygame Event
        """
        self.tiles_board_moving.update(event_list)
        self.display_screen()
        self.tiles_board_moving.draw(self.displaysurf)

    def remove_tiles_board_moving(self) -> None:
        """Move tiles from tile_board_moving group the tiles_board group
        """
        for tile in self.tiles_board_moving:
            self.tiles_board_moving.remove(tile)
            self.tiles_board.add(tile)

    # --- MÉTHODES PRIVÉES ---

    def _display_tiles_hand(self) -> None:
        """Renders the tiles in the player's hand sprite group
        to the display surface.
        """
        self.tiles_hand.draw(self.displaysurf)

    def _display_tiles_board(self) -> None:
        """Renders the tiles placed on the board sprite group to the
        display surface.
        """
        for tile in self.tiles_board:
            self.displaysurf.blit(tile.image, tile.rect)

    def _display_tiles_deck(self) -> None:
        """Renders the tiles in the deck sprite group to the display
        surface.
        """
        self.tiles_deck.draw(self.displaysurf)