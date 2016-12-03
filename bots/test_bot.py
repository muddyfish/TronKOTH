from bot_skeleton import BotSkeleton

import random


class Test(BotSkeleton):
    def make_move(self, board, position):
        self.board = board
        self.position = position
        valid_moves = self.get_valid_moves()
        return random.choice(valid_moves)

    def get_valid_moves(self):
        moves = filter(self.board.position_valid, ((self.position[0]+1, self.position[1]),
                                                   (self.position[0]-1, self.position[1]),
                                                   (self.position[0], self.position[1]+1),
                                                   (self.position[0], self.position[1]-1)))
        return list(moves)
