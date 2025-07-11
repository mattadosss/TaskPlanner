const taskdiv = document.getElementById('tasks')
const refreshButton = document.getElementById('refreshButton')
const datebutton = document.getElementById("datebutton")
const undone = document.getElementById("undone")
const upcoming = document.getElementById("upcoming")
const today = document.getElementById("today")
const del_done = document.getElementById("del_done")

function renderTaskList(tasks) {
    taskdiv.replaceChildren();  // Clear the container

    tasks.forEach(task => {
        console.log(task);

        const taskContainer = document.createElement('div');
        taskContainer.classList.add('task');

        //taskContainer.style.cursor = 'pointer';
        //taskContainer.onclick = () => {
        //  loadoneTask(task.Task_ID);
        //};

        const title = document.createElement('h2');
        title.innerText = task.Titel;

        const label = document.createElement("label");
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.name = "erledigt";
        checkbox.id = "erledigt";
        if (task.erledigt === 1) {
            checkbox.checked = true
        }
        checkbox.addEventListener('change', () => {
            if (checkbox.checked === true) {
                const url = `/api_done_task?id=${task.Task_ID}&erledigt=1`;
                let result = fetch(url);
                //let task = result.json();
            } else {
                const url = `/api_done_task?id=${task.Task_ID}&erledigt=0`;
                let result = fetch(url);
            }
        });

        const labelText = document.createTextNode(" Erledigt");
        label.appendChild(checkbox);
        label.appendChild(labelText);

        const description = document.createElement('p');
        description.innerText = `Beschreibung: ${task.Beschreibung}`;

        const datetime = document.createElement('p');
        datetime.innerText = `Datum & Uhrzeit: ${task.DatumUhrzeit}`;

        const deleteButton = document.createElement("button");
        deleteButton.innerText = "Delete Task";

        deleteButton.onclick = async () => {
            const url = `/api_delete_task?id=${task.Task_ID}`;
            try {
                const response = await fetch(url, {method: 'DELETE'});
                if (response.ok) {
                    console.log("Task deleted");
                    loadBlogPost();  // Refresh the task list, assuming this function exists
                } else {
                    console.error("Failed to delete task");
                }
            } catch (error) {
                console.error("Error:", error);
            }
        };
        const updateButton = document.createElement("button");
        updateButton.innerText = "update Task";

        updateButton.onclick = async () => {
            sessionStorage.setItem("Task_to_update_id", task.Task_ID)
            window.location.href = "/update_task"
        };


        taskContainer.appendChild(title);
        taskContainer.appendChild(label);
        taskContainer.appendChild(description);
        taskContainer.appendChild(datetime);
        taskContainer.appendChild(deleteButton)
        taskContainer.appendChild(updateButton)

        taskdiv.appendChild(taskContainer);
    });
}


async function loadBlogPost() {
    const url = "/api_get_tasks";
    let result = await fetch(url);
    let task = await result.json();
    console.log(task)
    renderTaskList(task);
}

async function taskBydate() {
    const url = "/api_get_tasks_by_date";
    let result = await fetch(url);
    let task = await result.json();
    console.log(task)
    renderTaskList(task);
}


async function undone_tasks() {
    const url = `/api_get_undone_tasks`;
    console.log(url)
    let result = await fetch(url);
    let task = await result.json();
    console.log(task)
    renderTaskList(task);
}

async function upcoming_tasks() {
    const url = `/api_upcoming_tasks`;
    console.log(url)
    let result = await fetch(url);
    let task = await result.json();
    console.log(task)
    renderTaskList(task);
}

async function today_tasks() {
    const url = `/api_today_tasks`;
    console.log(url)
    let result = await fetch(url);
    let task = await result.json();
    console.log(task)
    renderTaskList(task);
}

async function delete_done() {
    const confirmed = confirm("Are you sure you want to delete all done tasks?");
    if (!confirmed) {
        return;
    }
    const url = `/api_delete_done_task`;
    console.log(url)
    let result = await fetch(url);
    let task = await result.json();
    console.log(task)
    loadBlogPost()
}


loadBlogPost();
refreshButton.addEventListener('click', loadBlogPost)
datebutton.addEventListener("click", taskBydate)
undone.addEventListener("click", undone_tasks)
upcoming.addEventListener("click", upcoming_tasks)
today.addEventListener("click", today_tasks)
del_done.addEventListener("click", delete_done)
