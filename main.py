if __name__ == "__main__":
    import bot_loader
    import game

    bots = bot_loader.load_bots(no_bots=4, allow_duplicates=True)

    game.Game(bots)
