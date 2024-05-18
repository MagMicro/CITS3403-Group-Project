$(document).ready(() =>{
    // Checks if comment field is empty, hides the comment buttons when empty, displays them when user enters message
    $("#CommentContent").keyup(function(){
        if($(this).val().length <= 0){
            $("#commentCreationButtons").css("display", "none");
        }
        else{
            $("#commentCreationButtons").css("display", "block");
        }
    });
    // Deletes the current contents of the comment field when the user presses the cancel button
    $("#commentCancel").click(function(){
        event.preventDefault();
        $("#CommentContent").val("");
        $("#commentCreationButtons").css("display", "none");
    })
    onclick = "window.open('/Poll/' + $(this).attr('id'))"
});