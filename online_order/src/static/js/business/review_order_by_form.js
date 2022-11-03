
$(document).ready(function () {
    $(".messages").fadeOut(4000);
    $(".item_price").change( function(){
        var price_list = $('.item_price').map((_,el) => el.value).get();
    //        var array = String(price_list).match(/\d+(?:\.\d+)?/g).map(Number);
        var sum = 0.0;
        for( var i=0; i<price_list.length; i++){
            if(price_list[i]){
                sum = sum + parseFloat(price_list[i]);
            }
        }
        $("#id_total_price").text(sum+"/-");
        $("#id_total").val(sum);
    });
});