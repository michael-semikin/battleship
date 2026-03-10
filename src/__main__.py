from src.logic.engine import GameEngine
from src.view.output_providers.console_view_provider import ConsoleViewProvider


def main():
    game = GameEngine(ConsoleViewProvider())
    game.init_game()
    game.play()

if __name__ == "__main__":
    main()