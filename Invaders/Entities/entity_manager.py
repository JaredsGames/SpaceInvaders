import pygame
import typing

from Invaders.Entities.Entity import Entity


class EntityManager:
    def __init__(self, entities: typing.Dict[str, Entity]):
        self.entities = entities
