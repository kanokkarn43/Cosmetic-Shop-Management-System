$(document).ready( function () {

    $('#txt_OrderID').change (function () {
        var order_id = $(this).val().trim();

        $.ajax({
            url:  '/all_order/detail/' + order_id,
            type:  'get',
            dataType:  'json',
            success: function  (data) {
                $('#txt_OrderID').val(data.all_orders.order_id);
                $('#txt_OrderDate').val(data.all_orders.order_date);
                $('#txt_Contact').val(data.all_orders.contact);
                $('#txt_Amount').val(data.all_orders.amount);
            },
            error: function (xhr, status, error) {
                $('#txt_OrderDate').val('');
                $('#txt_Contact').val(''); 
                $('#txt_Amount').val('');
            } 
        });
    });

});
