
$(document).ready( function(){

});

var mobile = $("#id_mobile").val();
jQuery.validator.addMethod('check_mobile', function(mobile) {
    return /[0-9]{10}/.test(mobile);
});

var sec_mobile = $("#id_secondary_mobile").val();
jQuery.validator.addMethod('check_sec_mobile', function(sec_mobile) {
    if(sec_mobile){
        return /[0-9]{10}/.test(sec_mobile);
    }
    else{
        return true;
    }
});

var manager_mobile = $("#id_manager_mobile").val();
jQuery.validator.addMethod('check_manager_mobile', function(manager_mobile) {
    if(sec_mobile){
        return /[0-9]{10}/.test(manager_mobile);
    }
    else{
        return true;
    }
});

var account_no = $("#id_account_no").val();
jQuery.validator.addMethod('check_account_number', function(account_no) {
    if(account_no){
        return /[0-9]/.test(account_no);
    }else{
        return true;
    }
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
        manager: {
          required: false,
          maxlength: 100,
        },
        address: {
          required: false,
          maxlength: 1000,
        },
        manager_mobile: {
          required: false,
          minlength: 10,
          maxlength: 10,
          check_manager_mobile: true,
        },
        secondary_mobile: {
          required: false,
          minlength: 10,
          maxlength: 10,
          check_sec_mobile: true,
        },
        upi_id: {
          required: false,
          maxlength: 50,
        },
        account_no: {
          required: false,
          check_account_number: true,
          maxlength: 30,
        },
        ifsc: {
          required: false,
          maxlength: 20,
        },
        about: {
          required: false,
          maxlength: 1000,
        },
    },
    messages: {
        name: {
            maxlength: "Name must be within 100 characters",
            required: "Name is required",
        },
        email: {
            email_value_pattern: "Email is not valid",
        },
        mobile: {
            required: "Mobile number is required",
            minlength: "Mobile number must be 10 digit",
            maxlength: "Mobile number must be 10 digit",
            check_mobile: "Mobile number is not valid",
        },
        manager: {
            maxlength: "Manager name must be within 100 characters",
        },
        address: {
            maxlength: "Address can't exceed 1000 characters",
        },
        about: {
            maxlength: "About can't exceed 1000 characters",
        },
        manager_mobile: {
            minlength: "Manager mobile number must be 10 digit",
            maxlength: "Manager mobile number must be 10 digit",
            check_manager_mobile: "Manager mobile number is not valid",
        },
        upi_id: {
            maxlength: "UPI ID can't exceed 50 characters",
        },
        account_no: {
            maxlength: "Account number can't exceed 30 characters",
            check_account_number: "Account number is not valid",
        },
        ifsc: {
            maxlength: "IFSC can't exceed 20 characters",
        },
        secondary_mobile: {
            minlength: "Secondary mobile number must be 10 digit",
            maxlength: "Secondary mobile number must be 10 digit",
            check_sec_mobile: "Secondary mobile number is not valid",
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

//called when key is pressed in textbox
$("#id_mobile").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        return false;
    }
});

//called when key is pressed in textbox
$("#id_secondary_mobile").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        return false;
    }
});

//called when key is pressed in textbox
$("#id_manager_mobile").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        return false;
    }
});
