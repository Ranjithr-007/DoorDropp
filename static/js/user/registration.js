
var is_common_validation = false;

$(document).ready( function(){
    $(".messages").fadeOut(4000);
});


var value = $("#id_password").val();
$.validator.addMethod("check_lower", function(value) {
  return /[a-z]/.test(value);
});
$.validator.addMethod("check_upper", function(value) {
  return /[A-Z]/.test(value);
});
$.validator.addMethod("check_digit", function(value) {
  return /[0-9]/.test(value);
});
$.validator.addMethod("pw_check", function(value) {
  return /^[A-Za-z0-9\d=!\-@._*]*$/.test(value) && /[a-z]/.test(value) && /\d/.test(value) && /[A-Z]/.test(value);
});



var email = $("#id_email").val();
$.validator.addMethod("email_value_pattern", function(email) {
    if(email){
        return /(?:[a-z0-9!#$%&*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&*+/=?^_`{|}~-]+)*|(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*)@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/.test(email);
    }
    return true;
});


var mobile = $("#id_mobile").val();
jQuery.validator.addMethod('check_mobile', function(mobile) {
    return /[0-9]{10}/.test(mobile);
});

$.validator.addMethod("mobile_check_exist", function(mobile) {
    var response = check_mobile(mobile);
    return response;
});


$('#registerForm').validate({
    rules: {
        password: {
          minlength: 6,
          maxlength: 30,
          required: true,
//          check_lower: true,
//          check_upper: true,
//          check_digit: true,
        },
        conf_password: {
          required: true,
          equalTo: "#id_password",
        },
        name: {
          required: true,
          maxlength: 100,
        },
        mobile: {
          minlength: 10,
          maxlength: 10,
          required: true,
          check_mobile: true,
//          mobile_check_exist: true,
        },
        email: {
          maxlength: 100,
//          required: true,
          email_value_pattern: true,
        },
        village: {
          required: true,
        },
        area: {
          required: true,
        },
        answer: {
          maxlength: 100,
        },
    },
    messages: {
        password: {
//            check_lower: "Password requires at least one lowercase letter",
//            check_upper: "Password requires at least one uppercase letter",
//            check_digit: "Password requires at least one digit",
            minlength: "Password required at least 6 characters",
            maxlength: "Password must be within 30 characters",
            required: "Password is required",
        },
        email: {
            email_value_pattern: "Please enter a valid email address",
            maxlength: "Email must be within 100 characters",
            required: "Email is required",
        },
        name: {
            maxlength: "Name must be within 100 characters",
            required: "Name is required",
        },
        mobile: {
            required: "Mobile number is required",
            minlength: "Mobile number must be 10 digit",
            maxlength: "Mobile number must be 10 digit",
            check_mobile: "Mobile number is not valid",
            mobile_check_exist: "A user already registered with this mobile number",
        },
        conf_password: {
            required: "Confirm password is required",
            equalTo: "Password must be same",
            minlength: "Confirm Password required at least 6 characters",
            maxlength: "Confirm Password must be within 30 characters",
        },
        village: {
            required: "Village required! If your village is not found, our service has not yet started there",
        },
        area: {
            required: "Area required! If your area is not found, our service has not yet started there",
        },
        answer: {
            required: "Answer is required!",
            maxlength: "Answer must be within 100 characters",
        },
    },

    errorContainer : $('#errorContainer'),
    errorLabelContainer : $('#errorContainer ul'),
    wrapper : 'li',

    highlight: function(element) {
//        $('.panel100').show();
        var id_attr = "#" + $(element).attr("id");
        $(id_attr).css("border","1px solid #af2206");//more efficient
    },
    unhighlight: function(element) {
        var id_attr = "#" + $(element).attr("id");
        $(id_attr).css("border","1px solid #00940f"); //more efficient
    },
});

$("#id_security_question").change( function(){
    $("#id_answer").prop('required', false);
    if($(this).val()){
        $("#id_answer").prop('required', true);
    }
});

$('#registerForm').submit( function(){
    $("#errorContainerTwo").empty();
    $("#errorContainerTwo").hide();
    $("#divIdError").hide();
    if(!$("#id_email").val() && !$("#id_security_question").val()){
        $("#errorContainerTwo").append('<ul><li><label class="error">Either email or security question is required!</label></li></ul>');
        $("#divIdError").show();
        $("#errorContainerTwo").show();
        is_common_validation = true;
        return false;
    }
});

$('input').keypress(function(){
    if ($('#errorContainer').css('display') == 'none') {
         $('.panel100').hide();
    }
//    else{
//        $('.panel100').show();
//    }
});

$('input').change(function(){
    if ($('#errorContainer').css('display') == 'none') {
         $('.panel100').hide();
    }
//    else{
//        $('.panel100').show();
//    }
});

$('select').change(function(){
    if ($('#errorContainer').css('display') == 'none') {
         $('.panel100').hide();
    }
//    else{
//        $('.panel100').show();
//    }
});

$("#id_mobile").change( function(){
    if(is_common_validation){
//        console.log("No validation");
    }else{
        $("#errorContainerTwo").empty();
        $("#errorContainerTwo").hide();
        $("#divIdError").hide();
    }
    var mobile_number = $(this).val();
    var is_valid = check_mobile(mobile_number);
    if(!is_valid){
        $("#errorContainerTwo").append('<ul><li><label class="error">A user already registered with this mobile number!</label></li></ul>');
        $("#divIdError").show();
        $("#errorContainerTwo").show();
        $(this).css("border","1px solid #af2206");
        $(this).focus();
    }else{
        if(is_common_validation){
            $("#errorContainerTwo").html('<ul><li><label class="error">Either email or security question is required!</label></li></ul>');
        }else{
            $("#errorContainerTwo").empty();
            $("#errorContainerTwo").hide();
            $("#divIdError").hide();
        }
    }
});

$("#id_email").change( function(){
    if($(this).val()){
        if(is_common_validation){
            $("#errorContainerTwo").empty();
            $("#errorContainerTwo").hide();
            $("#divIdError").hide();
            is_common_validation = false;
        }
    }
});

$("#id_security_question").change( function(){
    if($(this).val()){
        if(is_common_validation){
            $("#errorContainerTwo").empty();
            $("#errorContainerTwo").hide();
            $("#divIdError").hide();
            is_common_validation = false;
        }
    }
});

function check_mobile(mobile){
    var status = true;
    $.ajax({
        type: 'GET',
        dataType : 'JSON',
        url:  '/check-mobile',
        async:  false,
        data:{
             mobile: JSON.stringify(mobile),
        },
        success:function(data){
//            console.log(data);
            if(data['status'] == 'FAILED'){
                status = false;
            }
            if(data['status'] == 'SYSTEM-FAILED'){
                console.log(data['error']);
            }
        }
    });
    return status;
}


$("#id_village").change( function(){
    $.ajax({
        type: 'GET',
        dataType : 'JSON',
        url:  '/get-area',
        async:  false,
        data:{
             village_id: JSON.stringify($("#id_village").val()),
        },
        success:function(data){
//            console.log(data);
            $("#id_area").empty();
            if(data['status'] == 'SUCCESS'){
                if(data.data.length){
                    var str = "";
                    for(var i=0; i<data.data.length; i++){
                        str += '<option value="'+data.data[i].id+'">'+data.data[i].name+'</option>';
                    }
                    $("#id_area").append(str);
                }else{
                    var str = '<option value="">Choose your locality/area</option>';
                    $("#id_area").append(str);
                }
            }else{
                var str = '<option value="">Choose your locality/area</option>';
                $("#id_area").append(str);
            }
        }
    });
});

//called when key is pressed in textbox
$("#id_mobile").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        return false;
    }
});
