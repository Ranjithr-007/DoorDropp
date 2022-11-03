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

$('form').validate({
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
        conf_password: {
            required: "Confirm password is required",
            equalTo: "Password must be same",
            minlength: "Confirm Password required at least 6 characters",
            maxlength: "Confirm Password must be within 30 characters",
        },
    },

    errorContainer : $('#errorContainer'),
    errorLabelContainer : $('#errorContainer ul'),
    wrapper : 'li',

    highlight: function(element) {
//        $('.panel100').show();
        var id_attr = "#" + $(element).attr("id");
        $(id_attr).removeClass('success-valid').addClass('error-valid');
    },
    unhighlight: function(element) {
        $('.panel100').hide();
        var id_attr = "#" + $(element).attr("id");
        $(id_attr).removeClass('error-valid').addClass('success-valid');
    },
});

$('input').change(function(){
    if ($('#errorContainer').css('display') == 'none') {
         $('.panel100').hide();
    }
//    else{
//        $('.panel100').show();
//    }
});

$('input').keypress(function(){
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

//called when key is pressed in textbox
$("#id_mobile").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        return false;
    }
});