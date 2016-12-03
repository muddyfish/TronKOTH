from typing import List, Union
from typing_hints import Position
from bot_skeleton import BotSkeleton
from board import Board

from multiprocessing.pool import ThreadPool
from multiprocessing.context import TimeoutError
import time
import os
import traceback
try:
    import curses
except ImportError:
    print("""
curses not found.
Windows users should install http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses for their python version""")
    has_curses = False
    time.sleep(0.5)
else:
    has_curses = True
#has_curses = False


class Game:
    timeout = 10
    colours = (15, 14, 13, 12, 11, 10, 9, 8)
    non_filled = 2

    def __init__(self, bots):
        self.board, bot_positions = self.init_board(len(bots))
        self.bots = self.init_bots(bots)
        self.logs = self.init_logs()
        self.bot_names = [bot.name for bot in self.bots]
        if has_curses:
            self.init_screen()
        else:
            for bot in self.bots:
                print(bot.bot_id, "-", bot.name, bot.log_name)
        print("Game started with {}".format(self.bots))
        while len(self.bots) > 1:
            self.show_board()
            new_positions = self.update_bots(bot_positions)
            self.bots, bot_positions = self.check_dead(bot_positions, new_positions)
        for log in self.logs:
            log.close()
        #curses.endwin()

    def init_screen(self):
        self.screen = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, Game.non_filled, Game.non_filled)
        for i, colour in enumerate(Game.colours):
            curses.init_pair(i + 2, colour, colour)

    def init_logs(self):
        logs = []
        for bot in self.bots:
            new_log = open(os.path.join("logs", bot.log_name+".log"), "w")
            bot.add_log(new_log)
            logs.append(new_log)
        return logs

    def init_bots(self, bots: List[type]) -> List[BotSkeleton]:
        rtn = []
        for i, bot in enumerate(bots):
            rtn.append(bot(no_bots=len(bots), bot_id=i+1))
        return rtn

    def init_board(self, no_bots: int) -> (Board, List[Position]):
        board = Board()
        positions = []
        for bot_id in range(no_bots):
            new_pos = board.get_random_empty_pos()
            positions.append(new_pos)
            board[new_pos] = bot_id+1
        return board, positions

    def update_bots(self, bot_positions: List[Position]) -> List[Position]:
        rtn = []

        threads = []
        pool = ThreadPool(len(self.bots))
        position_dict = {bot.bot_id: pos for bot, pos in zip(self.bots, bot_positions)}
        for bot in self.bots:
            threads.append(pool.apply_async(bot.make_move, args=(self.board, position_dict)))
        start = time.time()
        while time.time() - start <= Game.timeout:
            if all(thread.ready() for thread in threads):
                break
            time.sleep(0.01)
        else:
            pool.terminate()
        for thread, bot in zip(threads, self.bots):
            try:
                rtn.append(thread.get(0))
            except TimeoutError:
                rtn.append(None)
                bot.log.write("\nTimed out\n")
            except KeyboardInterrupt:
                raise
            except:
                bot.log.write("\n")
                bot.log.write(traceback.format_exc())
                bot.log.write("\n")
                rtn.append(None)
        return rtn

    def update_bots(self, bot_positions):
        position_dict = {bot.bot_id: pos for bot, pos in zip(self.bots, bot_positions)}
        return [bot.make_move(self.board, position_dict) for bot in self.bots]

    def check_dead(self, old_positions: List[Union[Position, None]], moves: List[Union[Position, None]]) -> List[BotSkeleton]:
        bots_left = []
        new_positions = []
        for bot, old_move, new_move in zip(self.bots, old_positions, moves):
            if new_move is None:
                continue
            delta_move = (new_move[0] - old_move[0], new_move[1] - old_move[1])
            if delta_move not in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                continue
            if not self.board.position_valid(new_move):
                continue
            bots_left.append(bot)
            new_positions.append(new_move)
            self.board[new_move] = bot.bot_id
        return bots_left, new_positions

    def show_board(self):
        if not has_curses:
            return self.show_board_no_curses()
        self.screen.clear()
        for y in range(self.board.y_size):
            for x in range(self.board.x_size):
                self.screen.addstr(" ", curses.color_pair(self.board[y, x]+1))
            self.screen.addstr("\n")
        self.screen.addstr("\n")
        for i, name in enumerate(self.bot_names):
            self.screen.addstr(" ", curses.color_pair(i+2))
            self.screen.addstr(" - ")
            self.screen.addstr(name)
            self.screen.addstr("\n")
        self.screen.refresh()

    def show_board_no_curses(self):
        print(self.board)
        print("---")
