let exerciseIndex = 0;
let timer = null;
let duration = 0;
let timeLeft = 0;
let isPaused = false;

function startWorkout() {
    document.getElementById("start-button").style.display = "none";
    showExercise();

}

function showExercise() {
    if (exerciseIndex >= exercises.length) {
        document.getElementById("exercise-name").innerText = "Congratulations!";
        document.getElementById("timer").innerText = "";
        document.getElementById("next-button").style.display = "none";
        document.getElementById("pause-button").style.display = "none";
        document.getElementById("complete-form-div").style.display = "inline";
        document.getElementById("previous-button").style.display = "none";
        return;
    }

    const exercise = exercises[exerciseIndex];
    document.getElementById("exercise-name").innerText = exercise.name;
    
    const currentRow = document.getElementById(`exercise-${exerciseIndex + 1}`);
    const allRows = document.querySelectorAll("#exercise-table tbody tr");
    allRows.forEach(row => row.classList.remove("current-exercise"));
    currentRow.classList.add("current-exercise");


    if (exercise.duration) {
        timeLeft = exercise.duration;
        document.getElementById("timer").style.display = "block";
        document.getElementById("repetitions-info").style.display = "none";
        updateTimer();
        timer = setInterval(countdown, 1000);
        document.getElementById("next-button").style.display = "inline";
        document.getElementById("pause-button").style.display = "inline";
        if (exerciseIndex > 0 && exerciseIndex <= exercises.length) {
            document.getElementById("previous-button").style.display = "inline";
        }
    } else if (exercise.repetition) {
        clearInterval(timer);
        document.getElementById("timer").style.display = "none";
        document.getElementById("repetitions-info").innerText = `Complete ${exercise.repetition} repetitions`;
        document.getElementById("repetitions-info").style.display = "block";
        document.getElementById("next-button").style.display = "inline";
        document.getElementById("pause-button").style.display = "none";
        if (exerciseIndex > 0 && exerciseIndex <= exercises.length) {
            document.getElementById("previous-button").style.display = "inline";
        }
    }
}

function countdown() {
    if (timeLeft <= 0) {
        clearInterval(timer);
        exerciseIndex++;
        showExercise();
    } else {
        timeLeft--;
        updateTimer();
    }
}

function updateTimer() {
    document.getElementById("timer").innerText = `${timeLeft}s`;
}

function pauseTimer() {
    clearInterval(timer);
    isPaused = true;
    document.getElementById("pause-button").style.display = "none";  // Hide the pause button
    document.getElementById("resume-button").style.display = "inline";  // Show the resume button
}

function resumeTimer() {
    isPaused = false;
    document.getElementById("pause-button").style.display = "inline";  // Show the pause button
    document.getElementById("resume-button").style.display = "none";  // Hide the resume button
    timer = setInterval(countdown, 1000);
}

function nextExercise() {
    if (isPaused === true) {
        resumeTimer()
    }
    clearInterval(timer);
    exerciseIndex++;
    showExercise();
}

function previousExercise() {
    if (isPaused === true) {
        resumeTimer()
    }
    clearInterval(timer);
    exerciseIndex--;
    if (exerciseIndex === 0) {
        document.getElementById("previous-button").style.display = "none";
    }
    showExercise();
}