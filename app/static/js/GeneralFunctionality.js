function changeVisibilty(){
    if($("#visibility").attr("class") == "fas fa-eye-slash"){
        $("#visibility").attr("class", "fas fa-eye");
        $("#visibility").attr("title", "Hide");
        $("#visibility").css("color", "green");
        $("#password").attr("type", "text");
    }
    else{
        $("#visibility").attr("class", "fas fa-eye-slash");
        $("#visibility").attr("title", "View");
        $("#visibility").css("color", "red");
        $("#password").attr("type", "password");
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
function toggle_dropdown(){
    $("#home").click(() => {
        $("#homeDropdown").animate({height:"toggle"});
        if($("#accountDropdown").css("display") != "none"){
            $("#accountDropdown").animate({height:"toggle"});
        }
    });
    $("#account").click(() => {
        $("#accountDropdown").animate({height:"toggle"});
        if($("#homeDropdown").css("display") != "none"){
            $("#homeDropdown").animate({height:"toggle"});
        }
    });
}
function init(){
    toggle_dropdown();
    setInterval(()=>{makeWord();}, 700);
    setTimeout(() => {$("#messageDisplay").animate({height:"toggle"});}, 3000);
}
$(document).ready(init);