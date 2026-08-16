const API_URL = "http://127.0.0.1:8000";
const TASKS_CACHE_KEY = "tasks";

const taskForm = document.getElementById("task-form");
const taskList = document.getElementById("task-list");

const titleInput = document.getElementById("title");
const titleError = document.getElementById("title-error");


// ==========================================
// AI ELEMENTS
// ==========================================

const aiForm = document.getElementById("ai-form");
const aiMessage = document.getElementById("ai-message");
const aiButton = document.getElementById("ai-button");
const aiLoading = document.getElementById("ai-loading");
const aiError = document.getElementById("ai-error");
const aiResponse = document.getElementById("ai-response");


// ==========================================
// TITLE VALIDATION - REMOVE ERROR ON INPUT
// ==========================================

titleInput.addEventListener("input", () => {
    if (titleInput.value.trim() !== "") {
        titleError.textContent = "";
    }
});


// ==========================================
// LOAD TASKS
// ==========================================

async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks`);

        if (!response.ok) {
            throw new Error("Failed to load tasks");
        }

        const tasks = await response.json();

        renderTasks(tasks);

    } catch (error) {
        console.error(error);

        // Keep cached tasks visible if available
        if (!localStorage.getItem(TASKS_CACHE_KEY)) {
            taskList.replaceChildren();

            const errorMessage = document.createElement("p");
            errorMessage.textContent = "Unable to load tasks.";

            taskList.appendChild(errorMessage);
        }
    }
}


// ==========================================
// RENDER TASKS
// ==========================================

function renderTasks(tasks) {

    // Cache current task list as JSON
    localStorage.setItem(
        TASKS_CACHE_KEY,
        JSON.stringify(tasks)
    );

    taskList.replaceChildren();

    if (tasks.length === 0) {
        const emptyMessage = document.createElement("p");
        emptyMessage.textContent = "No tasks found.";

        taskList.appendChild(emptyMessage);

        return;
    }

    tasks.forEach(task => {

        // ==================================
        // MAIN TASK CONTAINER
        // ==================================

        const taskElement = document.createElement("div");
        taskElement.className = "task-item";


        // ==================================
        // TASK TITLE
        // ==================================

        const titleElement = document.createElement("h3");
        titleElement.textContent = task.title;


        // ==================================
        // PRIORITY
        // ==================================

        const priorityElement = document.createElement("p");

        const priorityLabel = document.createElement("strong");
        priorityLabel.textContent = "Priority: ";

        priorityElement.appendChild(priorityLabel);

        priorityElement.appendChild(
            document.createTextNode(task.priority)
        );


        // ==================================
        // DUE DATE
        // ==================================

        const dueDateElement = document.createElement("p");

        const dueDateLabel = document.createElement("strong");
        dueDateLabel.textContent = "Due Date: ";

        dueDateElement.appendChild(dueDateLabel);

        dueDateElement.appendChild(
            document.createTextNode(task.due_date || "Not set")
        );


        // ==================================
        // EDIT BUTTON
        // ==================================

        const editButton = document.createElement("button");

        editButton.type = "button";
        editButton.textContent = "Edit";

        editButton.addEventListener("click", () => {
            editTask(task);
        });


        // ==================================
        // DELETE BUTTON
        // ==================================

        const deleteButton = document.createElement("button");

        deleteButton.type = "button";
        deleteButton.textContent = "Delete";

        deleteButton.addEventListener("click", () => {
            deleteTask(task.id);
        });


        // ==================================
        // BUTTON CONTAINER
        // ==================================

        const buttonContainer = document.createElement("div");

        buttonContainer.className = "task-actions";

        buttonContainer.appendChild(editButton);
        buttonContainer.appendChild(deleteButton);


        // ==================================
        // ADD EVERYTHING TO TASK
        // ==================================

        taskElement.appendChild(titleElement);
        taskElement.appendChild(priorityElement);
        taskElement.appendChild(dueDateElement);
        taskElement.appendChild(buttonContainer);


        // Add task to list
        taskList.appendChild(taskElement);
    });
}


// ==========================================
// ADD TASK
// ==========================================

taskForm.addEventListener("submit", async (event) => {

    // Prevent normal form submission
    event.preventDefault();


    // ==================================
    // TITLE VALIDATION
    // ==================================

    if (titleInput.value.trim() === "") {
        titleError.textContent = "Task title is required.";
        titleInput.focus();
        return;
    }

    titleError.textContent = "";


    const priorityInput = document.getElementById("priority");
    const dueDateInput = document.getElementById("due-date");


    const newTask = {
        project_id: 1,
        title: titleInput.value.trim(),
        priority: priorityInput.value.trim().toLowerCase(),
        due_date: dueDateInput.value
    };


    // Check all fields
    if (!newTask.title || !newTask.priority || !newTask.due_date) {
        alert("Please fill in all fields.");
        return;
    }


    // Validate priority
    if (!["low", "medium", "high"].includes(newTask.priority)) {
        alert("Priority must be low, medium, or high.");
        return;
    }


    try {

        const response = await fetch(`${API_URL}/tasks`, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(newTask)
        });


        if (!response.ok) {
            throw new Error("Failed to create task");
        }


        // Clear form
        taskForm.reset();

        // Clear validation error
        titleError.textContent = "";


        // Refresh task list and update cache
        await loadTasks();


    } catch (error) {

        console.error(error);

        alert("Unable to create task.");
    }
});


// ==========================================
// EDIT TASK
// ==========================================

async function editTask(task) {

    const newTitle = prompt(
        "Enter new task title:",
        task.title
    );


    if (newTitle === null) {
        return;
    }


    const newPriority = prompt(
        "Enter new priority:",
        task.priority
    );


    if (newPriority === null) {
        return;
    }


    const newDueDate = prompt(
        "Enter new due date (YYYY-MM-DD):",
        task.due_date || ""
    );


    if (newDueDate === null) {
        return;
    }


    const updatedTask = {
        project_id: task.project_id,
        title: newTitle.trim(),
        priority: newPriority.trim().toLowerCase(),
        due_date: newDueDate
    };


    // Validate edited task
    if (
        !updatedTask.title ||
        !updatedTask.priority ||
        !updatedTask.due_date
    ) {
        alert("All fields are required.");
        return;
    }


    if (!["low", "medium", "high"].includes(updatedTask.priority)) {
        alert("Priority must be low, medium, or high.");
        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/tasks/${task.id}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(updatedTask)
            }
        );


        if (!response.ok) {
            throw new Error("Failed to update task");
        }


        // Refresh task list and update cache
        await loadTasks();


    } catch (error) {

        console.error(error);

        alert("Unable to update task.");
    }
}


// ==========================================
// DELETE TASK
// ==========================================

async function deleteTask(taskId) {

    const confirmed = confirm(
        "Are you sure you want to delete this task?"
    );


    if (!confirmed) {
        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/tasks/${taskId}`,
            {
                method: "DELETE"
            }
        );


        if (!response.ok) {
            throw new Error("Failed to delete task");
        }


        // Refresh task list and update cache
        await loadTasks();


    } catch (error) {

        console.error(error);

        alert("Unable to delete task.");
    }
}


