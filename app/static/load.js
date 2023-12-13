let selectedCells = [];
let toLoad = [];

function handleCellClick(cellId, cellName) {
    if (cellName !== 'NAN' && cellName !== 'UNUSED') {
        const index = selectedCells.indexOf(cellId);
        if (index === -1) {
            selectedCells.push(cellId);
        } else {
            selectedCells.splice(index, 1);
        }
    }

    updateSelectedCellsIndicator();
    
}

function updateSelectedCellsIndicator() {
    const gridItems = document.querySelectorAll('.grid-item');
    gridItems.forEach(item => {
        const cellId = item.id;
        if (selectedCells.includes(cellId)) {
            item.classList.add('selected');
        } else {
            item.classList.remove('selected');
        }
    });
}

function doneSelecting() {
    document.getElementsByClassName('grid-container')[0].style.display = 'none';
    document.getElementById('done').style.display = 'none';

    document.getElementById('header').innerHTML = 'Enter containers to load onto ship';

    const containerInput = document.querySelector('.container-input');
    containerInput.style.display = 'block';
    document.getElementById('containerInput').focus();
}

function handleContainerInput(event) {
    if (event.key === 'Enter') {
        let containerInput = document.getElementById('containerInput');
        toLoad.push(containerInput.value);

        let confirmationPopup = document.querySelector('.confirmation-popup');
        confirmationPopup.style.display = 'block';
    }
}

function addMoreContainers() {
    const containerInput = document.getElementById('containerInput');
    containerInput.value = '';
    containerInput.focus();

    const confirmationPopup = document.querySelector('.confirmation-popup');
    confirmationPopup.style.display = 'none';

    const containerInputVisible = document.querySelector('.container-input');
    containerInputVisible.style.display = 'block';
}

async function sendLoadRequest() {
    document.querySelector('.container-input').style.display = 'none';
    document.querySelector('.confirmation-popup').style.display = 'none';

    document.getElementById('header').innerHTML = 'Calculating the fastest set of operations...';

    formData = new FormData();
    formData.append('load', toLoad);
    formData.append('unload', selectedCells);

    const response = await fetch('/load', {
        method: 'POST',
        body: formData
    });

    window.location.href = "/steps";
}

