// Initialises listener for vote submission and ensuers options provided are valid
function handle_submission(){
    document.getElementById("poll-form").addEventListener("submit", function (event) {
        event.preventDefault();
        poll_ID = document.getElementsByClassName("poll")[0].getAttribute("id");

        // Make sure the option selected is valid
        if(option == '1' || option == '2') {
            voteOnPoll(poll_ID, option);
        }
    });
}

// Function responsible for sending a vote request to the server to be processed, acts corresponding to code returned
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

function toggle_selected(current){
    $(".selectionOption").css("background-color", "white");
    $("label[for = " + $(current).attr('id') + "]").css("background-color", "rgb(232, 232, 232)");
    option = $(current).attr('value');
}

$(document).ready(() => {
    let option;
    handle_submission();
    // Changes background colour on option selected
    $("#SubmissionOptions-0").click(function(){toggle_selected(this);});
    $("#SubmissionOptions-1").click(function(){toggle_selected(this);});
});