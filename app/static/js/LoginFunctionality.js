// Notifies the user if a given field is empty
function notifyEmpty(id){
    if($(id).val() == ""){
        $(id + "+ .notify").css("display", "block");
        $(id + "+ .notify").html("<span class = 'fas fa-exclamation'></span> This field cannot be empty");
    }
    else{
        $(id + "+ .notify").css("display", "none");
    }
}

$(document).ready( () => {
    // Notifies user if username or password is empty
    $("#username").blur(() => {notifyEmpty("#username");});
    $("#password").blur(() => {notifyEmpty("#password");});

    // Prevents submission if either field is empty
    $("#loginForm").submit(() => {
        if($("#username + .notify").css("display" != empty || "#password + .notify").css("display" != empty)){
            event.preventDefault();
        }
    })
});