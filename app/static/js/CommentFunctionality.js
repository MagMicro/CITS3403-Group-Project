$(document).ready(() =>{
    $("#CommentContent").keyup(function(){
        if($(this).val().length <= 0){
            $("#commentCreationButtons").css("display", "none");
        }
        else if($("#commentCreationButtons").css("display") == "none"){
            $("#commentCreationButtons").css("display", "block");
        }
    })
});