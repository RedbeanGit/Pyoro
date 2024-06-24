from pyoro.game_engine import GameEngine
from pyoro.game_loop import GameLoop


def main():
    game_engine = GameEngine()
    game_engine.start_splash()

    game_loop = GameLoop.get_instance()
    game_loop.run()


if __name__ == "__main__":
    main()
