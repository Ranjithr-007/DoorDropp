
$(document).ready(function () {
    $(".messages").fadeOut(5000);
});

$(".r-icon-bar").on("click", function () {
    var width = $(window).width();
    if(width < 600){
        $(".sidebar-wrpr").removeClass("access");
        $(".dashboard-area").removeClass("access");
        $(".r-icon-bar2").removeClass("access");
    }else{
        $(".sidebar-wrpr").addClass("active");
        $(".dashboard-area").addClass("active");
        $(".r-icon-bar2").addClass("active");
    }
});

$(".r-icon-bar2").on("click", function () {
    var width = $(window).width();
    if(width < 600){
        $(".sidebar-wrpr").addClass("access");
        $(".dashboard-area").addClass("access");
        $(this).addClass("access");
    }else{
        $(".sidebar-wrpr").removeClass("active");
        $(".dashboard-area").removeClass("active");
        $(this).removeClass("active");
    }
});

