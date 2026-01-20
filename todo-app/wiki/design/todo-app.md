# Design: Todo Web Application

## Overview
A simple, elegant todo application with CRUD operations and local persistence.

## Architecture

### Component Structure
```
index.html          - Main HTML structure
├── styles.css      - Styling
└── app.js          - Application logic
    ├── TodoApp     - Main application class
    ├── Storage     - localStorage wrapper
    └── UI          - DOM manipulation
```

### Data Model
```javascript
{
  id: string,       // unique identifier
  text: string,     // todo content
  completed: boolean,
  createdAt: number // timestamp
}
```

### API (Internal)
| Function | Description |
|----------|-------------|
| `addTodo(text)` | Add new todo |
| `toggleTodo(id)` | Toggle completion |
| `deleteTodo(id)` | Remove todo |
| `getTodos()` | Get all todos |
| `saveTodos()` | Persist to localStorage |

## UI Design
- Clean, minimal interface
- Input field with add button
- Todo list with checkboxes
- Delete button on hover
- Completed todos with strikethrough
- Dark/light theme support

## Tech Decisions
| Decision | Rationale |
|----------|-----------|
| Vanilla JS | Simple, no build step needed |
| localStorage | No backend complexity |
| CSS Variables | Easy theming |
