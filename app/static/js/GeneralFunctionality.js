// Sets a password field to visible/ invisible when clicked by user
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

// Deletes the generated word from the html document
function removeWord(word){
    $(word).remove();
}

// Randomly generates an example poll, with randomised position and size
function makeWord(){
    // Randomised values for position and size
    const offset = Math.random() * 1000;
    const size = Math.random() * 15 + 10;

    //Random match-ups list
    const names = ["Batman vs. Superman", "Cat vs. Dog", "Java vs. C#", "Hot vs. Cold", "Horror vs. Romance", "Coffee vs. Tea", "Cookies vs. Cake", "Bugs vs. Fish", "Basketball vs. Hockey", "Pencil vs. Pen", "Coke vs. Pepsi", "Red vs. Blue", "Chemistry vs. Physics"];

    //Modify the multiply for number of options(-1)
    const randomName = names[Math.round(Math.random()*12)];
    const word = $("<div id = 'word'>" +randomName +"</div>");
    word.css("bottom",offset + "px")
    word.css("font-size", size+"px")
    $("body").append(word);

    // Removes the word after it has gone off screen
    setTimeout(()=>{removeWord(word);}, 8000);
}

// Initialises dropdown behaviour for banner
function init_dropdowns() {
    // Shows home dropdown on hover, closes others
    $("#home").hover(
        function() {
            toggle("#homeDropdown");
            untoggle("#SearchDropdown");
        },
        function() {
            untoggle("#homeDropdown");
        }
    );

    // Shows home account on hover, closes others
    $("#account").hover(
        function() {
            toggle("#accountDropdown");
            untoggle("#SearchDropdown");
        },
        function() {
            untoggle("#accountDropdown");
        }
    );

    // Shows searchbar dropdown on hover, closes others
    $("#SearchBar").focus(function() {
        if ($("#SearchDropdown").css("display") == "none") {
            toggle("#SearchDropdown");
        }
    });

    // Closes searchbar dropdown when user clicks away
    $("body").click(function(event) {
        const target = $(event.target);
        if($("#SearchDropdown").css("display") != "none" && target.closest("#search").length === 0){
            untoggle("#SearchDropdown");
        }
    });

    // Animation for closing dropdown
    function untoggle(selector) {
        if ($(selector).css("display") != "none") {
            $(selector).animate({height:"toggle"});
        }
    }

    // Animation for openning dropdown
    function toggle(selector) {
        if ($(selector).css("display") == "none") {
            $(selector).animate({height:"toggle"});
        }
    }
}

// Submits searchbar contents when enter is pressed
function check_search_enter(event){
    if(event.which == 13){
        document.getElementById("postSearchForm").submit();
    }
}

// Initialisation for all functionality regarding banner and background for all pages
function init(){
    init_dropdowns();
    // Generates new background poll every 0.7 seconds
    setInterval(()=>{makeWord();}, 700);

    // Displays any flash messages when page is loaded for 3 seconds
    setTimeout(() => {$("#messageDisplay").animate({height:"toggle"});}, 3000);

    // Checks if enter was pressed with searchbar selected
    $("#SearchBar").keydown(check_search_enter);
    $("#SearchDropdown").keydown(check_search_enter);

    // Resets selected tags in searchbar dropdown on click
    $("#tagReset").click(function(){
        event.preventDefault();
        $(".tagField option").prop("selected", false)
    })

    // Event for deletion notificaions (comments or posts), submits the deletion form on click
    $("#confirm").click(()=>{$("#deletionForm").submit()});

    // Event for hiding deletion notifications if close button is pressed
    $("#notificationClose").click(()=>{$("#itemDeletion").css("display", "none");});
}
$(document).ready(init);