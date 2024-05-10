// vote.js

document.addEventListener("DOMContentLoaded", function () {
    loadRandomPoll();

    // Handle the "Next Poll" button click
    document.getElementById("next-poll").addEventListener("click", function () {
        loadRandomPoll();
    });
});

function loadRandomPoll() {
    fetch("/api/poll/random")
        .then((response) => response.json())
        .then((poll) => {
            if (poll.message) {
                document.getElementById("polls-container").innerHTML = `<p>${poll.message}</p>`;
            } else {
                displayPoll(poll);
            }
        })
        .catch((error) => {
            console.error("Error loading polls:", error);
        });
}

function displayPoll(poll) {
    const pollContainer = document.getElementById("polls-container");
    pollContainer.innerHTML = `
        <div class="poll">
            <h3>${poll.title}</h3>
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
    fetch(`/api/poll/vote`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ poll_id: pollId, option: option }),
    })
        .then((response) => response.json())
        .then((updatedPoll) => {
            showResults(updatedPoll);
        })
        .catch((error) => {
            console.error("Error submitting vote:", error);
        });
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
