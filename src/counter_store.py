from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Dict


class CounterStore:
    """Guild + user based counter storage persisted as JSON."""

    def __init__(self, file_path: str | Path) -> None:
        self._file_path = Path(file_path)
        self._lock = threading.Lock()
        self._counts: Dict[str, int] = {}
        self._load()

    def get(self, guild_id: int, user_id: int) -> int:
        key = self._build_key(guild_id, user_id)
        with self._lock:
            return self._counts.get(key, 0)

    def increment(self, guild_id: int, user_id: int) -> int:
        key = self._build_key(guild_id, user_id)
        with self._lock:
            next_value = self._counts.get(key, 0) + 1
            self._counts[key] = next_value
            self._save_unlocked()
            return next_value

    @staticmethod
    def _build_key(guild_id: int, user_id: int) -> str:
        return f"{guild_id}:{user_id}"

    def _load(self) -> None:
        if not self._file_path.exists():
            self._counts = {}
            return

        with self._file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError("counts.json must contain a JSON object")

        parsed: Dict[str, int] = {}
        for key, value in data.items():
            if not isinstance(key, str) or not isinstance(value, int):
                raise ValueError("counts.json has invalid key/value types")
            parsed[key] = value

        self._counts = parsed

    def _save_unlocked(self) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        with self._file_path.open("w", encoding="utf-8") as f:
            json.dump(self._counts, f, ensure_ascii=False, indent=2)
