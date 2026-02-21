import json
import sys
import unittest
from pathlib import Path


CODE_DIR = Path(__file__).resolve().parents[1]
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from todo_app import TodoService, TodoStore  # noqa: E402


class TodoServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store_path = Path(__file__).resolve().parent / "test-todos.json"
        if self.store_path.exists():
            self.store_path.unlink()
        self.service = TodoService(TodoStore(self.store_path))

    def tearDown(self) -> None:
        if self.store_path.exists():
            self.store_path.unlink()

    def test_add_task_creates_pending_task(self) -> None:
        task = self.service.add_task("Buy milk")

        self.assertEqual(task["id"], 1)
        self.assertEqual(task["text"], "Buy milk")
        self.assertFalse(task["completed"])
        self.assertEqual(len(self.service.list_tasks()), 1)

    def test_add_task_rejects_empty_text(self) -> None:
        with self.assertRaises(ValueError):
            self.service.add_task("   ")

    def test_complete_task_marks_task_done(self) -> None:
        task = self.service.add_task("Write tests")
        updated = self.service.complete_task(task["id"])

        self.assertTrue(updated["completed"])
        self.assertTrue(self.service.list_tasks()[0]["completed"])

    def test_complete_task_unknown_id_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.service.complete_task(99)

    def test_delete_task_removes_item(self) -> None:
        task = self.service.add_task("Delete me")
        removed = self.service.delete_task(task["id"])

        self.assertEqual(removed["id"], task["id"])
        self.assertEqual(self.service.list_tasks(), [])

    def test_delete_task_unknown_id_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.service.delete_task(7)

    def test_tasks_persist_between_instances(self) -> None:
        self.service.add_task("Persisted")

        reloaded = TodoService(TodoStore(self.store_path))
        tasks = reloaded.list_tasks()

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["text"], "Persisted")

    def test_corrupt_json_file_is_handled_as_empty(self) -> None:
        self.store_path.write_text("{bad json", encoding="utf-8")

        reloaded = TodoService(TodoStore(self.store_path))

        self.assertEqual(reloaded.list_tasks(), [])

    def test_store_writes_json_array(self) -> None:
        self.service.add_task("One")
        raw = json.loads(self.store_path.read_text(encoding="utf-8"))

        self.assertIsInstance(raw, list)
        self.assertEqual(raw[0]["text"], "One")


if __name__ == "__main__":
    unittest.main()
