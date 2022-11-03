
$(document).ready( function(){
    resetAll();
//    $(".clear").removeClass('selected_color');
    $('#id_data_table').DataTable();
});

$(".edit-icon-menu").click( function(){
    $(".overlay").show();
    var id = this.id;
    $("#id_key").val(id);
    getLoadData(id);
    $(".overlay").hide();
    $("#idSave").text("Update");
});


function getLoadData(id){
    $.ajax({
        type: 'GET',
        dataType : 'JSON',
        url:  '/edit-area',
        async:  false,
        data:{
             id: JSON.stringify(id),
        },
        success:function(data){

//                console.log(data);
                $("#id_area").val(data['area']);
                $("#id_village").val(data['village']);
                $("#id_kilometer_limit").val(data['kilometer_limit']);
                $("#id_key").val(data['id']);

                document.getElementById('divIdContent').scrollIntoView();
        }
    });
}

function resetAll(){
    document.getElementById("idForm").reset();
    $("#idSave").text("Save");
    $("#id_key").val("");
//    $(".search").val('');
}

//$(".search").on("keyup", function () {
//    var v = $.trim($(this).val());
//    var v_cap = capitalizeFirstLetter(v);
//    $(".clear").removeClass("selected_color");
//    $(".clear").each(function () {
//        if ((v_cap && $(this).find('td.name').text().search(v_cap) != -1) || (v && $(this).find('td.name').text().search(v) != -1)) {
//            var content = $(this).find('td.name').text();
//            $(this).addClass('selected_color');
//            document.getElementsByClassName('clear')[0].scrollIntoView();
//        }
//    });
//
//});
//
//function capitalizeFirstLetter(string) {
//    return string.charAt(0).toUpperCase() + string.slice(1);
//}
//

