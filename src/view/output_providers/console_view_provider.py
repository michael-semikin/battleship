   
from typing import Iterable

from src.models.board import Board, Point
from src.models.common import BOARD_SIZE, CellState, ShipType
from src.models.player import Player
from src.view.output_providers.view_provider import ViewProvider


class ConsoleViewProvider(ViewProvider):
    _SYMBOLS = {
        CellState.EMPTY: "░",
        CellState.SHIP:  "█", 
        CellState.HIT:   "🔥", 
        CellState.MISS:  "💦"
    }
    
    _TOP_LEFT_EDGE, _TOP_RIGHT_EDGE = "\u250c", "\u2510"  # ┌, ┐
    _BOTTOM_LEFT_EDGE, _BOTTOM_RIGHT_EDGE = "\u2514", "\u2518"  # └, ┘

    _HORIZONTAL_LINE, _VERTICAL_LINE   = "\u2500", "\u2502"  # ─, │

    def render(self, player: Player):
        size = BOARD_SIZE
        
        # Вспомогательная функция для сборки одной строки любой доски
        def get_row_content(board_to_render: Board, row_idx: int) -> str:
            cells_view = ""
            for col_idx in range(size):
                state = board_to_render[Point(row_idx, col_idx)]
                match state:
                    case CellState.HIT | CellState.MISS:
                        cells_view += f"\033[44m{self._SYMBOLS[state]}\033[0m"
                    case CellState.SHIP:
                        cells_view += f"\033[91m{self._SYMBOLS[state] * 2}\033[0m"
                    case CellState.EMPTY:
                        cells_view += f"\033[44m{self._SYMBOLS[state] * 2}\033[0m"
                    case _ :
                        raise ValueError(f"No case for {state} value")

            return f"{row_idx:2} {self._VERTICAL_LINE}{cells_view}{self._VERTICAL_LINE}"

        # header with column letters
        letters_row = " ".join([chr(97 + i) for i in range(size)])

        print(f"\n{' ' * 7}[ {player.name} ]{' ' * 22}[ ENEMY BOARD ]")
        print(f"{' ' * 5}{letters_row}{' ' * 17}{letters_row}")

        # top frame for both boards
        h_line = self._HORIZONTAL_LINE * (size * 2)
        edge_line = f"   {self._TOP_LEFT_EDGE}{h_line}{self._TOP_RIGHT_EDGE}"

        print(f"{edge_line}           {edge_line}")

        # board rows
        for row_idx in range(size):
            own_line = get_row_content(player.board, row_idx)
            radar_line = get_row_content(player.tracking_board, row_idx)
            
            print(f"{own_line}           {radar_line}")

        # bottom frame for both boards
        bottom_edge = f"   {self._BOTTOM_LEFT_EDGE}{h_line}{self._BOTTOM_RIGHT_EDGE}"
        print(f"{bottom_edge}           {bottom_edge}")

    def render_stats(self, data: tuple[tuple[int, int], ...]):
        stats_start_column = BOARD_SIZE * 6 + 5
        self.print_at(BOARD_SIZE * 9 + 4, 1, "[ STATS ]")
        self.print_at(BOARD_SIZE * 8, 2, "[ My Afloat ]")
        self.print_at(BOARD_SIZE * 9 + 13, 2, "[ Enemy Killed ]")
        for idx, (ship, count) in enumerate(zip(ShipType, data)):
            self.print_at(stats_start_column, 3 + idx, f"{ship.description:10}: {count[0]:10} {count[1]:23}")

        self.print_at(0, BOARD_SIZE + 5)

    def render_log(self, log: Iterable[str]):
        for log_entry in log:
            print(log_entry)


    def clear_screen(self):
        print("\033c", end="")
        
    def print_at(self, column: int, row: int, text: str = ""):
        print(f"\033[{row + 1};{column + 1}H{text}", end="")
