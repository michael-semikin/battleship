from abc import ABCMeta, abstractmethod
from collections.abc import Iterable

from src.models.player import Player


class ViewProvider (metaclass=ABCMeta):
   @abstractmethod
   def render(self, player: Player):
      """renders the game state for the given player, including their own board and the tracking board for the enemy
         Args:
            player: the player for whom the game state should be rendered
      """

   @abstractmethod
   def clear_screen(self):
      """contains some logic to refresh screen and /or update rendering"""

   @abstractmethod
   def render_stats(self, data: tuple[tuple[int, int], ...]):
      """renders some statistics, for example, how many ships of each type are alive for each player
         Args:
            data: a tuple of tuples, where each inner tuple contains two integers: the first one is the count of alive ships of a specific type, and the second one is the count of destroyed ships of that type. The order of inner tuples corresponds to the order of ship types (e.g., Battleship, Cruiser, Destroyer, Scout).
      """

   @abstractmethod
   def render_log(self, log: Iterable[str]):
      """renders log entries, each entry is a string"""