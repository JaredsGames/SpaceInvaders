import pygame
import dataclasses


class Projectile(pygame.sprite.Sprite):
    def __init__(self, path: str = "assets/rocket.png"):
        self.asset = pygame.image.load(path)
