from collections import deque
from dataclasses import dataclass
from datetime import datetime

from src.models.turn import Turn


@dataclass(frozen=True)
class LogEntry:
    message: str
    turn: Turn
    date: datetime

class GameLogger:
    def __init__(self, maxsize = 15) -> None:
        self._logs = deque(maxlen=maxsize)

    def log(self, msg: str, turn: Turn):
        self._logs.append(LogEntry(msg, turn, datetime.now()))

    def get_logs(self)-> list[LogEntry]:
        return list(self._logs)