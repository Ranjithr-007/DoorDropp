
$(document).ready( function(){
    var default_status = get_area_of_village(default_village_id);
    if(default_status){
        $("#id_area_specified").val(parseInt(default_area_id));
    }
});

$("#id_village").change( function(){
    var village_id = $("#id_village").val();
    get_area_of_village(village_id);
});

function get_area_of_village(village_id){
    var response = false;
    $.ajax({
        type: 'GET',
        dataType : 'JSON',
        url:  '/get-area',
        async:  false,
        data:{
             village_id: JSON.stringify(village_id),
        },
        success:function(data){
//            console.log(data);
            $("#id_area_specified").empty();
            if(data['status'] == 'SUCCESS'){
                if(data.data.length){
                    var str = "";
                    for(var i=0; i<data.data.length; i++){
                        str += '<option value="'+data.data[i].id+'">'+data.data[i].name+'</option>';
                    }
                    $("#id_area_specified").append(str);
                    response = true;
                }else{
                    var str = '';
                    $("#id_area_specified").append(str);
                }
            }else{
                var str = '';
                $("#id_area_specified").append(str);
            }
        }
    });
    return response;
}

var mobile = $("#id_mobile").val();
jQuery.validator.addMethod('check_mobile', function(mobile) {
    return /[0-9]{10}/.test(mobile);
});

var email = $("#id_email").val();
$.validator.addMethod("email_value_pattern", function(email) {
    if(email){
        return /(?:[a-z0-9!#$%&*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&*+/=?^_`{|}~-]+)*|(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*)@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/.test(email);
    }
    return true;
});

$('#idForm').validate({
    rules: {
        name: {
          required: true,
          maxlength: 100,
        },
        mobile: {
          minlength: 10,
          maxlength: 10,
          required: true,
          check_mobile: true,
        },
        email: {
          email_value_pattern: true,
        },
        landmark: {
          required: true,
          maxlength: 250,
        },
        address: {
          required: true,
          maxlength: 2000,
        },
        village: {
          required: true,
        },
        area_specified: {
          required: true,
        },
    },
    messages: {
        name: {
            maxlength: "Name must be within 100 characters",
            required: "Name is required",
        },
        mobile: {
            required: "Mobile number is required",
            minlength: "Mobile number must be 10 digit",
            maxlength: "Mobile number must be 10 digit",
            check_mobile: "Mobile number is not valid",
        },
        email: {
            email_value_pattern: "Email is not valid",
        },
        landmark: {
            maxlength: "Landmark can't exceed 250 characters",
            required: "Landmark is required!",
        },
        address: {
            maxlength: "Address can't exceed 2000 characters",
            required: "Address is required!",
        },
        village: {
            required: "Village / Municipality required!",
        },
        area_specified: {
            required: "Area / Locality required!",
        },
    },

    errorContainer : $('#errorContainer'),
    errorLabelContainer : $('#errorContainer ul'),
    wrapper : 'li',

    highlight: function(element) {
        $('.panel100').show();
        var id_attr = "#" + $(element).attr("id");
        $(id_attr).removeClass('success-valid').addClass('error-valid');
        document.getElementById('errorContainer').scrollIntoView(true);
    },
    unhighlight: function(element) {
        var id_attr = "#" + $(element).attr("id");
        $(id_attr).removeClass('error-valid').addClass('success-valid');
    },
});

$('input').keypress(function(){
    if ($('#errorContainer').css('display') == 'none') {
         $('.panel100').hide();
    }else{
        $('.panel100').show();
    }
});

$('input').change(function(){
    if ($('#errorContainer').css('display') == 'none') {
         $('.panel100').hide();
    }else{
        $('.panel100').show();
    }
});

$('select').change(function(){
    if ($('#errorContainer').css('display') == 'none') {
         $('.panel100').hide();
    }else{
        $('.panel100').show();
    }
});

//called when key is pressed in textbox
$("#id_mobile").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        return false;
    }
});
