const form = document.querySelector('.create-form')
const dialog = document.getElementById('new-modal')
const dialogTitle = dialog.querySelector('h2')

function createTask() {
    form.reset()
    dialogTitle.innerText = 'New To-do'
    dialog.showModal()
}

