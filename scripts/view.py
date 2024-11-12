"""
docstring
"""
from __future__ import annotations


import sys

import random
import math
from typing import List
import pygame
from pygame.event import Event

# pylint: disable=no-member

# Variables

ANGLES = {0:0, 1:-60, 2:-120, 3:-180, 4:-240, 5:-300}
DISPLAY_SIZE = (960,720)
TILE_HEIGHT = 70
POSITION_LIST = [(302,241),
                (301,326),
                (301,411),
                (377,198),
                (376,284),
                (376,369),
                (376,455),
                (451,155),
                (451,241),
                (451,327),
                (450,413),
                (450,499),
                (525,199),
                (525,284),
                (525,370),
                (524,455),
                (599,242),
                (598,328),
                (598,413)]
FPS = 60

###

class DragOperator:
    """drag an pygame.Rect object and change angle
    """
    def __init__(self, sprite: TileView):
        self.sprite = sprite
        self.dragging = False
        self.rel_pos = (0, 0)

    def _update_move(self, event_list: List[Event]):
        """Update position tile by dragging it

        Args:
            event_list (List[Event]): pygame event
        """
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.dragging = self.sprite.rect.collidepoint(event.pos)
                self.rel_pos = event.pos[0] - self.sprite.rect.x, event.pos[1] - self.sprite.rect.y
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
            if event.type == pygame.MOUSEMOTION and self.dragging:
                self.sprite.rect.topleft = event.pos[0] - self.rel_pos[0], event.pos[1] - self.rel_pos[1]

    def _update_angle(self, event_list: List[Event]):
        """Update angle tile with left click on it

        Args:
            event_list (List[Event]): pygame event
        """
        for event in event_list:
            if  event.type == pygame.MOUSEBUTTONDOWN and self.dragging:
                if event.button == 3:
                    self.sprite.angle_index = (self.sprite.angle_index+1)%6

                    rotated_image = pygame.transform.rotate(
                        pygame.image.load(self.sprite.url_image),
                        angle = ANGLES[self.sprite.angle_index]
                        )

                    if self.sprite.angle_index not in [0,3]:
                        rotated_image = rotated_image.subsurface((25, 42,200,173))

                    rotated_image = pygame.transform.smoothscale(rotated_image, (81,70))

                    new_rect = rotated_image.get_bounding_rect()
                    new_rect.topleft = self.sprite.rect.topleft
                    self.sprite.image = rotated_image
                    self.sprite.rect = new_rect

    def update(self, event_list : List[Event]):
        """Update position and angle tile

        Args:
            event_list (List[Event]): pygame event
        """
        self._update_move(event_list)
        self._update_angle(event_list)

class TileView(pygame.sprite.Sprite):
    """Class Tile for the view
    """
    def __init__(self, id_tile, position=(0,0), angle_index=0):
        super().__init__()
        self.id_tile = id_tile
        self.url_image = id_tile
        for number in ["1", "2", "3", "4", "5", "6", "7"]:
            self.url_image = self.url_image.replace(number, "")
        self.url_image = "image/armies/"+self.url_image+".png"
        self.image = pygame.transform.smoothscale(
            pygame.image.load(self.url_image), 
            (81,70)
        )
        self.rect = self.image.get_rect()
        self.angle_index = angle_index
        self.rect.topleft = position
        self.drag = DragOperator(self)
        self.button = Button(self.rect.topleft)

    def _clean_postition(self):
        """transform approximative position to real board posistion 
        (global POSITION_LIST)
        """
        pos_relative = [((self.rect.topleft[0] - position[0])**2) +
                        (self.rect.topleft[1] - position[1])**2
                        for position in POSITION_LIST
                    ]
        index_min = min(range(len(pos_relative)), key=pos_relative.__getitem__)
        if pos_relative[index_min] < 750:
            self.rect.topleft = POSITION_LIST[index_min]
            self.button.rect.topleft = self.rect.topleft

    def update(self, event_list):
        """update for dragging and angle tile

        Args:
            event_list (_type_): pygame event liste
        """
        self.drag.update(event_list)
        self.image = self.image if self.drag.dragging else self.image
        self._clean_postition()

    def click_tile(self, event_list, surface):
        """prompt button on tile"""
        self.button.enable = True
        self.button.render(surface)
        return self.button.isvalidated(event_list)

