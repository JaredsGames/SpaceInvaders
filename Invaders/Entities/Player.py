from Invaders.Entities.Entity import Entity
from Invaders.Dataclasses.point import Point
from Invaders.Entities.laser import Laser

import pygame
import typing
import pathlib


class Player(Entity):
    def __init__(
        self,
        master_display: pygame.Surface,
        sprites: typing.List[pathlib.Path],
        position: Point,
        health: int = 100,
    ):
        super().__init__(master_display, sprites, position, 1000)
