# [PATTERN] Python Todo CLI with Service and Store Split

## TL;DR
Separating CLI parsing, business logic, and storage made the todo app easy to test and robust to file errors.

## Problem
A new Python todo app needed CRUD behavior with persistence and test coverage, but the environment had restricted write locations and no external test tools.

## Solution
- Implemented `TodoService` for business rules and `TodoStore` for JSON persistence.
- Kept CLI behavior in `code/cli.py`, with clear success/error messages and non-zero exits for invalid operations.
- Used built-in `unittest` to avoid dependency on `pytest`.
- Adjusted tests to write temporary files inside workspace paths, avoiding sandbox permission failures from system temp paths.

## Code Example
```python
class TodoService:
    def add_task(self, text: str) -> dict:
        normalized_text = text.strip()
        if not normalized_text:
            raise ValueError("Task text must not be empty.")
        task = {"id": self._next_id, "text": normalized_text, "completed": False}
        self._tasks.append(task)
        self._store.save_tasks(self._tasks)
        return task.copy()
```

## Prevention
- Prefer workspace-local temp paths in tests under sandboxed environments.
- Keep storage and domain logic separate so failures are easier to isolate.
- Validate IDs and task text centrally in the service layer.

## Tags
#pattern #python #cli #todo-app #tdd #sandbox
