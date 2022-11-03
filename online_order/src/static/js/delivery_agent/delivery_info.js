

$(document).ready( function(){
    $("#id_payment_method").ready( function(){
        $("#divIdShowQr").hide();
        var is_upi = $('option:selected', this).attr('name');
//        console.log(is_upi);
        if(is_upi == 'True'){
            var qr_url = $('option:selected', this).attr('title');
//            console.log(qr_url);
            if(qr_url){
                $("#idShowQr").prop('href', qr_url);
                $("#divIdShowQr").show();
            }
        }
    });
});
$("#id_payment_method").change( function(){
    $("#divIdShowQr").hide();
    var is_upi = $('option:selected', this).attr('name');
//    console.log(is_upi);
    if(is_upi == 'True'){
        var qr_url = $('option:selected', this).attr('title');
//        console.log(qr_url);
        if(qr_url){
            $("#idShowQr").prop('href', qr_url);
            $("#divIdShowQr").show();
        }
    }
});