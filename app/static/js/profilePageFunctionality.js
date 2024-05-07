function init(){
    $("#userPosts").load("/GetUserPosts/" + $("#sortOption").val() + "/" + $("#sortOrder").val());
    $("#sortOption").change(() => {$("#userPosts").load("/GetUserPosts/" + $("#sortOption").val() + "/" + $("#sortOrder").val());});
    $("#sortOrder").change(() => {$("#userPosts").load("/GetUserPosts/" + $("#sortOption").val() + "/" + $("#sortOrder").val());});
}
$(document).ready(init);