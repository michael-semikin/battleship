
from logic.engine import GameEngine
from view.view_provider import ConsoleViewProvider


def main():
    game = GameEngine(ConsoleViewProvider())
    game.init_game()
    game.play()


if __name__ == "__main__":
    main()

