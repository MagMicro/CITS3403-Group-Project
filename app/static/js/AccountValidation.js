// User side validation for username, ensures username is correct length
function checkUsername(username){
    if(username.length < 5){
        return "username must be atleast 5 characters long."
    }
    else if(username.length > 15){
        return "max username length exceeded (15 characters)"
    }
    else{
        return "Valid username."
    }
}

// Displays a message if the username validation fails, notifying the user
function verifyUsername(id){
    const username = $(id).val();
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

// User-side validation that makes sure that a valid email format is entered
function checkEmail(email){
    const pattern = new RegExp("^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]{3}$");
    if(pattern.test(email)){
        return true;
    }
    return false;
}

// Displays a message if the email validation fails, notifying the user
function verifyEmail(id){
    const email = $(id).val();
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

// User-side validation for strong passwords
function checkPassword(password){
    const lowercase = new RegExp("[a-z]+");
    const uppercase = new RegExp("[A-Z]+");
    const number = new RegExp("[0-9]+");
    const symbol = new RegExp("[-~`!@#\$%\^&\*()\+=|,<>\?/\\\.\'\"\_]+");
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

// Displays a message if the password validation fails, notifying the user
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
    // Checks if the email is valid whenever the user types
    $("#email").keyup(() => {verifyEmail("#email")});
    $("#email").blur(() => {verifyEmail("#email")});

    // Checks if the password is valid whenever the user types
    $("#password").keyup(() => {verifyPassword("#password")});
    $("#password").blur(() => {verifyPassword("#password")});
    
    // Checks if the username is valid whenever the user types
    $("#username").keyup(() => {verifyUsername("#username")});
    $("#username").blur(() => {verifyUsername("#username")});

    // Only allows form submission if all validators are passed
    $("#creationForm").submit((event) => {if(!(
        checkUsername($("#username").val()) == "Valid username." && 
        checkEmail($("#email").val()) == true && 
        checkPassword($("#password").val()) == "Valid password."))
        {event.preventDefault();}});
});