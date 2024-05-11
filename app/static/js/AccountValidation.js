function checkUsername(username){
    if(username.length < 5){
        return "username must be longer than 5 characters."
    }
    else if(username.length > 20){
        return "max username length exceeded (20 characters)"
    }
    else{
        return "Valid username."
    }
}
function verifyUsername(id){
    let username = $(id).val();
    $(id + "+ #usernameNotification").css("display", "block");
    response = checkUsername(username);
    if(response == "Valid username."){
        $(id + "+ #usernameNotification").html("<span class = 'fas fa-check'></span> " + response);
        $(id + "+ #usernameNotification").css("color", "green");
    }
    else{
        $(id + "+ #usernameNotification").html("<span class = 'fas fa-exclamation'></span> " + response);
        $(id + "+ #usernameNotification").css("color", "red");
    }
}
function checkEmail(email){
    let pattern = new RegExp("^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]{3}$");
    if(pattern.test(email)){
        return true;
    }
    return false;
}

function verifyEmail(id){
    let email = $(id).val();
    $(id + "+ #emailNotification").css("display", "block");
    if(!checkEmail(email)){
        $(id + "+ #emailNotification").html("<span class = 'fas fa-exclamation'></span> Invalid Email");
        $(id + "+ #emailNotification").css("color", "red");
    }
    else{
        $(id + "+ #emailNotification").html("<span class = 'fas fa-check'></span> " + "Valid Email");
        $(id + "+ #emailNotification").css("color", "green");
    }
}

function checkPassword(password){
    let lowercase = new RegExp("[a-z]+");
    let uppercase = new RegExp("[A-Z]+");
    let number = new RegExp("[0-9]+");
    let symbol = new RegExp("[-~`!@#\$%\^&\*()\+=|,<>\?/\\\.\'\"\_]+");
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

$(document).ready( () =>{
    $("#email").keydown(() => {verifyEmail("#email")});
    $("#email").blur(() => {verifyEmail("#email")});
    $("#password").keydown(() => {verifyPassword("#password")});
    $("#password").blur(() => {verifyPassword("#password")});
    $("#username").keydown(() => {verifyUsername("#username")});
    $("#username").blur(() => {verifyUsername("#username")});
    $("#creationForm").submit((event) => {if(!(
        checkUsername($("#username").val()) == "Valid username." && 
        checkEmail($("#email").val()) == true && 
        checkPassword($("#password").val()) == "Valid password."))
        {event.preventDefault();}});
});