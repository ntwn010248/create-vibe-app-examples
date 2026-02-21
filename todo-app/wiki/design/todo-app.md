# Design: Python Todo Application

## Overview
This design covers a local Python todo app with a CLI. The app stores todos in JSON and supports add, list, complete, and delete operations.

## Goals
- Provide a small, dependency-free todo app using Python standard library.
- Keep business logic testable and independent from CLI parsing.
- Persist todos across runs in a local JSON file.

## Non-Goals
- Multi-user support
- Remote sync or database backend
- GUI or web frontend

## Architecture

### Components
| Component | Responsibility |
|-----------|----------------|
| `TodoService` | Core operations: add, list, complete, delete |
| `TodoStore` | Load/save JSON persistence |
| `cli.py` | Parse command arguments and print output |

### Data Flow
1. User runs CLI command.
2. CLI initializes `TodoStore` and `TodoService`.
3. Service validates inputs and mutates in-memory items.
4. Store persists updated state to disk.
5. CLI prints success or error message.

## Data Model
```python
{
  "id": int,
  "text": str,
  "completed": bool
}
```

## API Design (Internal)
| Function | Description |
|----------|-------------|
| `add_task(text: str) -> dict` | Add a non-empty task |
| `list_tasks() -> list[dict]` | Return all tasks |
| `complete_task(task_id: int) -> dict` | Mark task complete |
| `delete_task(task_id: int) -> dict` | Remove task |

## Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| SQLite backend | Stronger persistence | More complexity for a small app |
| In-memory only | Very simple | No persistence across runs |
| External CLI libs | Better UX | Extra dependency overhead |

## Risks
| Risk | Mitigation |
|------|------------|
| Corrupt JSON file | Fallback to empty list on decode errors |
| Invalid task id handling | Raise clear `ValueError` from service |
