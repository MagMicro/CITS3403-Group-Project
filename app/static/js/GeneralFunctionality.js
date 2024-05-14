function changeVisibilty(){
    if($("#visibility").attr("class") == "fas fa-eye-slash"){
        $("#visibility")
        .attr("class", "fas fa-eye")
        .attr("title", "Hide")
        .css("color", "green");

        $("#password").attr("type", "text");
    }
    else{
        $("#visibility")
        .attr("class", "fas fa-eye-slash")
        .attr("title", "View")
        .css("color", "red");
        
        $("#password").attr("type", "password")
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

function untoggle(id){
    if($(id).css("display") != "none"){
        $(id).animate({height:"toggle"});
    }
}
function init_dropdowns(){
    $("#home").click(() => {
        $("#homeDropdown").animate({height:"toggle"});
        untoggle("#accountDropdown");
        untoggle("#SearchDropdown");
    });
    $("#account").click(() => {
        $("#accountDropdown").animate({height:"toggle"});
        untoggle("#homeDropdown");
        untoggle("#SearchDropdown");
    });

    $("#SearchBar").focus(() => {
        if($("#SearchDropdown").css("display") == "none"){
            $("#SearchDropdown").animate({height:"toggle"});
        }
        untoggle("#homeDropdown");
        untoggle("#accountDropdown");
    });
}

function check_search_enter(event){
    if(event.which == 13){
        document.getElementById("postSearchForm").submit();
    }
}
function init(){
    init_dropdowns();
    setInterval(()=>{makeWord();}, 700);
    setTimeout(() => {$("#messageDisplay").animate({height:"toggle"});}, 3000);
    $("#SearchBar").keydown(check_search_enter);
    $("#SearchDropdown").keydown(check_search_enter);
    $("#tagReset").click(function(){
        event.preventDefault();
        $(".tagField option").prop("selected", false)
    })
}
$(document).ready(init);