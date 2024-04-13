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
    let lowercase = new RegExp("[a-z]+");
    let uppercase = new RegExp("[A-Z]+");
    let number = new RegExp("[0-9]+");
    let symbol = new RegExp("[~`!@#$%^&*()-+=|,<>?/\\\.'\"]+");
    if(!lowercase.test(password)){
        return "Password needs one or more lowercase letters.";
    }
    else if(!uppercase.test(password)){
        return "Password needs one or more uppercase letters.";
    }
    else if(!number.test(password)){
        return "Password needs one or more numbers.";
    }
    else if(!symbol.test(password)){
        return "Password needs one or more symbols.";
    }
    else if(password.length < 12){
        return "Password needs to be atleast 12 characters long.";
    }
    else{
        return "Valid password.";
    }
}

function verifyPassword(id){
    let password = $(id).val();
    let response = checkPassword(password);
    $(id + "+ #passwordNotification").css("display", "block");
    if(response == "Valid password."){
        $(id + "+ #passwordNotification").html("<span class = 'fas fa-check'></span> " + response);
        $(id + "+ #passwordNotification").css("color", "green");
    }
    else{
        $(id + "+ #passwordNotification").html("<span class = 'fas fa-exclamation'></span> " + response);
        $(id + "+ #passwordNotification").css("color", "red");
    }
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
function removeWord(word){
    $(word).remove();
}
function makeWord(){
    let offset = Math.random() * 1000;
    let size = Math.random() * 15 + 10;
    //Random match-ups list
    let names = ["Batman vs. Superman", "Cookies vs. Cake", "Bugs vs. Fish", "Basketball vs. Hockey", "Pencil vs. Pen", "Coke vs. Pepsi", "Red vs. Blue", "Chemistry vs. Physics"];
    //Modify the multiply for number of options(-1)
    let randomName = names[Math.round(Math.random()*7)];
    let word = $("<div id = 'word'>" +randomName +"</div>");
    word.css("bottom",offset + "px")
    word.css("font-size", size+"px")
    $("body").append(word);
    setTimeout(()=>{removeWord(word);}, 8000);
}

function init(){
    $("#usernameField").blur(() => {notifyEmpty("#usernameField");});
    $("#passwordField").blur(() => {notifyEmpty("#passwordField");});
    $("#emailField").blur(() => {verifyEmail("#emailField")});
    $("#passwordField").blur(() => {verifyPassword("#passwordField")});
    $("#visibility").click(() => {changeVisibilty();});
    $(".inputFields").submit(() => {createCookie();})
    setInterval(()=>{makeWord();}, 700);
}
$(document).ready(init);
fillUsername();