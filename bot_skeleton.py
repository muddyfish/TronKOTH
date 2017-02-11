from abc import ABCMeta, abstractmethod
from typing_hints import Position, BotID, PositionDict
from board import Board


class BotSkeleton(metaclass=ABCMeta):
    def __init__(self, no_bots: int, bot_id: BotID):
        self.no_bots = no_bots
        self.bot_id = bot_id
        self.log = None

    def __repr__(self) -> str:
        return self.name

    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def make_move(self, board: Board, positions: PositionDict) -> Position:
        raise NotImplemented()

    @property
    def log_name(self):
        return "{}_{}".format(self.name, str(self.bot_id))
