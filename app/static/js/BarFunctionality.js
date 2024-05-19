// Initialises the poll results bar, so that the bar reflects what the poll difference looks like
function set_bar(){
    left = $("#PercentageLeft").text();
    right = $("#PercentageRight").text();

    $("#left").css("width", left);
    $("#right").css("width", right);
    $("#divider").css("left", left);
}
$(document).ready(() => {set_bar();});