// ==========================================
// TASKFLOW AI
// ==========================================

aiForm.addEventListener("submit", async (event) => {

    event.preventDefault();


    const message = aiMessage.value.trim();


    // ==================================
    // VALIDATION
    // ==================================

    if (!message) {

        aiError.textContent =
            "Please enter a message.";

        aiMessage.focus();

        return;
    }


    // Clear previous response/error
    aiError.textContent = "";
    aiResponse.textContent = "";
    aiLoading.hidden = false;
    aiButton.disabled = true;


    try {

        const response = await fetch(
            `${API_URL}/ai/chat`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "AI request failed"
            );
        }


        // Display AI response safely
        aiResponse.textContent =
            data.message || "No response received.";


    } catch (error) {

        console.error("AI ERROR:", error);

        aiError.textContent =
            "Unable to connect to TaskFlow AI. " +
            error.message;


    } finally {

        aiLoading.hidden = true;
        aiButton.disabled = false;
    }
});


// ==========================================
// INITIAL LOAD
// ==========================================

// Get cached tasks first
const cachedTasks =
    localStorage.getItem(TASKS_CACHE_KEY);

if (cachedTasks) {

    try {

        // Convert JSON string back into array
        const tasks = JSON.parse(cachedTasks);

        // Render cached tasks immediately
        renderTasks(tasks);

    } catch (error) {

        console.error(
            "Invalid cached tasks:",
            error
        );

        localStorage.removeItem(
            TASKS_CACHE_KEY
        );
    }
}


// ==========================================
// LOAD FRESH TASKS FROM BACKEND
// ==========================================

loadTasks();