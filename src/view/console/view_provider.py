   
from src.models.board import Board, Point
from src.models.players import Player
from src.models.ship import CellState, ShipType
from src.view.view_provider import ViewProvider


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
        size = Board.BOX_SIZE
        
        # Вспомогательная функция для сборки одной строки любой доски
        def get_row_content(board_to_render: Board, row_idx: int, hide_ships: bool) -> str:
            cells_view = ""
            for col_idx in range(size):
                state = board_to_render[Point(row_idx, col_idx)]
                # Fog of War: если hide_ships=True, заменяем SHIP на EMPTY
                visible_state = state if not (hide_ships and state == CellState.SHIP) else CellState.EMPTY
                if visible_state in (CellState.HIT, CellState.MISS):
                    cells_view += self._SYMBOLS[visible_state]
                else:
                    cells_view += self._SYMBOLS[visible_state] * 2

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
        for r in range(size):
            own_line = get_row_content(player.board, r, hide_ships=False)
            radar_line = get_row_content(player.tracking_board, r, hide_ships=True)
            
            # Печать с 11 пробелами между вертикальными линиями
            print(f"{own_line}           {radar_line}")

        # bottom frame for both boards
        bottom_edge = f"   {self._BOTTOM_LEFT_EDGE}{h_line}{self._BOTTOM_RIGHT_EDGE}"
        print(f"{bottom_edge}           {bottom_edge}")

    def render_stats(self, data: tuple[tuple[int, int], ...]):
        stats_start_column = Board.BOX_SIZE * 6 + 5
        self.print_at(Board.BOX_SIZE * 9 + 4, 1, "[ STATS ]")
        self.print_at(Board.BOX_SIZE * 8, 2, "[ My Afloat ]")
        self.print_at(Board.BOX_SIZE * 9 + 13, 2, "[ Enemy Killed ]")
        for idx, (ship, count) in enumerate(zip(ShipType, data)):
            self.print_at(stats_start_column, 3 + idx, f"{ship.description:10}: {count[0]:10} {count[1]:23}")

        self.print_at(0, Board.BOX_SIZE + 5)




    def clear_screen(self):
        print("\033c", end="")
        
    def print_at(self, column: int, row: int, text: str = ""):
        print(f"\033[{row + 1};{column + 1}H{text}", end="")
