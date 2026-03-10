from src.logic.engine import GameEngine
from src.view.console.view_provider import ConsoleViewProvider


def main():
    game = GameEngine(ConsoleViewProvider())
    game.init_game()
    game.play()

if __name__ == "__main__":
    main()