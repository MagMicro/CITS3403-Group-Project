function notifyEmpty(id){
    if($(id).val() == ""){
        $(id + "+ .notify").css("display", "block");
    }
    else{
        $(id + "+ .notify").css("display", "none");
    }
}
function change_visibilty(){
    if($("#visibility").attr("class") == "fas fa-eye-slash"){
        $("#visibility").attr("class", "fas fa-eye");
        $("#visibility").css("color", "green");
        $("#passwordField").attr("type", "text");
    }
    else{
        $("#visibility").attr("class", "fas fa-eye-slash");
        $("#visibility").css("color", "red");
        $("#passwordField").attr("type", "password");
    }
}
function init(){
    $("#usernameField").blur(() => {notifyEmpty("#usernameField");});
    $("#passwordField").blur(() => {notifyEmpty("#passwordField");});
    $("#visibility").click(() => {change_visibilty();});
}
$(document).ready(init);