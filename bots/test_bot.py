from bot_skeleton import BotSkeleton

import random


class Test(BotSkeleton):
    def make_move(self, board, positions):
        self.board = board
        self.position = positions[self.bot_id]
        valid_moves = self.get_valid_moves()
        try:
            return random.choice(valid_moves)
        except IndexError:
            return None

    def get_valid_moves(self):
        moves = filter(self.board.position_valid, ((self.position[0]+1, self.position[1]),
                                                   (self.position[0]-1, self.position[1]),
                                                   (self.position[0], self.position[1]+1),
                                                   (self.position[0], self.position[1]-1)))
        return list(moves)
