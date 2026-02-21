from __future__ import annotations

import argparse
import sys
from pathlib import Path

from todo_app import TodoService, TodoStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple Python todo app")
    parser.add_argument(
        "--file",
        default=str(Path.cwd() / "todos.json"),
        help="Path to the JSON file used for persistence.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task.")
    add_parser.add_argument("text", help="Task text.")

    subparsers.add_parser("list", help="List all tasks.")

    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed.")
    complete_parser.add_argument("task_id", type=int, help="Task id.")

    delete_parser = subparsers.add_parser("delete", help="Delete a task.")
    delete_parser.add_argument("task_id", type=int, help="Task id.")

    return parser


def format_task(task: dict) -> str:
    status = "x" if task["completed"] else " "
    return f"[{status}] {task['id']}: {task['text']}"


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    service = TodoService(TodoStore(args.file))

    try:
        if args.command == "add":
            task = service.add_task(args.text)
            print(f"Added task {task['id']}: {task['text']}")
            return 0

        if args.command == "list":
            tasks = service.list_tasks()
            if not tasks:
                print("No tasks found.")
                return 0
            for task in tasks:
                print(format_task(task))
            return 0

        if args.command == "complete":
            task = service.complete_task(args.task_id)
            print(f"Completed task {task['id']}.")
            return 0

        if args.command == "delete":
            task = service.delete_task(args.task_id)
            print(f"Deleted task {task['id']}.")
            return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
