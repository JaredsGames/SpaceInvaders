import abc
import typing
import pathlib
import pygame
import dataclasses

from Invaders.Dataclasses.point import Point
from Invaders.Dataclasses.direction import Direction

from Invaders.Entities.laser import Laser

"""
This module contains the template for entity like classes
"""


class Entity(pygame.sprite.Sprite):
    """
    Virtual class for all entities to inherit from
    """

    def __init__(
        self,
        master_display: pygame.Surface,
        sprites: typing.List[pathlib.Path],
        position: Point,
        health: int = 100,
    ):
        super().__init__()
        self.assets = self.load_sprites(sprites)
        self.health = health
        self.current_sprite = 0
        self.image = self.assets[0]
        self._master_display = master_display
        self.position = position
        self.break_from_draw = False
        self.rect = self.image.get_rect(center=dataclasses.astuple(self.position))
        self.rect.topleft = dataclasses.astuple(position)
        self.ready = True
        self.laser_epoch = 0
        self.lasers = pygame.sprite.Group()

    def load_sprites(
        self, sprites: typing.List[pathlib.Path]
    ) -> typing.List[pygame.Surface]:
        """
        Load all the sprites for a given entity
        @param sprites - paths to the images that will represent the sprites
        @return - typing.List[pygame.Surface]
        """

        return list(map(pygame.image.load, sprites))

    @abc.abstractclassmethod
    def animate(self):
        """
        How the entity should appear on the screen
        """

        draw_loop = True

        while draw_loop or self.health > 0 and not self.break_from_draw:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.break_from_draw = True

        raise NotImplementedError(
            f"Virtual entity class cannot run this function, please use a generalized class instance"
        )

    def draw(self) -> None:
        """
        Draw the current sprite frame to the display
        """

        self._master_display.blit(
            self.assets[self.current_sprite], dataclasses.astuple(self.position)
        )

    def update(self, speed: typing.Union[int, float]) -> None:
        """
        Update the position in which we need to change to the next frame
        of the sprite's animation

        @param speed: takes an integer like object to increment the position in the assets container
        """

        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.assets):
            self.current_sprite = 0

        self.image = self.assets[int(self.current_sprite)]
        self.recharge()
        self.lasers.update()

    def fire(self, direction: Direction = Direction.NORTH, return_laser=False):
        """
        Mechanic to fire the laser at an opponent
        Takes a cardinal direction to determine the velocity
        Steps:
        - spawn a projectile position
        - give projectile a velocity
        - hand off to another entity
        """

        velocity = -8 if (direction == Direction.NORTH.value) else 8
        current_position = self.assets[self.current_sprite].get_rect()
        shot_laser = Laser(
            self.position, velocity, direction, self._master_display.get_rect()
        )
        if not return_laser:
            # this is a janky fix
            self.lasers.add(shot_laser)
        self.laser_epoch = pygame.time.get_ticks()
        self.ready = False
        return None if not return_laser else shot_laser

    def recharge(self):
        """
        Allow the time for the entity to have about 1 second of delay
        until they can fire again
        """

        if not self.ready:
            current = pygame.time.get_ticks()
            if current - self.laser_epoch >= 1000:
                self.ready = True
