function set_bar(){
    left = $("#PercentageLeft").text();
    right = $("#PercentageRight").text();

    alert(left);
    $("#left").css("width", left);
    $("#right").css("width", right);
    $("#divider").css("left", left);
}
$(document).ready(() => {set_bar();});