class Hexagone(pygame.sprite.Sprite):
    """hexagone polygone Class
    """
    def __init__(self, position) -> None:
        super().__init__()
        self.image = pygame.Surface((50,50), pygame.SRCALPHA, 32 )  
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.topleft = (position[0]+15, position[1]+10)
        self.radius = 50

        self.radius_hexa = 42
        self.collide = False
        self.vertices = self._compute_vertice()

        self.button = Button(self.rect.topleft)
        self.cac_attacks_button = Button(
            (position[0]+2, position[1]+20),
            image="cac_attack"
        )
        self.range_attacks_button = Button(
            (position[0]+42, position[1]+20), 
            image="range_attack"
        )

    def minimal_radius(self) -> float:
        """Horizontal length of the hexagon"""
        # https://en.wikipedia.org/wiki/Hexagon#Parameters
        return self.radius_hexa* math.cos(math.radians(30))

    def _compute_vertice(self):
        x, y = self.position[0] + 19, self.position[1]
        half_radius = self.radius_hexa/ 2
        minimal_radius = self.minimal_radius()
        return [
            (x, y),
            (x - half_radius, y + minimal_radius),
            (x, y + 2 * minimal_radius),
            (x + self.radius_hexa, y + 2 * minimal_radius),
            (x + 3 * half_radius, y + minimal_radius),
            (x + self.radius_hexa, y),
        ]

    def render(self, drawsurf, colour, colour_highlight, width) -> None:
        """Renders the hexagon on the screen"""
        pygame.draw.polygon(drawsurf, colour, self.vertices)
        pygame.draw.polygon(drawsurf, colour_highlight, self.vertices, width)

    def click_button(self, event_list, surface):
        """prompt button on tile"""
        self.button.enable = True
        self.button.render(surface)
        return self.button.isvalidated(event_list)

    def attacks_cac_click_button(self, event_list, surface):
        self.cac_attacks_button.enable = True
        self.cac_attacks_button.render(surface)
        return self.cac_attacks_button.isvalidated(event_list)

    def attacks_range_click_button(self, event_list, surface):
        self.range_attacks_button.enable = True
        self.range_attacks_button.render(surface)
        return self.range_attacks_button.isvalidated(event_list)


