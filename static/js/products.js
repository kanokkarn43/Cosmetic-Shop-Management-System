$(document).ready( function () {

    $('#txt_ProductCode').change (function () {
        var product_code = $(this).val().trim();

        $.ajax({
            url:  '/all_product/detail/' + product_code,
            type:  'get',
            dataType:  'json',
            success: function  (data) {
                $('#txt_ProductCode').val(data.all_products.product_code);
                $('#txt_ProductName').val(data.all_products.product_name);
                $('#txt_Price').val(data.all_products.price);
                $('#txt_SoldNo').val(data.all_products.sold_no);
                $('#txt_Quantity').val(data.all_products.quantity);
                $('#txt_Inventory').val(data.all_products.inventory);
            },
            error: function (xhr, status, error) {
                $('#txt_ProductName').val('');
                $('#txt_Price').val('');
                $('#txt_SoldNo').val('');
                $('#txt_Quantity').val('');
                $('#txt_Inventory').val('');
            }
        });
    });
});

