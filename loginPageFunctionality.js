function notifyEmpty(id){
    if($(id).val() == ""){
        $(id + "+ .notify").css("display", "block");
    }
    else{
        $(id + "+ .notify").css("display", "none");
    }
}
function changeVisibilty(){
    if($("#visibility").attr("class") == "fas fa-eye-slash"){
        $("#visibility").attr("class", "fas fa-eye");
        $("#visibility").attr("title", "Hide");
        $("#visibility").css("color", "green");
        $("#passwordField").attr("type", "text");
    }
    else{
        $("#visibility").attr("class", "fas fa-eye-slash");
        $("#visibility").attr("title", "View");
        $("#visibility").css("color", "red");
        $("#passwordField").attr("type", "password");
    }
}

function createCookie(){
    let value = $("#usernameField").val();
    const current_time = new Date();
    //Expires in a month (31 days)
    const offset = (31 *24 *60 *60 *1000);
    current_time.setTime(current_time.getTime() + offset);
    let cookie = "username=" + value + ";expires=" + current_time.toUTCString() + ";path=/"
    document.cookie = cookie;
}
function fillUsername (){
    let cookies = document.cookie.split(";");
    let username;
    for(cookie of cookies){
        if(cookie.includes("username")){
            username = cookie.substring(cookie.indexOf("=") + 1, cookie.length);
            break;
        }
    }
    if(username){
        $("#usernameField").val(username);
    }
}

function init(){
    $("#usernameField").blur(() => {notifyEmpty("#usernameField");});
    $("#passwordField").blur(() => {notifyEmpty("#passwordField");});
    $("#visibility").click(() => {changeVisibilty();});
    $("#inputFields").submit(() => {createCookie();})
}
$(document).ready(init);
fillUsername();