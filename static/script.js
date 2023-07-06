const form = document.querySelector('.create-form')
const dialog = document.getElementById('new-modal')
const dialogTitle = dialog.querySelector('h2')
const listEl = document.getElementById('task-list')

function createTask() {
    form.reset()
    dialogTitle.innerText = 'New To-do'
    dialog.showModal()
}

async function refreshTodos() {
    const todos = await fetch('/todos').then(x => x.json())
        .catch(() => alert('Unable to refresh tasks'))
    if (!todos) return

    const template = document.getElementById('todo-template')
    listEl.innerHTML = ''
    todos.forEach(todo => {
        const element = template.content.children[0].cloneNode(true)
        const [nameEl, descEl, editBtn, delBtn] = element.children
        element.id += todo.key
        nameEl.innerText = todo.key
        descEl.innerText = todo.desc
        editBtn.dataset.key = delBtn.dataset.key = todo.key
        listEl.appendChild(element)
    })
}

function setButtonState(disable) {
    [...form.elements, document.querySelector('.popup .close')]
        .forEach(btn => { btn.disabled = disable })
}

form.addEventListener('submit', async e => {
    e.preventDefault()
    const data = Object.fromEntries(new FormData(form))
    const path = data.old_key ? '/edit' : '/create'
    setButtonState(true)
    fetch(path, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {'Content-Type': 'application/json'}
    }).then(async () => {
        // Request succeeded
        await refreshTodos()
        setButtonState(false)
        dialog.close()
    }).catch(() => {
        // Request failed
        alert('Could not save todo')
        setButtonState(false)
    })
})

function editTask(key) {
    const todo = document.getElementById('t-' + key)
    form.elements.old_key.value = key
    form.elements.name.value = key
    form.elements.desc.value = todo.querySelector('.todo-desc').innerText
    dialogTitle.innerText = 'Edit To-do'
    dialog.showModal()
}

document.body.addEventListener('click', e => {
    if (e.target.matches('.edit')) return editTask(e.target.dataset.key)
})
