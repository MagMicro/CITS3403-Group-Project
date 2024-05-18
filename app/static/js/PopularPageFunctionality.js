$(document).ready(() =>{
    $("#popularPolls").load("/GetMostPopular/Daily");
    $("#popularTimePeriod").change(function(){
        const mode = $(this).val();
        $("#popularPolls").load("/GetMostPopular/" + mode);
    });
});