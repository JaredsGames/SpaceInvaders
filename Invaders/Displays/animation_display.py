# Jared Dyreson
# CPSC 386-01
# 2021-11-29
# jareddyreson@csu.fullerton.edu
# @JaredDyreson
#
# Lab 00-04
#
# Some filler text
#

"""
This module contains the Intro display class
"""

import pygame
import functools
import sys
import pathlib
import typing
import os
import dataclasses
import random
from pprint import pprint as pp
import time

from Invaders.Dataclasses.point import Point
from Invaders.Displays.display import Display
from Invaders.UI.button import Button

# from Invaders.Entities.cacodemon import Cacodemon
# from Invaders.Entities.Entity import Entity
from Invaders.Entities.enemy_matrix import EnemyMatrix

# from Invaders.Entities.Player import Player
from Invaders.Entities.Entity import Entity
from Invaders.Dataclasses.direction import Direction

# TODO : move this to its own respective module or something like that


def absolute_file_paths(directory: pathlib.Path) -> typing.List[pathlib.Path]:
    """
    List the contents of a directory with their absolute path
    @param directory: path where to look
    @return: typing.List[pathlib.Path]
    """

    return [
        pathlib.Path(os.path.abspath(os.path.join(dirpath, f)))
        for dirpath, _, filenames in os.walk(directory)
        for f in filenames
    ]


class AnimationDisplay(Display):
    def __init__(self):
        super().__init__()

        self.break_from_draw = False
        self.entities = EnemyMatrix(5, 5, self._display_surface)
        self.main_player = Entity(
            self._display_surface, ["assets/rocket.png"], Point(550, 700)
        )
        # self.main_player = Player(self._display_surface, [
        # "assets/rocket.png"], Point(550, 700))

        self.DRAW_NEXT_ENTITY = pygame.USEREVENT + 1
        self.ENEMY_FIRE_INTERVAL = pygame.USEREVENT + 2
        self.score, self.lives = 0, 3
        self.score_label_position = Point(775, 20)
        self.lives_label_position = Point(775, 60)

    def draw(self) -> None:
        draw_loop = True
        pygame.time.set_timer(self.DRAW_NEXT_ENTITY, 300)
        pygame.time.set_timer(self.ENEMY_FIRE_INTERVAL, 2000)

        will_move = False

        enemy_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        enemy_laser_group = pygame.sprite.Group()

        player_group.add(self.main_player)
        # print(player_group)

        for x, row in enumerate(self.entities.matrix):
            for y, column in enumerate(row):
                enemy_group.add(column.entity)
        # FIXME

        while draw_loop and not self.break_from_draw:
            positions = self.entities.scan_column()  # FIXME: this code is not working

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == self.DRAW_NEXT_ENTITY:
                    self._display_surface.fill(pygame.Color("black"))
                    enemy_group.update(1)
                elif event.type == self.ENEMY_FIRE_INTERVAL:
                    for position in random.choices(positions, k=2):
                        x, y = position.container
                        __laser = self.entities.matrix[x][y].entity.fire(
                            Direction.SOUTH.value, True
                        )
                        enemy_laser_group.add(__laser)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.main_player.fire(Direction.NORTH.value)
                    if event.key == pygame.K_LEFT:
                        self.main_player.position.x -= 20
                    if event.key == pygame.K_RIGHT:
                        self.main_player.position.x += 20
                    will_move = True
                elif event.type != pygame.KEYDOWN:
                    will_move = False

            if pygame.sprite.groupcollide(
                self.main_player.lasers, enemy_group, True, True
            ):
                self.score += 20

            if pygame.sprite.groupcollide(
                enemy_laser_group, player_group, False, False
            ):
                print("hit the player!")
                self.lives -= 1

            self._display_surface.fill(self.background_color)
            enemy_group.draw(self._display_surface)
            self.main_player.draw()
            self.main_player.lasers.draw(self._display_surface)

            enemy_laser_group.draw(self._display_surface)
            enemy_laser_group.update()

            if not enemy_group:
                draw_loop = False

            self.write_text(
                f"Score: {self.score}",
                self.score_label_position,
                pygame.font.SysFont(None, 30),
            )

            self.write_text(
                f"Lives: {self.lives}",
                self.lives_label_position,
                pygame.font.SysFont(None, 30),
            )

            self.main_player.update(1)
            pygame.display.flip()
            self.fps_meter.tick(60)
