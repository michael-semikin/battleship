from abc import ABCMeta, abstractmethod

from src.models.players import Player


class ViewProvider (metaclass=ABCMeta):
    @abstractmethod
    def render(self, player: Player):
       pass
   
    @abstractmethod
    def clear_screen(self):
       """contains some logic to refresh screen and /or update rendering"""

    def render_stats(self, data: tuple[tuple[int, int], ...]):
       pass
