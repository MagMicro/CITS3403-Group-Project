function init(){
    $("#userPosts").load("/GetUserPosts/" + $("#sortOption").val() + "/" + $("#sortOrder").val());
    $("#sortOption").change(() => {$("#userPosts").load("/GetUserPosts/" + $("#sortOption").val() + "/" + $("#sortOrder").val());});
    $("#sortOrder").change(() => {$("#userPosts").load("/GetUserPosts/" + $("#sortOption").val() + "/" + $("#sortOrder").val());});
    $("#accountDelete").click(() => {$("#accountConfirmMsg").css("display", "block")});
    $("#accountNotificationClose").click(() => {$("#accountConfirmMsg").css("display", "none");});
}
$(document).ready(init);