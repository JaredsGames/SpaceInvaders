"""
Main driver code for Invaders
"""

# Jared Dyreson
# CPSC 386-01
# 2021-12-1
# jareddyreson@csu.fullerton.edu
# @JaredDyreson
#
# Lab 00-05
#
# Some filler text
#


import functools
from Invaders.Displays.intro_display import IntroDisplay
from Invaders.Displays.animation_display import AnimationDisplay
from Invaders.Displays.display import HighScoreDisplay
from Invaders.Displays.display_manager import DisplayManager


def main():
    """
    All implementations are run here
    """

    MANAGER = DisplayManager(
        functools.partial(IntroDisplay, ()),
        functools.partial(AnimationDisplay, ()),
        functools.partial(HighScoreDisplay, (500, "Jared"))
    )
    MANAGER.deploy()


if __name__ == "__main__":
    main()
