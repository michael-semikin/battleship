from src.logic.desktop_engine import DesktopGameEngine
from src.view.input_providers.console_input_provider import ConsoleInputProvider
from src.view.input_providers.hunter_input_provider import HunterInputProvider
from src.view.output_providers.console_view_provider import ConsoleViewProvider



def main():
    game = DesktopGameEngine(ConsoleViewProvider())
    game.init_game(ConsoleInputProvider(), HunterInputProvider())
    game.play()

if __name__ == "__main__":
    main()