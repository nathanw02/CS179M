function handleUpload() {
    var fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.txt';

    fileInput.click();

    fileInput.addEventListener('change', function () {
        var file = fileInput.files[0];


        var formData = new FormData();
        formData.append('file', file);

        fetch('/manifest', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            document.getElementById('upload-btn').style.display = 'none';
            document.getElementById('action-btns').classList.remove('d-none');
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}

function showLoginForm() {
    document.getElementById('loginModal').style.display = 'flex';
}

async function submitLoginForm() {
    var name = document.getElementById('name').value;

    formData = new FormData();
    formData.append('name', name);
    await fetch('/login', {
        method: 'POST',
        body: formData
    });

    document.getElementById('current-user').textContent = 'Current user: ' + name;
    document.getElementById('loginModal').style.display = 'none';
}

function redirectToLoadPage() {
    window.location.href = '/load';
}