
$(document).ready( function(){

//    $(".item_price").change( function(){
//        var price_list = $('.item_price').map((_,el) => el.value).get();
////        console.log(price_list)
//    //        var array = String(price_list).match(/\d+(?:\.\d+)?/g).map(Number);
//        var sum = 0.0;
//        for( var i=0; i<price_list.length; i++){
//            if(price_list[i]){
//                sum = sum + parseFloat(price_list[i]);
//            }
//        }
//        $("#id_total_price").text(sum+"/-");
//        $("#id_total").val(sum);
//    });

    $(".cam-img-svg").show();
    $(".upload-text").show();
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
});

function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    console.log(replacement);
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function cloneMore(selector, prefix) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name');
        if(name) {
            name = name.replace('-' + (total-1) + '-', '-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('');
        }
    });

    total++;

    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    var conditionRow = $('.form-row:not(:last)');
    conditionRow.find('.add-form-row')
    .removeClass('btn-success').addClass('btn-danger')
    .removeClass('add-form-row').addClass('remove-form-row')
    .html('-');
    return false;
}

function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1){
        btn.closest('.form-row').remove();
        var forms = $('.form-row');
        console.log(forms.length)
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length - 1);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i - 1);
            });
        }
    }
    $(".item_price").trigger('change');
    return false;
}

//$(document).on('click', '.add-form-row', function(e){
//    cloneMore('.form-row:last', 'form');
//    return false;
//});
//
//$(document).on('click', '.remove-form-row', function(e){
//    deleteForm('form', $(this));
//    return false;
//});
