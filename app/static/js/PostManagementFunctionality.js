    function delete_post(id){
        $.get("/DeletePost/" + id, function (data) {window.location.replace(data)});
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
    $("#confirm").click(()=>{delete_post(id);});

    // Opens new window with a given post when a user clicks on it
    $(".postContent").click(function(){window.open("/Poll/" + $(this).parent().attr("id"));});