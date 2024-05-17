function handle_submission(){
    document.getElementById("poll-form").addEventListener("submit", function (event) {
        event.preventDefault();
        poll_ID = document.getElementsByClassName("poll")[0].getAttribute("id");
        const formData = new FormData(event.target);
        const selectedOption = formData.get("option");

        if (selectedOption) {
            voteOnPoll(poll_ID, selectedOption);
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
                $("#results").css("display", "block");
                break;

            //Case the user has already voted OR invalid option was detected
            default:
                window.location.reload();
        }

    }
    // Send the field values as JSON to the server
    xhttp.send(JSON.stringify({ poll_id: pollId, option: option }));
}
