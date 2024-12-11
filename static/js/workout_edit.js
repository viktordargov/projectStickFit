function toggleFields() {
    const repetitionField = document.getElementById('repetition_id');
    const durationField = document.getElementById('duration_id');
    const option1Radio = document.getElementById('option1-radio');

    if (option1Radio.checked) {
        repetitionField.classList.remove('hidden');
        durationField.classList.add('hidden');
    } else {
        durationField.classList.remove('hidden');
        repetitionField.classList.add('hidden');
    }
}

window.onload = function () {
    toggleFields();
}