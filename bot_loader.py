import importlib
import os
import glob
import random

import bot_skeleton
import bots


class NotEnoughBotsError(Exception):
    pass


class BotNotFoundError(Exception):
    pass


def load_bots(no_bots, allow_duplicates=False):
    names = get_bot_names()
    if len(names) < no_bots:
        if not allow_duplicates:
            raise NotEnoughBotsError("Tried to load {} bots but could only find {}".format(no_bots, len(names)))
        duplicates_required = no_bots - len(names)
        duplicates = [random.choice(names) for _ in range(duplicates_required)]
        names.extend(duplicates)
    else:
        random.shuffle(names)
        names = names[:4]
    bot_modules = import_bots(names)
    bot_classes = [find_bot(bot_module) for bot_module in bot_modules]
    return bot_classes


def find_bot(module):
    for value in module.__dict__.values():
        try:
            if issubclass(value, bot_skeleton.BotSkeleton):
                if value is not bot_skeleton.BotSkeleton:
                    return value
        except TypeError:
            pass
    raise BotNotFoundError("A class in the module that inherits from BotSkeleton was not found in {}".format(module))


def import_bots(bot_names):
    return [importlib.import_module("bots."+bot_name, "bots") for bot_name in bot_names]


def get_bot_names():
    rtn = []
    for name in glob.glob(os.path.join("bots", "*.py")):
        if name.endswith("__init__.py"):
            continue
        rtn.append(os.path.basename(name)[:-3])
    return rtn
