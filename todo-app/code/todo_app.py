from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class TodoStore:
    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    def load_tasks(self) -> list[dict[str, Any]]:
        if not self.file_path.exists():
            return []

        try:
            content = json.loads(self.file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []

        if not isinstance(content, list):
            return []

        normalized: list[dict[str, Any]] = []
        for item in content:
            if not isinstance(item, dict):
                continue
            if not isinstance(item.get("id"), int):
                continue
            if not isinstance(item.get("text"), str):
                continue
            if not isinstance(item.get("completed"), bool):
                continue

            normalized.append(
                {
                    "id": item["id"],
                    "text": item["text"],
                    "completed": item["completed"],
                }
            )
        return normalized

    def save_tasks(self, tasks: list[dict[str, Any]]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(tasks, ensure_ascii=True, indent=2)
        self.file_path.write_text(payload, encoding="utf-8")


class TodoService:
    def __init__(self, store: TodoStore) -> None:
        self._store = store
        self._tasks = store.load_tasks()
        self._next_id = self._compute_next_id()

    def list_tasks(self) -> list[dict[str, Any]]:
        return [task.copy() for task in self._tasks]

    def add_task(self, text: str) -> dict[str, Any]:
        normalized_text = text.strip()
        if not normalized_text:
            raise ValueError("Task text must not be empty.")

        task = {
            "id": self._next_id,
            "text": normalized_text,
            "completed": False,
        }
        self._next_id += 1
        self._tasks.append(task)
        self._store.save_tasks(self._tasks)
        return task.copy()

    def complete_task(self, task_id: int) -> dict[str, Any]:
        task = self._find_task(task_id)
        task["completed"] = True
        self._store.save_tasks(self._tasks)
        return task.copy()

    def delete_task(self, task_id: int) -> dict[str, Any]:
        self._validate_task_id(task_id)
        for index, task in enumerate(self._tasks):
            if task["id"] == task_id:
                removed = self._tasks.pop(index)
                self._store.save_tasks(self._tasks)
                return removed.copy()

        raise ValueError(f"Task with id {task_id} does not exist.")

    def _compute_next_id(self) -> int:
        if not self._tasks:
            return 1
        return max(task["id"] for task in self._tasks) + 1

    def _find_task(self, task_id: int) -> dict[str, Any]:
        self._validate_task_id(task_id)
        for task in self._tasks:
            if task["id"] == task_id:
                return task
        raise ValueError(f"Task with id {task_id} does not exist.")

    def _validate_task_id(self, task_id: int) -> None:
        if isinstance(task_id, bool) or not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task id must be a positive integer.")
