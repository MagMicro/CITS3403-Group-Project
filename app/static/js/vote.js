// vote.js

document.addEventListener("DOMContentLoaded", function () {
    loadRandomPoll();

    // Handle the "Next Poll" button click
    document.getElementById("next-poll").addEventListener("click", function () {
        loadRandomPoll();
    });
});

function loadRandomPoll() {
    const xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/api/poll/random");
    xhttp.onload = function(){
        const response = JSON.parse(xhttp.responseText);
        switch(xhttp.status){
            // Case that the vote was successfully logged in the system
            case 200:
                displayPoll(response);
                break;
            case 404:
                document.getElementById("polls-container").innerHTML = `<p>${response.message}</p>`;
                break;
        }
    }
    xhttp.send();
}

function displayPoll(poll) {
    const pollContainer = document.getElementById("polls-container");
    pollContainer.innerHTML = `
        <div class="poll">
            <h3>${poll.prompt}</h3>
            <form id="poll-form">
                <div class="poll-options">
                    <label>
                        <input type="radio" name="option" value="1">
                        ${poll.option1}
                    </label>
                    <label>
                        <input type="radio" name="option" value="2">
                        ${poll.option2}
                    </label>
                </div>
                <button type="submit" class="btn-vote">Vote</button>
            </form>
            <div id="results" style="display: none;">
                <h4>Results:</h4>
                <p>${poll.option1}: ${poll['left%']}%</p>
                <p>${poll.option2}: ${poll['right%']}%</p>
            </div>
        </div>
    `;

    // Handle form submission
    document.getElementById("poll-form").addEventListener("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const selectedOption = formData.get("option");

        if (selectedOption) {
            voteOnPoll(poll.ID, selectedOption);
        } else {
            alert("Please select an option before voting.");
        }
    });
}


function voteOnPoll(pollId, option) {
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/api/poll/vote");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.onload = function(){
        switch(xhttp.status){
            // Case that the user is not logged in, send them to login page
            case 404:
                window.location.replace(xhttp.responseText);
                break;

            // Case that the vote was successfully logged in the system
            case 200:
                showResults(JSON.parse(xhttp.responseText));
                break;
        }

    }
    // Send the field values as JSON to the server
    xhttp.send(JSON.stringify({ poll_id: pollId, option: option }));
}

function showResults(poll) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.style.display = "block";
    resultsDiv.innerHTML = `
        <h4>Results:</h4>
        <p>${poll.option1}: ${poll['left%']}%</p>
        <p>${poll.option2}: ${poll['right%']}%</p>
    `;
}
