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
    $("#username").blur(() => {notifyEmpty("#username");});
    $("#password").blur(() => {notifyEmpty("#password");});
});