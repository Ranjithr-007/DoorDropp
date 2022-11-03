
var intervalID = null

$(document).ready(function () {
    $(".messages").fadeOut(4000);

    intervalID = setInterval(getNewOrders, 10000);
    // clearInterval(intervalID); // Will clear the timer.

});

function getNewOrders(){
    $.get("/get-new-delivery-orders", function(data, status){
        if(data['status'] == 'SUCCESS'){
//            console.log(data['all_open_orders']);
//            console.log(data['all_processed_orders']);
            if(data['all_open_orders'].length){
                $("#divIdOpenDelivery").text('');
                var str_open_order = '';
                for(var i=0; i<data['all_open_orders'].length; i++){
                    var str_inside_order = '';
                    for(var j=0; j<data['all_open_orders'][i]['orders'].length; j++){
                        str_inside_order = str_inside_order + '<div class="id-shop">\n'+
                            '<div class="row">\n'+
                                '<div class="col-6 col-lg-6">\n'+
                                    '<a href="'+data['all_open_orders'][i]['orders'][j]['order_info_link']+'">\n'+
                                        '<h4>'+data['all_open_orders'][i]['orders'][j]['order_id']+'</h4>\n'+
                                    '</a>\n'+
                                '</div>\n'+
                                '<div class="col-6 col-lg-6">\n'+
                                    '<h4>'+data['all_open_orders'][i]['orders'][j]['business']+'</h4>\n'+
                                '</div>\n'+
                            '</div>\n'+
                        '</div>';
                    }
                    str_open_order = str_open_order + '<div class="today-dl-txt">\n' +
                        '<div class="row">\n'+
                            '<div class="col-6 col-lg-6">\n'+
                                '<div class="lable-section">\n'+
                                    '<h4><strong>User :</strong> '+data['all_open_orders'][i]["common_user"]+'</h4>\n'+
                                '</div>\n'+
                            '</div>\n'+
                            '<div class="col-6 col-lg-6">\n'+
                                '<div class="lable-section-1">\n'+
                                    '<h4><strong>Area :</strong> '+data['all_open_orders'][i]["area"]+'</h4>\n'+
                                '</div>\n'+
                            '</div>\n'+
                            '<div class="col-6 col-lg-6">\n'+
                                '<div class="lable-section">\n'+
                                    '<h4><strong>Mobile :</strong> '+data['all_open_orders'][i]["mobile"]+'</h4>\n'+
                                '</div>\n'+
                            '</div>\n'+
                            '<div class="col-6 col-lg-6">\n'+
                                '<div class="lable-section-1">\n'+
                                    '<h4><strong>Land Mark :</strong> '+data['all_open_orders'][i]["landmark"]+'</h4>\n'+
                                '</div>\n'+
                            '</div>\n'+
                            '<div class="col-12 col-lg-12">\n'+
                                '<div class="lable-section">\n'+
                                    '<h4><strong>Address :</strong> '+data['all_open_orders'][i]["address"]+'</h4>\n'+
                                '</div>\n'+
                            '</div>\n'+
                        '</div>\n'+
                    '</div>\n'+
                    '<div class="id-status-section">\n'+str_inside_order+
                        '<p>Status : Order is open</p>\n'+
                        '<hr>\n'+
                        '<div class="row detais-btn">\n'+
                            '<div class="col-12">\n'+
                                '<a href="'+data['all_open_orders'][i]["url"]+'" onclick="return confirm("Are you sure want to take this delivery?")">\n'+
                                    '<button class="btn btn-primary" type="button">I will deliver this order</button>\n'+
                                '</a>\n'+
                            '</div>\n'+
                        '</div>\n'+
                    '</div>';
                }
                $("#divIdOpenDelivery").append(str_open_order);
            }
            if(data['all_processed_orders'].length){
                $("#divIdDeliveryProcessing").text('');
                var str_processing_order = '';
                for(var i=0; i<data['all_processed_orders'].length; i++){
                    var str_inside_processed_order = '';
                    for(var j=0; j<data['all_processed_orders'][i]['orders'].length; j++){
                        str_inside_processed_order = str_inside_processed_order + '<div class="id-shop">\n'+
                            '<div class="row">\n'+
                                '<div class="col-3 col-lg-3">\n'+
                                    '<a href="'+data['all_processed_orders'][i]['orders'][j]['order_info_link']+'">\n'+
                                        '<h4>'+data['all_processed_orders'][i]['orders'][j]['order_id']+'</h4>\n'+
                                    '</a>\n'+
                                '</div>\n'+
                                '<div class="col-4 col-lg-4">\n'+
                                    '<h4>'+data['all_processed_orders'][i]['orders'][j]['business']+'</h4>\n'+
                                '</div>\n'+
                                '<div class="col-3 col-lg-3">\n'+
                                    '<h4>'+data['all_processed_orders'][i]['orders'][j]['order_total_items']+' Items</h4>\n'+
                                '</div>\n'+
                                '<div class="col-2 col-lg-2">'+data['all_processed_orders'][i]['orders'][j]['element']+'</div>\n'+
                            '</div>\n'+
                        '</div>';
                    }

                    str_processing_order = str_processing_order + '<div class="today-dl-txt" id="ongoing_'+data['all_processed_orders'][i]["id"]+'">\n' +
                        '<div class="row">\n'+
                            '<div class="col-6 col-lg-6">\n'+
                                '<div class="lable-section">\n'+
                                    '<h4><strong>User :</strong> '+data['all_processed_orders'][i]["common_user"]+'</h4>\n'+
                                '</div>\n'+
                            '</div>\n'+
                            '<div class="col-6 col-lg-6">\n'+
                                '<div class="lable-section-1">\n'+
                                    '<h4><strong>Area :</strong> '+data['all_processed_orders'][i]["area"]+'</h4>\n'+
                                '</div>\n'+
                            '</div>\n'+
                            '<div class="col-6 col-lg-6">\n'+
                                '<div class="lable-section">\n'+
                                    '<h4><strong>Mobile :</strong> '+data['all_processed_orders'][i]["mobile"]+'</h4>\n'+
                                '</div>\n'+
                            '</div>\n'+
                            '<div class="col-6 col-lg-6">\n'+
                                '<div class="lable-section-1">\n'+
                                    '<h4><strong>Land Mark :</strong> '+data['all_processed_orders'][i]["landmark"]+'</h4>\n'+
                                '</div>\n'+
                            '</div>\n'+
                            '<div class="col-12 col-lg-12">\n'+
                                '<div class="lable-section">\n'+
                                    '<h4><strong>Address :</strong> '+data['all_processed_orders'][i]["address"]+'</h4>\n'+
                                '</div>\n'+
                            '</div>\n'+
                        '</div>\n'+
                    '</div>\n'+
                    '<div class="id-status-section">\n'+str_inside_processed_order+
                        '<p>Status : Order is Processing..</p>\n'+
                        '<hr>\n'+
                        '<div class="row detais-btn">\n'+
                            '<div class="col-12">\n'+
                                '<a href="'+data['all_processed_orders'][i]["url"]+'">\n'+
                                    '<button class="btn btn-primary" type="button">Details</button>\n'+
                                '</a>\n'+
                            '</div>\n'+
                        '</div>\n'+
                    '</div>';
                }
                $("#divIdDeliveryProcessing").append(str_processing_order);
            }
        }
    });
}