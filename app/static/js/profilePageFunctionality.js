function init(){
    $("#userPosts").load("/GetUserPosts/" + $("#SortOption").val() + "/" + $("#SortOrder").val());
    $("#SortOption").change(() => {$("#userPosts").load("/GetUserPosts/" + $("#SortOption").val() + "/" + $("#SortOrder").val());});
    $("#SortOrder").change(() => {$("#userPosts").load("/GetUserPosts/" + $("#SortOption").val() + "/" + $("#SortOrder").val());});
    $("#accountDelete").click(() => {$("#accountConfirmMsg").css("display", "block")});
    $("#accountNotificationClose").click(() => {$("#accountConfirmMsg").css("display", "none");});
}
$(document).ready(init);