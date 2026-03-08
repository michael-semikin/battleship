from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logic.fire import Visitor
    from models.board import Point

class Acceptor(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor: Visitor, point: Point | None = None):
        pass