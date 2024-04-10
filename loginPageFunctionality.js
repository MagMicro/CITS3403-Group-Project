function checkEmail(email){
    let pattern = new RegExp("^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]{3}$");
    if(pattern.test(email)){
        return true;
    }
    return false;
}

function verifyEmail(id){
    let email = $(id).val();
    if(!checkEmail(email)){
        $(id + "+ #emailNotification").css("display", "block");
    }
    else{
        $(id + "+ #emailNotification").css("display", "none");
    }
}
function checkPassword(password){
    let pattern = new RegExp("[a-z]+[A-Z]+[0-9]+[~`!@#$%^&*()-_+=|\\,.<>?/]+");
    if(pattern.test(password) && password.length >= 12){
        return true;
    }
    return false;
}

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
    $("#emailField").blur(() => {verifyEmail("#emailField")});
    $("#visibility").click(() => {changeVisibilty();});
    $("#inputFields").submit(() => {createCookie();})
}
$(document).ready(init);
fillUsername();