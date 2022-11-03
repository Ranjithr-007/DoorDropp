

$(document).ready( function(){
//    $(".fixed-box").fadeOut(4000);
});

$("#id_area").change( function(){
    $('#idForm').trigger('submit');
});

$(".search").on("keyup", function () {
    var v = $.trim($(this).val());
    var v_cap = capitalizeFirstLetter(v);
    $(".clear").removeClass("selected_color");
    $(".clear").each(function () {
        if ((v_cap && $(this).find('h5.search_name').text().search(v_cap) != -1) || (v && $(this).find('h5.search_name').text().search(v) != -1)) {
            var content = $(this).find('h5.search_name').text();
            $(this).addClass('selected_color');
            document.getElementsByClassName('clear')[0].scrollIntoView();
        }
    });

});

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}