// Todo App - Main Application Logic

class TodoApp {
    constructor() {
        this.todos = this.loadTodos();
        this.form = document.getElementById('todo-form');
        this.input = document.getElementById('todo-input');
        this.list = document.getElementById('todo-list');
        this.footer = document.getElementById('footer');
        this.countEl = document.getElementById('todo-count');
        this.clearBtn = document.getElementById('clear-completed');

        this.bindEvents();
        this.render();
    }

    // Generate unique ID
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    // Load todos from localStorage
    loadTodos() {
        const data = localStorage.getItem('todos');
        return data ? JSON.parse(data) : [];
    }

    // Save todos to localStorage
    saveTodos() {
        localStorage.setItem('todos', JSON.stringify(this.todos));
    }

    // Add new todo
    addTodo(text) {
        const todo = {
            id: this.generateId(),
            text: text.trim(),
            completed: false,
            createdAt: Date.now()
        };
        this.todos.unshift(todo);
        this.saveTodos();
        this.render();
    }

    // Toggle todo completion
    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.completed = !todo.completed;
            this.saveTodos();
            this.render();
        }
    }

    // Delete todo
    deleteTodo(id) {
        this.todos = this.todos.filter(t => t.id !== id);
        this.saveTodos();
        this.render();
    }

    // Clear completed todos
    clearCompleted() {
        this.todos = this.todos.filter(t => !t.completed);
        this.saveTodos();
        this.render();
    }

    // Bind event listeners
    bindEvents() {
        // Form submit
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            const text = this.input.value.trim();
            if (text) {
                this.addTodo(text);
                this.input.value = '';
            }
        });

        // Clear completed
        this.clearBtn.addEventListener('click', () => {
            this.clearCompleted();
        });

        // Delegate events for todo items
        this.list.addEventListener('click', (e) => {
            const item = e.target.closest('.todo-item');
            if (!item) return;

            const id = item.dataset.id;

            if (e.target.classList.contains('todo-checkbox')) {
                this.toggleTodo(id);
            } else if (e.target.classList.contains('delete-btn')) {
                this.deleteTodo(id);
            }
        });
    }

    // Render todos
    render() {
        // Render list
        if (this.todos.length === 0) {
            this.list.innerHTML = `
                <li class="empty-state">
                    No todos yet. Add one above!
                </li>
            `;
        } else {
            this.list.innerHTML = this.todos.map(todo => `
                <li class="todo-item ${todo.completed ? 'completed' : ''}" data-id="${todo.id}">
                    <div class="todo-checkbox"></div>
                    <span class="todo-text">${this.escapeHtml(todo.text)}</span>
                    <button class="delete-btn" title="Delete">×</button>
                </li>
            `).join('');
        }

        // Update footer
        const activeCount = this.todos.filter(t => !t.completed).length;
        const completedCount = this.todos.filter(t => t.completed).length;

        this.countEl.textContent = `${activeCount} item${activeCount !== 1 ? 's' : ''} left`;
        this.footer.classList.toggle('hidden', this.todos.length === 0);
        this.clearBtn.style.display = completedCount > 0 ? 'block' : 'none';
    }

    // Escape HTML to prevent XSS
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    new TodoApp();
});
