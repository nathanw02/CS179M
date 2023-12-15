let currentStep = 0;
let steps = [];
let r1, c1, r2, c2;

function loadSteps(input) {
    steps = input;
    console.log(steps)
    document.addEventListener('DOMContentLoaded', (event) => {
        if (steps.toString() == [-1, -1].toString()) {
            document.getElementById('confirmation-message').innerHTML = 'An error occured. Please try again.';
            document.getElementById('confirmation').style.display = 'block';
            document.getElementById('modalOverlay').style.display = 'block';
        }else if (steps.length == 0) {
            document.getElementById('modalOverlay').style.display = 'block';
            document.getElementById('confirmation').style.display = 'block';
        } else {
            updateGridWithStep();
            updateStepDisplay();
        }
    });
}

function nextStep() {
    moveContainer(r1, c1, r2, c2);
    if (currentStep < steps.length - 1) {
        currentStep++;
        updateGridWithStep();
        updateStepDisplay();
    } else {
        document.getElementById('modalOverlay').style.display = 'block';
        document.getElementById('confirmation').style.display = 'block';
    }
}

function updateGridWithStep() {
    resetGrid();

    const [originR, originC, destinationR, desitinationC] = steps[currentStep];

    highlightCell(originR + 1, originC, 'red');
    highlightCell(destinationR + 1, desitinationC, 'green');

    r1 = originR + 1;
    c1 = originC;
    r2 = destinationR + 1;
    c2 = desitinationC;

}

function resetGrid() {
    const highlightedCells = document.querySelectorAll('.highlighted');
    highlightedCells.forEach(cell => {
        cell.classList.remove('highlighted');
    });
}

function highlightCell(row, col, color) {
    const cellId = `cell-${row}-${col}`;
    const cell = document.getElementById(cellId);
    if (cell) {
        cell.classList.add('highlighted');
        cell.style.backgroundColor = color;
    }
}

function updateStepDisplay() {
    const stepCount = document.getElementById('stepCount');
    stepCount.innerHTML = 'Move Containers - Step ' + (currentStep + 1);
}

function moveContainer(r1, c1, r2, c2) {
    const originCell = document.getElementById(`cell-${r1}-${c1}`);
    const destinationCell = document.getElementById(`cell-${r2}-${c2}`);

    if (r2 != 0) {
        destinationCell.innerHTML = originCell.innerHTML;
        destinationCell.style.backgroundColor = 'rgb(63, 59, 59)';
    } else {
        destinationCell.style.backgroundColor = 'black';
    }

    if ([r1, c1].toString() != [0, 0].toString()) {
        originCell.innerHTML = '';
        originCell.style.backgroundColor = 'white';
    }
}

function finishTransfer() {
    // TODO: post request to write updated manifest to desktop somewhere
    window.location.href = '/';
}