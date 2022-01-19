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

from Invaders.Dataclasses.point import Point
from Invaders.Displays.display import Display
from Invaders.UI.button import Button


class IntroDisplay(Display):
    def __init__(self):
        super().__init__()

        self.logo_position = Point(225, 275)
        self.break_from_draw = False

        self.buttons = [
            Button(
                self._display_surface,
                Point(300, 600),
                300,
                50,
                "Start",
                functools.partial(self.terminate_intro),
            ),
        ]

    def terminate_intro(self):
        """
        Kill the current window
        """

        self.break_from_draw = True

    def draw(self) -> None:
        draw_loop = True
        logo = pygame.image.load("assets/logo.png")

        while draw_loop and not self.break_from_draw:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw_image(logo, self.logo_position)
            for button in self.buttons:
                self.write_text(
                    button.contents, button.center(), pygame.font.SysFont(None, 30)
                )
                button.draw()
            pygame.display.flip()
