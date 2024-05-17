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

    function delete_comment(id){
        $.get("/DeleteComment/" + id, function (data) {window.location.replace(data)});
    };

    let id;
    $(".deleteItem").click(
    function() 
        {
            id = $(this).parent().attr("id");
            $("#itemDeletion").css("display", "block");
        }
    )

    $("#notificationClose").click(()=>{$("#itemDeletion").css("display", "none");});
    $("#confirm").click(()=>{delete_comment(id);});
});