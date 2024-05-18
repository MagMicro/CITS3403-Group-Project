// Opens new window with a given post when a user clicks on it
 $(".postContent").click(function(){window.open("/Poll/" + $(this).parent().attr("id"));});