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
This module contains a basic "factory" pattern for generating new Display instances
"""

import abc
import dataclasses
import functools
import json
import pathlib
import pygame
import sys
import time
import typing
from datetime import datetime

from Invaders.UI.button import Button
from Invaders.Dataclasses.direction import Direction
from Invaders.Dataclasses.player import Player
from Invaders.Dataclasses.point import Point


class Display:
    """
    Not fully virtual class for each display to
    inherit from
    """

    def __init__(
        self, width: int = 900, height: int = 900, color=pygame.Color("black")
    ):
        # Checks for errors encountered
        _, num_fail = pygame.init()
        if num_fail > 0:
            print(f"[FATAL] There were {num_fail} error(s) produced!")
            sys.exit(-1)
        else:
            print("[+] Game successfully initialised")
        pygame.font.init()
        self.width, self.height = width, height
        self._display_surface = pygame.display.set_mode(
            (self.width, self.height), pygame.HWSURFACE
        )
        self.last_position = Point(-1, -1)
        self.background_color = color
        self.fps_meter = pygame.time.Clock()

    @abc.abstractmethod
    def draw(self):
        """
        Abstract draw class that must be implemented
        """

        raise NotImplementedError(
            f"Display.draw isn abstract method and should not be invoked directly"
        )

    def get_surface(self) -> pygame.Surface:
        """
        Obtain the current display surface
        to a given window
        @return - pygame.Surface
        """

        return self._display_surface

    def clear_text(self) -> None:
        """
        This removes all text from the screen
        """

        self._display_surface.fill(self.background_color)

    def draw_image(self, img_object: pygame.Surface, position: Point) -> None:
        """
        Draw an image object (in the form of a surface) to the screen
        at a given position
        @param img_object : currently loaded pygame surface that represents an image
        @param position : Cartesian coordinates that represent where on the screen to be drawn to
        """

        self._display_surface.blit(img_object, dataclasses.astuple(position))

    def write_text(
        self, text: str, position: Point, font, color=pygame.Color("white")
    ) -> None:
        """
        Write text to the screen, thanks to @NICE
        for helping with this!
        @param text - stuff we want to write to the screen
        @param position - where on the screen should it be writing to
        @param font - current font used
        @param color - selected color
        """

        lines = [line.split(" ") for line in text.splitlines()]
        space = font.size(" ")[0]

        x, y = dataclasses.astuple(position)
        self.last_position = position

        for line in lines:
            for word in line:
                word_surface = font.render(word, 0, color)
                width, height = word_surface.get_size()
                if x + width >= self.width + 100:
                    x = position.x
                    y += height
                self._display_surface.blit(word_surface, (x, y))
                x += width + space
            x = position.x
            y += height

    def center(self) -> Point:
        """
        Obtain the center of the current scene
        @return Point
        """

        return Point(self.width // 4, self.height // 4)


class HighScoreDisplay(Display):
    """
    Class that represents the high score display
    """

    def __init__(self, current_score: int, username: str):
        super().__init__()
        self.title_position = Point(250, 45)
        self.logo_position = Point(575, 435)
        self.break_from_draw = False
        self.back_button = Button(
            self._display_surface,
            Point(300, 575),
            300,
            50,
            "Quit",
            functools.partial(self.terminate_intro),
        )
        self.scoreboard_file = pathlib.Path("scores/scoreboard.json")
        self.scores = self.obtain_high_score_list(self.scoreboard_file)
        self.scores.append(
            Player(username, current_score,
                   datetime.now().strftime("%m/%d/%Y %H:%M"))
        )
        self.scores = sorted(self.scores, reverse=True)

    def obtain_high_score_list(self, path: pathlib.Path) -> typing.List[Player]:
        """
        Read in high score list found in a json file
        that is then loaded and sorted by the score obtained
        by a given player
        @param path - path to JSON file
        @return - typing.List[Player]
        """

        with open(path, "r") as fp:
            contents = json.load(fp)

        return [Player(**element) for element in contents["players"]]

    def terminate_intro(self):
        """
        This terminates the current scene
        """

        self.break_from_draw = True
        self._display_surface.fill(self.background_color)
        master = {"players": []}
        for score in self.scores:
            master["players"].append(dataclasses.asdict(score))

        with open(self.scoreboard_file, "w") as fp:
            json.dump(master, fp)

        pygame.quit()
        sys.exit()

    def draw(self):
        """
        Draw all the high scores in a row like
        manner
        """

        draw_loop = True

        while draw_loop and not self.break_from_draw:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate_intro()

            self.write_text(
                f"HIGH SCORES", self.title_position, pygame.font.SysFont(
                    None, 50)
            )

            self.write_text(
                self.back_button.contents,
                self.back_button.center(),
                pygame.font.SysFont(None, 30),
            )
            self.back_button.draw()

            for i, score in enumerate(self.scores[0:5]):
                x, y = dataclasses.astuple(self.center())
                self.write_text(
                    score.name,
                    Point((x - 50), y + i * 50),
                    pygame.font.SysFont(None, 33),
                )
                self.write_text(
                    str(score.score),
                    Point((x - 50) + 200, y + i * 50),
                    pygame.font.SysFont(None, 33),
                )

                self.write_text(
                    score.tod,
                    Point((x - 50) + 400, y + i * 50),
                    pygame.font.SysFont(None, 33),
                )
            pygame.display.flip()
