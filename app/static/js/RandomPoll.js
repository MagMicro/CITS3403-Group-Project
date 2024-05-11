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
        const pollContainer = document.getElementById("polls-container");
        switch(xhttp.status){
            // Case that the vote was successfully logged in the system
            case 200:
                pollContainer.innerHTML = xhttp.responseText;
                handle_submission();
                break;

            // Case there are no more valid random polls
            case 404:
                pollContainer.innerHTML = xhttp.responseText;
                document.getElementById("next-poll").style.display = "none"
                break;
        }
    }
    xhttp.send();
}