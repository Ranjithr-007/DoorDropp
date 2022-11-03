
$(document).ready( function(){
    resetAll();
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
        url:  '/edit-business',
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
                $("#id_secondary_mobile").val(data['secondary_mobile']);
                $("#id_manager_mobile").val(data['manager_mobile']);
                $("#id_payment_percentage").val(data['payment_percentage']);
                $("#id_manager").val(data['manager']);
                $("#id_about").val(data['about']);
                $("#id_area_specified").val(data['area_specified']);
                $("#id_category").val(data['category']);
                $("#id_key").val(data['id']);

                document.getElementById('divIdContent').scrollIntoView();
        }
    });
}

function resetAll(){
    document.getElementById("idForm").reset();
    $("#idSave").text("Save");
    $("#id_key").val("");
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

//called when key is pressed in textbox
$("#id_secondary_mobile").keypress(function (e) {
 //if the letter is not digit then display error and don't type anything
 if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
    //display error message
    $("#errmsg1").html("Digits Only").show().fadeOut("slow");
    return false;
 }
});

//called when key is pressed in textbox
$("#id_manager_mobile").keypress(function (e) {
 //if the letter is not digit then display error and don't type anything
 if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
    //display error message
    $("#errmsg2").html("Digits Only").show().fadeOut("slow");
    return false;
 }
});


