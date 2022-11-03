
var intervalID = null

$(document).ready(function () {
    $(".messages").fadeOut(4000);

    intervalID = setInterval(getNewOrders, 10000);
    // clearInterval(intervalID); // Will clear the timer.

});

function getNewOrders(){
    $.get("/get-new-orders", function(data, status){
        if(data['status'] == 'SUCCESS'){
//            console.log(data['all_open_orders']);
//            console.log(data['all_placed_orders']);
            if(data['all_open_orders'].length){
                $("#divIdToProcess").text('');
                var str_open_order = '';
                for(var i=0; i<data['all_open_orders'].length; i++){
                    str_open_order = str_open_order + '<a href="'+data['all_open_orders'][i]["url"]+'">\n' +
                        '<div class="business-order">\n'+
                            '<div class="row">\n'+
                                '<div class="col-6 col-lg-6"><h5>'+data['all_open_orders'][i]["order_id"]+'</h5></div>\n' +
                                '<div class="col-6 col-lg-6"><h6>'+data['all_open_orders'][i]["common_user"]+'</h6></div>\n' +
                                '<div class="col-6 col-lg-6"><h3>'+data['all_open_orders'][i]["order_type_text"]+'</h3></div>\n' +
                                '<div class="col-6 col-lg-6"><p>'+data['all_open_orders'][i]["created"]+'</p></div>\n' +
                                '<div class="col-12 col-lg-12"><span>'+data['all_open_orders'][i]["status_text"]+'</span></div>\n' +
                            '</div>\n' +
                        '</div>\n' +
                        '<hr>\n' +
                    '</a>';
                }
                $("#divIdToProcess").append(str_open_order);
            }
            if(data['all_placed_orders'].length){
                $("#divIdConfirmed").text('');
                var str_open_order = '';
                for(var i=0; i<data['all_placed_orders'].length; i++){
                    str_open_order = str_open_order + '<a href="'+data['all_placed_orders'][i]["url"]+'">\n' +
                        '<div class="business-order">\n'+
                            '<div class="row">\n'+
                                '<div class="col-6 col-lg-6"><h5>'+data['all_placed_orders'][i]["order_id"]+'</h5></div>\n' +
                                '<div class="col-6 col-lg-6"><h6>'+data['all_placed_orders'][i]["common_user"]+'</h6></div>\n' +
                                '<div class="col-6 col-lg-6"><h3>'+data['all_placed_orders'][i]["order_type_text"]+'</h3></div>\n' +
                                '<div class="col-6 col-lg-6"><p>'+data['all_placed_orders'][i]["created"]+'</p></div>\n' +
                                '<div class="col-12 col-lg-12"><span>'+data['all_placed_orders'][i]["status_text"]+'</span></div>\n' +
                            '</div>\n' +
                        '</div>\n' +
                    '</a>\n' +
                    '<div class="row">\n' +
                        '<div class="process-btn text-center">\n' +
                            '<button class="btn btn-primary" type="button" onclick="window.location.assign(\''+data['all_placed_orders'][i]["button_url"]+'\')">Packed</button>\n' +
                        '</div>\n' +
                    '</div>\n' +
                    '<hr>';
                }
                $("#divIdConfirmed").append(str_open_order);
            }
        }
    });
}