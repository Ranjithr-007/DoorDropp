
$(document).ready( function(){
    $(".profile-pic-2").hide();
    var readURL = function (input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('.profile-pic-2').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $('.file-upload-wrpr-2').on('click', function () {
        $('#file-upload').click();
    });
    $("#file-upload").on('change', function () {
        readURL(this);
        $(".cam-img-svg").hide();
        $(".upload-text").hide();
        $(".profile-pic-2").show();

    });
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
    $(".cam-img-svg").show();
    $(".upload-text").show();
    $(".profile-pic-2").hide();
    $.ajax({
        type: 'GET',
        dataType : 'JSON',
        url:  '/edit-payment-method',
        async:  false,
        data:{
             id: JSON.stringify(id),
        },
        success:function(data){

//                console.log(data);
                $("#id_name").val(data['name']);
                $("#id_is_upi").prop('checked', data['is_upi']);

                if(data['qr_code']){
                    $('.profile-pic-2').attr('src', data['qr_code'])
                    $(".cam-img-svg").hide();
                    $(".upload-text").hide();
                    $(".profile-pic-2").show();
                }
                $("#id_key").val(data['id']);

                document.getElementById('divIdContent').scrollIntoView();
        }
    });
}

function resetAll(){
    document.getElementById("idForm").reset();
    $("#idSave").text("Save");
    $("#id_key").val("");
    $(".cam-img-svg").show();
    $(".upload-text").show();
    $(".profile-pic-2").hide();
}

