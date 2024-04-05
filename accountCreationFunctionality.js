function checkEmail(email){
    let pattern = new RegExp("^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]{3}$");
    if(pattern.test(email)){
        return true;
    }
    return false;
}
function checkPassword(password){
    let pattern = new RegExp("[a-z]+[A-Z]+[0-9]+[~`!@#$%^&*()-_+=|\\,.<>?/]+");
    if(pattern.test(password) && password.length >= 12){
        return true;
    }
    return false;
}