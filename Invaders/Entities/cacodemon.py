from Invaders.Entities.Entity import Entity
from Invaders.Dataclasses.point import Point

import typing
import itertools
import pygame
import pathlib


class Cacodemon(Entity):
    def __init__(
        self,
        master_display: pygame.Surface,
        sprites: typing.List[pathlib.Path],
        position: Point,
        health: int = 100,
    ):
        super().__init__(master_display, sprites, position, health)
        print(super())
