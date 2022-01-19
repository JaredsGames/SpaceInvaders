from Invaders.Entities.Entity import Entity
from Invaders.Dataclasses.point import Point

import pygame
import pathlib
import os
import typing
import numpy
import functools


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


def index_of(
    container: typing.List[typing.Any], comparator: typing.Callable
) -> typing.List[int]:
    """
    Obtain the indices where each item in the predicate argument
    match. This is taken right from APL and the wiki can be found here:
           https://aplwiki.com/wiki/Index_Of
    """

    return [i for i, element in enumerate(container) if comparator(element)]


class Cell:
    def __init__(self, entity, alive=True, can_shoot=False):
        self.entity = entity
        self.is_alive = alive
        self.can_shoot = can_shoot


class CustomTuple:
    def __init__(self, *args):
        self.container: typing.Tuple[int] = tuple(args)


class EnemyMatrix:
    def __init__(self, m: int, n: int, display: pygame.Surface):
        assert m == n  # quick check to see if they're the same dimension
        self.m, self.n = m, n
        self._display = display
        self.break_from_draw = False
        assets = sorted(absolute_file_paths("assets/cacodemon/"))
        self.lasers = []

        container = []

        for i in range(0, self.m):
            sub = []
            for j in range(0, self.m):
                instance = Cell(
                    Entity(
                        self._display, assets, Point(i * 95 + 175, j * 75 + 100), 100
                    ),
                    True,
                    True if i == self.m - 1 else False,
                )
                sub.append(instance)
            container.append(sub)

        # for i in range(self.m, self.m+1):
        # sub = [
        # Cell(Entity(self._display, assets, Point(
        # i * 95 + 175, j * 75 + 100), 100), True, True)
        # for j in range(0, self.m)
        # ]
        # container.append(sub)
        self.matrix = numpy.array(container, Cell)
        # self.matrix.reshape(5, 5)

    def draw(self):
        for x in range(0, self.m):
            for y in range(0, self.m):
                if self.matrix[x][y].is_alive:
                    self.matrix[x][y].entity.draw()

    def print_state(self):
        for row in self.matrix:
            string = ", ".join("1" if element.can_shoot else "0" for element in row)
            print(f"[{string}],")

    def scan_column(self) -> typing.Tuple[int]:
        """
        We need to efficiently find the positions
        where the enemies can shoot
        """

        # might be a bad name because scan is another type of algorithm like reduce
        container = []
        for (row, column) in zip(range(0, self.m - 1), range(self.m - 1, 0, -1)):
            if indices := index_of(self.matrix[:, column], lambda x: x.can_shoot):
                # get column wise indices (y coordinates)

                tuple_factory = functools.partial(CustomTuple, (row))
                indices = list(map(tuple_factory, indices))
                container.extend(indices)
        return container
