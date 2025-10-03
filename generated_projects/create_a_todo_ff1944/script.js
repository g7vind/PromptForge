// Get references to DOM elements
const newTodoInput = document.getElementById('new-todo-input');
const addTodoButton = document.getElementById('add-todo-button');
const todoList = document.getElementById('todo-list');

/**
 * Creates a new <li> element for a todo item.
 * @param {string} todoText - The text content for the todo item.
 * @returns {HTMLLIElement} The constructed <li> element.
 */
function createTodoElement(todoText) {
    const listItem = document.createElement('li');

    const todoSpan = document.createElement('span');
    todoSpan.textContent = todoText;

    const completeButton = document.createElement('button');
    completeButton.textContent = 'Complete';
    completeButton.classList.add('complete-button');

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.classList.add('delete-button');

    listItem.appendChild(todoSpan);
    listItem.appendChild(completeButton);
    listItem.appendChild(deleteButton);

    return listItem;
}

/**
 * Handles adding a new todo item to the list.
 * Reads the input field, creates a new todo element, and appends it to the list.
 */
function addTodo() {
    const todoText = newTodoInput.value.trim();
    if (todoText !== '') {
        const newTodoItem = createTodoElement(todoText);
        todoList.appendChild(newTodoItem);
        newTodoInput.value = ''; // Clear the input field
    }
}

/**
 * Handles click events on the todo list using event delegation.
 * Toggles 'completed' class or removes the todo item based on the clicked button.
 * @param {Event} event - The click event object.
 */
function handleTodoActions(event) {
    const target = event.target;

    if (target.classList.contains('complete-button')) {
        // Toggle the 'completed' class on the parent <li> element
        target.parentElement.classList.toggle('completed');
    } else if (target.classList.contains('delete-button')) {
        // Remove the parent <li> element from the DOM
        target.parentElement.remove();
    }
}

// Add event listeners
addTodoButton.addEventListener('click', addTodo);

newTodoInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        addTodo();
    }
});

todoList.addEventListener('click', handleTodoActions);