class EndButton(pygame.sprite.Sprite):
    """end button turn sprite

    Args:
        pygame (_type_): _description_
    """
    def __init__(self, surface) -> None:
        super().__init__()
        self.image = pygame.image.load("image/endbutton.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (700, 585)
        self.surface = surface
        self.validated = False

    def isvalidated(self, event_list: List[pygame.event.Event]):
        """return true if button click

        Args:
            event_list (pygame.event.Event): Pygame event lsit

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
        """display button"""
        self.surface.blit(self.image, self.rect)

class DiscardZone(pygame.sprite.Sprite):
    """Discarde zone sprite for tiles
    """
    def __init__(self, surface) -> None:
        super().__init__()
        self.image = pygame.image.load("image/discardzone.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (150, 150)
        self.surface = surface
        self.tiles = pygame.sprite.Group()

    def render(self):
        """display button"""
        self.surface.blit(self.image, self.rect)

class KeepZone(pygame.sprite.Sprite):
    """Keep zone sprite for tiles
    """
    def __init__(self, surface) -> None:
        super().__init__()
        self.image = pygame.image.load("image/keepzone.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (745, 150)
        self.surface = surface

    def render(self):
        """display button"""
        self.surface.blit(self.image, self.rect)

class RerollButton(pygame.sprite.Sprite):
    """reroll turn button sprite
    """

    def __init__(self, surface, enable=True) -> None:
        super().__init__()
        self.image = pygame.image.load("image/rerollbutton.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (800, 585)
        self.surface = surface
        self.validated = False
        self.enable = enable

    def isvalidated(self, event_list):
        """return true if button click

        Args:
            event_list (pygame.event): Pygame event list

        Returns:
            bool: True if validated
        """
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    return True
    def render(self):
        """display button"""
        if self.enable:
            self.surface.blit(self.image, self.rect)

class BoardZone():
    """Class for generating hexagone shapes and display with transparance on the board
    """
    def __init__(self) -> None:
        self.hexagones = pygame.sprite.Group()
        self.drawsurf = pygame.Surface(DISPLAY_SIZE, pygame.SRCALPHA)
        self.drawsurf.fill(pygame.Color('#00000000'))
        self.green_highlight = (0,255,0,255)
        self.green = (0,255,0,100)
        self.red_highlight = (255,0,0,255)
        self.red = (255,0,0,100)
        self.empty_color = (0,0,0,0)
        self.generate_sprite()

    def generate_sprite(self) -> None:
        """generate all the hexagone of the board
        """
        for position in POSITION_LIST:
            hexagone = Hexagone(position=position)
            self.hexagones.add(hexagone)

    def get_hexagone_by_position(self, position: tuple) -> Hexagone|None:
        try:
            for hexagone in self.hexagones:
                if hexagone.position == position:
                    return hexagone
        except StopIteration:
            print("Any valide position")

    def get_multiple_hexa(self, positions: List[tuple]) -> List[Hexagone]:
        hexagones = []
        for position in positions:
            hexagones.append(self.get_hexagone_by_position(position))
        return hexagones

    def single_collision(self, sprite: pygame.sprite._SpriteSupportsGroup) -> bool:
        """Test if a sprite collide with any hexagones on the board

        Args:
            sprite (pygame.sprite.Sprite): Sprite to check

        Returns:
            bool: Return True if Sprite collide with the board
        """
        if pygame.sprite.spritecollide(sprite, self.hexagones, False) != []:
            return True
        return False

    def collision(self, group: pygame.sprite.Group) -> None:
        """Check if hexagones collide with any sprite in the group
        Args:
            group (pygame.sprite.Group): Sprite groupe to checke
        """
        for hexagone in self.hexagones:
            if pygame.sprite.spritecollideany(hexagone, group) is not None:
                hexagone.collide = True
            else:
                hexagone.collide = False

    def displaygreenboard(self):
        """Display a green layer on all the board
        """
        self.drawsurf.fill(pygame.Color('#00000000'))
        border = pygame.image.load("image/boardgreenboarder.png")
        for hexagone in self.hexagones:
            hexagone.render(self.drawsurf, (0,255,0,50), (0,255,0,50), width=20)
        self.drawsurf.blit(border,(290,143))

    def highlight_hexagones(self, positions_list: List) -> None:
        self.drawsurf.fill(pygame.Color('#00000000'))
        for position in positions_list:
            hexagone = self.get_hexagone_by_position(position)
            if hexagone is not None:
                hexagone.render(self.drawsurf, (0,255,0,70), (0,255,0,255), width=3)

    def highlight_and_click_hexagones(self, positions_list: List, event_list):
        self.drawsurf.fill(pygame.Color('#00000000'))
        for position in positions_list:
            hexagone = self.get_hexagone_by_position(position)
            if hexagone is not None:
                hexagone.render(self.drawsurf, (0,255,0,70), (0,255,0,255), width=3)
                if hexagone.click_button(event_list, self.drawsurf):
                    return hexagone

    def get_neighbors_hexagone(self, hexagone):
        hexagones_collided = []
        for hex in self.hexagones:
            if pygame.sprite.collide_circle(hexagone, hex):
                hexagones_collided.append(hex)
        return hexagones_collided

    def highlight_neighbors_hexagone(self, hexagone, color:str):
        hexagones_collided = self.get_neighbors_hexagone(hexagone)
        for hex in hexagones_collided:
            if color == "green":
                hex.render(self.drawsurf, (0,255,0,70), (0,255,0,255), width=3)
            elif color == "red":
                hex.render(self.drawsurf, (255,0,0,70), (255,0,0,255), width=3)

    def highlight_non_empty(self, group: pygame.sprite.Group) -> None:
        """highlight hexgone on the board collinding with a sprit group

        Args:
            group (pygame.sprite.Group): Sprite groupe to checke
        """
        self.drawsurf.fill(pygame.Color('#00000000'))
        for hexagone in self.hexagones:
            if pygame.sprite.spritecollideany(hexagone, group):
                hexagone.render(self.drawsurf, self.green, self.green_highlight, width=5)


    def highlight_board_empty(self, group: pygame.sprite.Group) -> None:
        """Display green hexagone on the sprite if not colliding with the group

        Args:
            group (pygame.sprite.Group): Sprite groupe to checke
        """
        self.drawsurf.fill(pygame.Color('#00000000'))
        self.collision(group)
        for hexagone in self.hexagones:
            if not hexagone.collide:
                hexagone.render(self.drawsurf, self.green, self.green_highlight, width=5)

class Button(pygame.sprite.Sprite):
    """Simple button sprite
    """
    def __init__(self, position, image:str = "rerollbutton", size: tuple = (35,35), enable=False) -> None:
        super().__init__()
        self.image = pygame.image.load(f"image/{image}.png")
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.validated = False
        self.enable = enable

    def isvalidated(self, event_list):
        """return true if button click
        """
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.enable = False
                    return True

    def render(self, surface):
        """display button
        Args:
            surface (pygame.Surface) : Surface to render on
        """
        if self.enable:
            surface.blit(self.image, self.rect)
            # pygame.display.flip()

class View():
    """class for prompting board and tiles
    """
    def __init__(self) -> None:
        pygame.init()
        self.fps = FPS
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

    def display_screen(self):
        """Display screen background
        """
        self.displaysurf.blit(self.background, (0,0))
        self.framepersec.tick(144)

    def hand_tile_to_board(self)-> List[str]:
        """Add a TileView object in the sprite group board

        Args:
            tile (TileView): tile to add
        """
        tile_ids_board = []
        for tile in self.tiles_hand:
            self.tiles_board.add(tile)
            self.tiles_hand.remove(tile)
            tile_ids_board.append(tile.id_tile)
        return tile_ids_board

    def get_tile_to_discard(self):
        """move tile to the discard list if collide with the discard zone
        """
        for tile in self.tiles_hand:
            if pygame.sprite.collide_rect(tile, self.discardzone):
                self.discardzone.tiles.add(tile)
                self.tiles_hand.remove(tile)

    def get_id_tile_to_keep(self) -> List[int]:
        """return index of tile to keep in hand

        Returns:
            List[int]: list of index
        """
        indexes_keep = []
        for tile in self.tiles_hand:
            if pygame.sprite.collide_rect(tile, self.keepzone):
                indexes_keep.append(tile.id_tile)
        return indexes_keep

    def get_tiles_hand(self, id_tiles):
        """add tiles in the sprite groupe hand"""

        self.tiles_hand.clear(self.displaysurf, self.displaysurf)
        self.tiles_hand.empty()
        i = 0
        for id_tile in id_tiles:
            tile = TileView(id_tile=id_tile, position=(150,240 + i*85))
            self.tiles_hand.add(tile)
            i+=1

    def get_tiles_deck(self, deck_size: int):
        """add tiles in the sprite group deck"""
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

    def _display_tiles_hand(self):
        """display sprites group hand
        """
        self.tiles_hand.draw(self.displaysurf)

    def _display_tiles_board(self):
        """display sprite group board
        """
        for tile in self.tiles_board:
            self.displaysurf.blit(tile.image, tile.rect)

    def _display_tiles_deck(self):
        """Display sprite group deck"""
        self.tiles_deck.draw(self.displaysurf)

    def generate_all_sprite_group(self):
        """Create a sprite group including all the sprites game"
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

    def display_all_sprite(self):
        """Display the allsprite group
        """
        self.allsprite.draw(self.displaysurf)

    def move_tile_hand(self, event_list):
        """move tile hand sprite group

        Args:
            event_list (List[pygame.event.Event]): liste of pygame Event
        """
        self.tiles_hand.update(event_list)
        self.display_screen()
        self.tiles_hand.draw(self.displaysurf)


    def move_tile_board(self, event_list):
        """move tile_board_moving sprite group

        Args:
            event_list (_type_): _description_
        """
        self.tiles_board_moving.update(event_list)
        self.display_screen()
        self.tiles_board_moving.draw(self.displaysurf)

    def remove_tiles_board_moving(self):
        """remove tile from tile_board_moving and add tile in tile board view 
        at the end of a turn
        """
        for tile in self.tiles_board_moving:
            self.tiles_board_moving.remove(tile)
            self.tiles_board.add(tile)

if __name__ == "__main__":
    hex = Hexagone((376,369))
    view = View()
    view.display_screen()
    run = True
    while run:

        event_list = pygame.event.get()
        for event in event_list:
            view.display_screen()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            hex.render(view.boardzone.drawsurf,(0,255,0,71), (0,255,0,255), width=3)
            
            
            if hex.attacks_cac_click_button(event_list, view.boardzone.drawsurf):
                print("yo")
            if hex.attacks_range_click_button(event_list, view.boardzone.drawsurf):
                print("yo")
            view.displaysurf.blit(view.boardzone.drawsurf, (0,0))
            pygame.display.flip()
            
