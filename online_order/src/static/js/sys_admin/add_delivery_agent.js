
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
        url:  '/edit-delivery-agent',
        async:  false,
        data:{
             id: JSON.stringify(id),
        },
        success:function(data){

//                console.log(data);
                $("#id_name").val(data['name']);
                $("#id_mobile").val(data['mobile']);
                $("#id_email").val(data['email']);
                $("#id_address").val(data['address']);
                $("#id_payment_percentage").val(data['payment_percentage']);
                $("#id_area_specified").val(data['area_specified']);

                $("#id_key").val(data['id']);

                document.getElementById('divIdContent').scrollIntoView();
        }
    });
}

//$('form').submit( function(){
//    $("#idErrorLabel").text('');
//    $(".alert-box").hide();
//
//    if( !$("#id_is_checked_whats_app").is(':checked') && !$("#id_is_checked_email").is(':checked') ){
//        $("#idErrorLabel").text('At least one alerting method must be chosen!');
//        $(".alert-box").show();
//        var el = document.getElementById("idErrorLabel");
//        el.scrollIntoView(false);
//        $(".alert-box").fadeOut(5000);
//        return false;
//    }
//    if( $("#id_is_checked_email").is(':checked') ){
//        if( !$("#id_email").val()){
//            $("#idErrorLabel").text('Email must be entered, if you want to choose email as alerting method!');
//            $(".alert-box").show();
//            var el = document.getElementById("idErrorLabel");
//            el.scrollIntoView(false);
//            $(".alert-box").fadeOut(5000);
//            return false;
//        }
//    }
//});

function resetAll(){
    document.getElementById("idForm").reset();
    $("#idSave").text("Save");
    $("#id_key").val("");
//    $(".search").val('');
}

//called when key is pressed in textbox
$("#id_mobile").keypress(function (e) {
 //if the letter is not digit then display error and don't type anything
 if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
    //display error message
    $("#errmsg").html("Digits Only").show().fadeOut("slow");
    return false;
 }
});

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
//
