# [PATTERN] Vanilla Todo App Foundation (LocalStorage + Theme State)

## TL;DR
For small web apps, a simple `Storage` wrapper plus a single app controller class keeps behavior clear and persistence reliable without a build step.

## Problem
We needed to build a new todo website quickly with core CRUD behavior, local persistence, and theme support, while keeping codebase complexity low.

## Solution
- Implemented a small `Storage` utility for todos and theme keys.
- Kept UI behavior inside a `TodoApp` class with explicit methods:
  - `addTodo(text)`
  - `toggleTodo(id)`
  - `deleteTodo(id)`
  - `render()`
  - `updateMeta()`
- Used event delegation on the todo list for toggle/delete interactions.
- Persisted data after each state mutation (`saveTodos()`).
- Applied and persisted theme with `data-theme` on `documentElement`.

## Code Example
```javascript
class Storage {
  static TODO_KEY = "flowlist.todos";
  static getTodos() {
    try {
      return JSON.parse(localStorage.getItem(Storage.TODO_KEY) || "[]");
    } catch {
      return [];
    }
  }
  static saveTodos(todos) {
    localStorage.setItem(Storage.TODO_KEY, JSON.stringify(todos));
  }
}
```

## Pitfall
Emoji characters in source text can become corrupted in constrained shell encoding environments, which can break JavaScript string literals.

## Prevention
- Prefer ASCII-safe UI labels in source when shell/file encoding is uncertain.
- Run a syntax check after edits (`node --check code/app.js`).
- Keep display decoration in CSS where possible.

## Tags
#pattern #localstorage #vanilla-js #todo-app #theme #encoding
