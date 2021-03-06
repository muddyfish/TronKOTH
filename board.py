import copy
import inspect
import os
import random

from typing_hints import Position
from typing import Any, List


class Board:
    EMPTY = 0

    def __init__(self, x: int=30, y: int=20):
        self.x_size = x
        self.y_size = y
        self.size = (x, y)
        self.__board = [[Board.EMPTY for i in range(self.x_size)] for j in range(self.y_size)]
        self.locked = True

    def __repr__(self) -> str:
        return "\n".join("".join({0: " "}.get(i, str(i)) for i in row) for row in self.__board)

    def __setattr__(self, key, value):
        if key == "locked":
            self.assert_not_bot()
        super().__setattr__(key, value)

    def __getitem__(self, item: Position) -> int:
        return self.__board[item[0]][item[1]]

    def __setitem__(self, key: str, value: Any):
        if self.locked:
            self.assert_not_bot()
        self.__board[key[0]][key[1]] = value

    @staticmethod
    def assert_not_bot():
        caller_filename = inspect.stack()[2].filename
        path = os.path.normpath(caller_filename).split(os.sep)
        assert path[-2] != "bots", "Bots aren't allowed to modify the board directly." \
                                   "Use board.copy() to get a modifiable one"

    def get_random_empty_pos(self) -> Position:
        rtn = (-1, -1)
        while self[rtn] or rtn == (-1, -1):
            rtn = (random.randrange(0, self.y_size), random.randrange(0, self.x_size))
        return rtn

    def position_valid(self, pos: Position) -> bool:
        if pos[0] < 0 or pos[1] < 0:
            return False
        if pos[0] >= self.y_size or pos[1] >= self.x_size:
            return False
        return self[pos] == Board.EMPTY

    def copy(self) -> "Board":
        new_board = copy.deepcopy(self)
        if self.locked:
            new_board.locked = False
        return new_board
