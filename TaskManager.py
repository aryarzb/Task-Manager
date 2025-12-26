from typing import Optional, List
from dataclasses import dataclass
import Time
from Storage import Storage
from dataclasses import asdict


@dataclass
class Task:
    id: int
    title: str
    status: str = "pending"
    note: Optional[str] = None
    due_at: Optional[str] = None
    remind_at: Optional[str] = None
    reminded: bool = False


class TaskManager:
    def __init__(self, storage: Storage | None = None) -> None:
            self._storage = storage or Storage("tasks.json")
            self._tasks: List[Task] = []
            self._next_id: int = 1
            self._load()

    def add_task(self, title: str, note: Optional[str] = None) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("title cannot be empty")

        task = Task(id=self._next_id, title=title, status="pending", note=note)
        self._tasks.append(task)
        self._next_id += 1
        self._save()
        return task

    def list_tasks(self, status: Optional[str] = None) -> List[Task]:
        if status is None:
            return list(self._tasks)

        status = status.strip().lower()
        if status not in ("pending", "done"):
            raise ValueError("status must be 'pending' or 'done'")

        return [t for t in self._tasks if t.status == status]

    def get_task(self, task_id: int) -> Optional[Task]:
        for t in self._tasks:
            if t.id == task_id:
                return t
        return None

    def _set_status(self, task_id: int, status: str) -> bool:
        t = self.get_task(task_id)
        if t is None:
            return False
        t.status = status
        self._save()
        return True

    def mark_done(self, task_id: int) -> bool:
        return self._set_status(task_id, "done")

    def mark_pending(self, task_id: int) -> bool:
        return self._set_status(task_id, "pending")

    def delete_task(self, task_id: int) -> bool:
        before = len(self._tasks)
        self._tasks = [t for t in self._tasks if t.id != task_id]
        self._save()
        return len(self._tasks) != before


    def set_due(self, task_id: int, due_iso: str | None) -> bool:
        t = self.get_task(task_id)
        if t is None:
            return False
        t.due_at = due_iso
        self._save()
        return True

    def set_reminder(self, task_id: int, remind_iso: str | None) -> bool:
        t = self.get_task(task_id)
        if t is None:
            return False
        t.remind_at = remind_iso
        t.reminded = False
        self._save()
        return True

    def set_timer_minutes(self, task_id: int, minutes: int) -> bool:
        if minutes <= 0:
            return False
        t = self.get_task(task_id)
        if t is None:
            return False

        remind_dt = Time.minutes_from_now(minutes)
        t.remind_at = Time.to_iso(remind_dt)
        t.reminded = False
        self._save()
        return True

    def get_due_reminders(self) -> List[Task]:
        result: List[Task] = []
        for t in self._tasks:
            if t.remind_at is None:
                continue
            if t.reminded:
                continue
            if Time.is_reached(t.remind_at):
                result.append(t)
        return result

    def mark_reminded(self, task_id: int) -> bool:
        t = self.get_task(task_id)
        if t is None:
            return False
        t.reminded = True
        self._save()
        return True

    def _load(self) -> None:
        raw = self._storage.load()
        self._tasks = []
        max_id = 0

        for item in raw:
            t = Task(
                id=int(item.get("id", 0)),
                title=str(item.get("title", "")).strip(),
                status=str(item.get("status", "pending")),
                note=item.get("note"),
                due_at=item.get("due_at"),
                remind_at=item.get("remind_at"),
                reminded=bool(item.get("reminded", False)),
            )
            if t.id > 0 and t.title:
                self._tasks.append(t)
                max_id = max(max_id, t.id)

        self._next_id = max_id + 1

    def _save(self) -> None:
        self._storage.save([asdict(t) for t in self._tasks])
