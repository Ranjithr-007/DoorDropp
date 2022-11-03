var myTimer = null;

$(document).ready( function(){
    $(".messages").fadeOut(4000);
    callMyCount();
    $("#id_otp_value").focus();
});

function ValidatePassKey(tb) {
    if (tb.value.length > 3){
        $("#id_btn_submit").focus();
    }
}

function callMyCount(){
    var arr_otp_time = otp_expire_time.split('.');
    var otp_time = arr_otp_time[0] + arr_otp_time[1].substring(0,3);
    var minutes_different = new Date(parseInt(otp_time)).getMinutes() - new Date().getMinutes();
    console.log('arr_otp_time = ', arr_otp_time);
    console.log('otp_time = ', otp_time);
    console.log('minutes_different = ', minutes_different);

    if(minutes_different > 0  && minutes_different < 6){
        document.getElementById('timer').innerHTML = minutes_different + ":" + '00';
        myTimer = setInterval(startTimer, 1000);
    }else{
        $("#id_btn_submit").prop('disabled', true);
        $("#id_otp_value").prop('disabled', true);
        $("#idOtpText").text('OTP expired! Please resend OTP');
        $("#divIdResend").show();
    }

    function startTimer() {
        var presentTime = document.getElementById('timer').innerHTML;
        var timeArray = presentTime.split(/[:]+/);
        var m = parseInt(timeArray[0]);
        var s = checkSecond((parseInt(timeArray[1]) - 1));
        if(s==59){m=m-1}
        if(m<0 && s==59){
            $("#id_btn_submit").prop('disabled', true);
            $("#id_otp_value").prop('disabled', true);
            $("#idOtpText").text('OTP expired! Please resend OTP');
            $("#divIdResend").show();
            clearTimeout(myTimer);
        }else{
            document.getElementById('timer').innerHTML =  m + ":" + s;
        }
    }

    function checkSecond(sec) {
        if (sec < 10 && sec >= 0) {sec = "0" + sec};
        if (sec < 0) {sec = "59"};
        return sec;
    }
}