// Loads polls for popular page on page load or filter change
$(document).ready(() =>{
    $("#popularPolls").load("/GetMostPopular/Daily");
    $("#popularTimePeriod").change(function(){
        const mode = $(this).val();
        $("#popularPolls").load("/GetMostPopular/" + mode);
    });
});