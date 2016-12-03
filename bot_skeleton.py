from abc import ABCMeta, abstractmethod


class BotSkeleton(metaclass=ABCMeta):
    def __init__(self, no_bots, bot_id):
        self.no_bots = no_bots
        self.bot_id = bot_id

    def __repr__(self):
        return self.name

    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def make_move(self, board, position):
        raise NotImplemented()

    def add_log(self, log):
        self.log = log

    @property
    def log_name(self):
        return self.name+"_"+str(self.bot_id)