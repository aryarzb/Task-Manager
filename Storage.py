import json
from pathlib import Path
from typing import Any


class Storage:
    def __init__(self, filename: str = "tasks.json") -> None:
        self.path = Path(filename)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        try:
            text = self.path.read_text(encoding="utf-8")
            data = json.loads(text)
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def save(self, tasks: list[dict[str, Any]]) -> None:
        self.path.write_text(
            json.dumps(tasks, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
