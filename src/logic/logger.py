from collections import deque
from dataclasses import dataclass
from datetime import datetime

from src.models.turn import Turn


@dataclass(frozen=True)
class LogEntry:
    message: str
    date: datetime
    turn: Turn | None = None

class GameLogger:
    def __init__(self, maxsize = 15) -> None:
        self._logs: deque[LogEntry] = deque(maxlen=maxsize)

    def log(self, msg: str, turn: Turn | None = None):
        self._logs.append(LogEntry(msg, datetime.now(), turn))

    def get_logs(self)-> list[LogEntry]:
        return list(self._logs)