let original;
function init(){
    $("#userPosts").load("/GetUserPosts/" + $("#SortOption").val() + "/" + $("#SortOrder").val() + "/" + $("#AccountID").val());
    $("#SortOption").change(() => {$("#userPosts").load("/GetUserPosts/" + $("#SortOption").val() + "/" + $("#SortOrder").val() + "/" + $("#AccountID").val())});
    $("#SortOrder").change(() => {$("#userPosts").load("/GetUserPosts/" + $("#SortOption").val() + "/" + $("#SortOrder").val() + "/" + $("#AccountID").val())});
    $("#accountDelete").click(() => {$("#accountConfirmMsg").css("display", "block")});
    $("#accountNotificationClose").click(() => {$("#accountConfirmMsg").css("display", "none");});
    $("#renameIcon").click(() => {
        original = $("#AccountUsername").val()
        const length = original.length
        $("#AccountUsername").attr("disabled", false).focus()
        $("#AccountUsername")[0].setSelectionRange(length, length)
    });
    $("#AccountUsername").blur(() => {
        current = $("#AccountUsername").val()
        if (current === original){
            $("#AccountUsername").attr("disabled", true);
        }
        else{
            $("#usernameForm").submit();
        }
    });
}
$(document).ready(init);