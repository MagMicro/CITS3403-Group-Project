// Stores the password the page loaded with
let original;

function init(){
    // Loads a user's posts on page open
    $("#userPosts").load("/GetUserPosts/" + $("#SortOption").val() + "/" + $("#SortOrder").val() + "/" + $("#AccountID").val());

    // Loads new posts order when filters are changed
    $("#SortOption").change(() => {$("#userPosts").load("/GetUserPosts/" + $("#SortOption").val() + "/" + $("#SortOrder").val() + "/" + $("#AccountID").val())});
    $("#SortOrder").change(() => {$("#userPosts").load("/GetUserPosts/" + $("#SortOption").val() + "/" + $("#SortOrder").val() + "/" + $("#AccountID").val())});

    // Shows account deletion propmt when cross on profile is clicked
    $("#accountDelete").click(() => {$("#accountConfirmMsg").css("display", "block")});

    // Closes account deletion prompt when close is clicked
    $("#accountNotificationClose").click(() => {$("#accountConfirmMsg").css("display", "none");});

    // Allows user to change usernmame on button click
    $("#renameIcon").click(() => {
        // Store initial username
        original = $("#AccountUsername").val()
        const length = original.length
        // Makes users cursor focus on end of current username
        $("#AccountUsername").attr("disabled", false).focus()
        $("#AccountUsername")[0].setSelectionRange(length, length)
    });
    // Checks to see if username needs updating when user clicks off
    $("#AccountUsername").blur(() => {
        current = $("#AccountUsername").val()
        // If the username hasnt changed, just deselects the username field and makes it disabled
        if (current === original){
            $("#AccountUsername").attr("disabled", true);
        }
        // If the username has changed, submits form to see if name change was successful
        else{
            $("#usernameForm").submit();
        }
    });
}
$(document).ready(init);