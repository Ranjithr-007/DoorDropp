
$(document).ready( function(){
    $(".profile-pic-2").hide();
    $("#divIdUpload").hide();
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
        $("#divIdUpload").show();
    });
});

var col2 = document.getElementsByClassName("inf_collapse");
for (var i = 0; i < col2.length; i++) {
    col2[i].addEventListener("click", function () {
        this.classList.toggle("inf_clicked");
        var content = this.nextElementSibling;
        console.log(content);
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
}

var coll = document.getElementsByClassName("inf_collapsible");
for (var i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("inf_active");
        var content = this.nextElementSibling;
        if (content.style.display === "block"){
            content.style.display = "none";
        }else{
            content.style.display = "block";
        }
    });
}


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
    return false;
}

$(document).on('click', '.add-form-row', function(e){
    cloneMore('.form-row:last', 'form');
    return false;
});

$(document).on('click', '.remove-form-row', function(e){
    deleteForm('form', $(this));
    return false;
});


$(".by_call").click(function(event){
    $("#primary").attr('href', "tel:+91"+primary);
    if(secondary && secondary != primary){
        $("#secondary").attr('href', "tel:+91"+secondary);
    }
    if(primary != manager && secondary != manager){
        $("#manager").attr('href', "tel:+91"+manager);
    }

    var status = confirm('Are you sure want to Order by Call?');
    if(status){
        $.ajax({
            type: 'GET',
            dataType : 'JSON',
            url:  '/new-order-by-call',
            async:  false,
            data:{
                 business_id: JSON.stringify($("#id_business_by_call").val()),
            },
            success:function(data){
                console.log(data);
                if(data['status'] == 'SUCCESS'){
                    var url = window.location.href;
//                    var arr_url = url.split('/');
//                    console.log(arr_url);
//                    var new_url = arr_url[0]+'/'+arr_url[1]+'/'+arr_url[2]+'/home/'+data['area_id']+'/';
//                    console.log(new_url);
//                    event.preventDefault();
//                    window.location.replace(new_url);
//                    window.location.reload();
//                    console.log(new_url);
//                    window.location.assign(new_url);
                }else{
                    console.log("failed");
                }
            }
        });
    }else{
        $(this).attr('href', '#');
    }
});
