from Invaders.Dataclasses.point import Point
from Invaders.Dataclasses.direction import Direction

import pygame
import dataclasses


class Laser(pygame.sprite.Sprite):
    def __init__(
        self,
        position: Point,
        speed: int,
        direction: Direction,
        sceen_rectangle,
        asset_path: str = "assets/projectile.jpg",
    ):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill("white")
        self.rect = self.image.get_rect(center=dataclasses.astuple(position))
        self.speed = speed
        self.direction = direction
        self.sceen_rectangle = sceen_rectangle

    def destroy(self):
        if not self.sceen_rectangle.contains(self.rect):
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()
