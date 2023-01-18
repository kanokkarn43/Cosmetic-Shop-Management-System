var ROW_NUMBER = 5;

Date.prototype.addDays = function(days) {
    var date = new Date(this.valueOf());
    date.setDate(date.getDate() + days); 
    return date;
}

$(document).ready( function () {

    /* create datepicker */
    $("#txt_OrderDate").datepicker({ 
        dateFormat: 'dd/mm/yy' 
    });
    
    $('#btn_OrderDate').click(function() {
        $('#txt_OrderDate').datepicker('show');
    });

    /* table add delete row */
    var $TABLE = $('#div_table');
    $('.table-add').click(function () {
        var $clone = $TABLE.find('tr.hide').clone(true).removeClass('hide table-line');
        $TABLE.find('tbody').append($clone);
        re_order_no();
    });

    $('.table-remove').click(function () { 
        $(this).parents('tr').detach();

        if ($('#table_main tr').length <= 9) {
            $('.table-add').click();
        }
        re_order_no();
        re_calculate_total_price();
    });

    // Search Contact(Member)     
    $('#txt_Contact').change (function () {
        var contact = $(this).val().trim();

        $.ajax({
            url:  '/member/detail/' + contact,
            type:  'get',
            dataType:  'json',
            success: function  (data) {
                $('#txt_Contact').val(data.members.contact);
                $('#txt_MemberName').val(data.members.member_name);
                
            },
            error: function (xhr, status, error) {
                $('#txt_MemberName').val('');
                
            }
        });
    });
 
    /* search product code ในตาราง */ 
    $('.search_product_code').click(function () {
        $p_code = $(this).parents('td').children('span').html();
        $(this).parents('tr').find('.order_no').html('*');

        $.ajax({
            url:  '/all_product/list',
            type:  'get',
            dataType:  'json',
            success: function  (data) {
                let rows =  '';
                var i = 1;
                data.all_products.forEach(all_product => {
                    rows += `
                    <tr class="d-flex">
                        <td class='col-1'>${i++}</td>
                        <td class='col-3'><a class='a_click' href='#'>${all_product.product_code}</a></td>
                        <td class='col-5'>${all_product.product_name}</td>
                        <td class='col-3'></td>
                        <td class='hide'>${all_product.price}</td>
                    </tr>`;

                });
                $('#table_modal > tbody').html(rows);

                $('#model_header_1').text('Product Code');
                $('#model_header_2').text('Product Name');
                $('#model_header_3').text('Note');
            },
        });
        // open popup
        $('#txt_modal_param').val('product_code');
        $('#modal_form').modal();
    });

    /* Popup ตอนเสิร์ชเมมเบอร์ */ 
    $('.search_customer_code').click(function () {
        $.ajax({
            url:  '/member/list',
            type:  'get',
            dataType:  'json',
            success: function  (data) {
                let rows =  '';
                var i = 1;
                data.members.forEach(member => {
                    rows += `
                    <tr class="d-flex">
                        <td class='col-1'>${i++}</td>
                        <td class='col-3'><a class='a_click' href='#'>${member.contact}</a></td>
                        <td class='col-5'>${member.member_name}</td>
                        <td class='col-3'></td>
                        <td class='hide'></td>
                    </tr>`;
                });
                $('#table_modal > tbody').html(rows);

                $('#model_header_1').text('Contact');
                $('#model_header_2').text('Member Name');
                $('#model_header_3').text('Note');

            },
        });        
        // open popup
        $('#txt_modal_param').val('contact');
        $('#modal_form').modal();
    });

    $('table').on('focusin', 'td[contenteditable]', function() {
        $(this).data('val', $(this).html());
    }).on('input', 'td[contenteditable]', function() {
        //re_calculate_total_price();
    }).on('keypress', 'td[contenteditable]', function (e) {
        if (e.keyCode == 13) {
            return false;
        }
    }).on('focusout', 'td[contenteditable]', function() {
        var prev = $(this).data('val');
        var data = $(this).html();
        if (!numberRegex.test(data)) {
            $(this).text(prev);
        } else {
            $(this).data('val', $(this).html());
        }
        re_calculate_total_price();
    });

    // return from modal (popup)
    $('body').on('click', 'a.a_click', function() {
        //console.log($(this).parents('tr').html());
        //console.log($(this).parents('tr').find('td:nth-child(1)').html());
        var code = $(this).parents('tr').find('td:nth-child(2)').children().html();
        var name = $(this).parents('tr').find('td:nth-child(3)').html();
        var note = $(this).parents('tr').find('td:nth-child(4)').html();
        var option = $(this).parents('tr').find('td:nth-child(5)').html();

        if ($('#txt_modal_param').val() == 'product_code') {
            $("#table_main tbody tr").each(function() {
                if ($(this).find('.order_no').html() == '*') {
                    $(this).find('.project_code_1 > span').html(code);
                    $(this).find('.product_name').html(name);
                    $(this).find('.price').html(option); 
                    $(this).find('.quantity').html("1");
                }
            });
            
            re_calculate_total_price();
        } else if ($('#txt_modal_param').val() == 'contact') {
            $('#txt_Contact').val(code);
            $('#txt_MemberName').val(name);
        } else if ($('#txt_modal_param').val() == 'order_id') {
            $('#txt_OrderID').val(code);
            $('#txt_OrderDate').val(name);
            $('#txt_Contact').val(note);
            $('#txt_Contact').change();

            get_invoice_detail(code);
        }

        $('#modal_form').modal('toggle');
    });

    // detect modal close form
    $('#modal_form').on('hidden.bs.modal', function () {
        re_order_no();
    });

    //disable_ui();
    reset_form();

    re_order_no();
    re_calculate_total_price();

    $('#btnNew').click(function () {
        reset_form();

        re_order_no();
        re_calculate_total_price();
    });
    
    $('#btnSave').click(function () {

        var contact = $('#txt_MemberName').val().trim();
        if (contact == '') {
            alert('กรุณาระบุ Member');
            $('#txt_Contact').focus();
            return false;
        }
        var order_date = $('#txt_OrderDate').val().trim();
        if (!dateRegex.test(order_date)) {
            alert('กรุณาระบุวันที่ ให้ถูกต้อง');
            $('#txt_OrderDate').focus();
            return false;
        }
        if ($('#txt_OrderID').val() == '<new>') {
            var token = $('[name=csrfmiddlewaretoken]').val();
                  
            $.ajax({
                url:  '/all_order/create',
                type:  'post',
                data: $('#form_invoice').serialize() + "&lineitem=" +lineitem_to_json(),
                headers: { "X-CSRFToken": token },
                dataType:  'json',
                success: function  (data) {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        $('#txt_OrderID').val(data.all_order.order_id)
                        alert('บันทึกสำเร็จ');
                    }                    
                },
            });  
        } else {
            var token = $('[name=csrfmiddlewaretoken]').val();
            console.log($('#form_invoice').serialize());
            console.log(lineitem_to_json());
            $.ajax({
                url:  '/all_order/update/' + $('#txt_OrderId').val(),
                type:  'post',
                data: $('#form_invoice').serialize() + "&lineitem=" +lineitem_to_json(),
                headers: { "X-CSRFToken": token },
                dataType:  'json',
                success: function  (data) {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        alert('บันทึกสำเร็จ');
                    }
                },
            }); 
        }
        
    });
    
    $('#btnPdf').click(function () {
        if ($('#txt_OrderID').val() == '<new>') {
            alert ('กรุณาระบุ Order ID');
            return false;
        }
        window.open('/sale/pdf/' + $('#txt_OrderID').val());
    });


});

function lineitem_to_json () {
    var rows = [];
    var i = 0;
    $("#table_main tbody tr").each(function(index) {
        if ($(this).find('.project_code_1 > span').html() != '') {
            rows[i] = {}; 
            rows[i]["item_no"] = (i+1);
            rows[i]["product_code"] = $(this).find('.project_code_1 > span').html();
            rows[i]["product_name"] = $(this).find('.product_name').html();
            rows[i]["price"] = $(this).find('.price').html();
            rows[i]["quantity"] = $(this).find('.quantity').html();
            rows[i]["product_total"] = $(this).find('.product_total').html();
            i++;
        }
    });
    var obj = {};
    obj.lineitem = rows;
    //console.log(JSON.stringify(obj));

    return JSON.stringify(obj);
}

function get_invoice_detail (order_id) {
    $.ajax({
        url:  '/all_order/detail/' + encodeURIComponent(order_id),
        type:  'get',
        dataType:  'json',
        success: function  (data) {
            //console.log(data.invoicelineitem.length);

            reset_table();
            for(var i=ROW_NUMBER;i<data.orderlineitem.length;i++) {
                $('.table-add').click();
            }
            var i = 0;
            $("#table_main tbody tr").each(function() {
                if (i < data.orderlineitem.length) {
                    $(this).find('.project_code_1 > span').html(data.orderlineitem[i].product_code);
                    $(this).find('.product_name').html(data.orderlineitem[i].product_code__name);
                    $(this).find('.price').html(data.orderlineitem[i].price);
                    $(this).find('.quantity').html(data.orderlineitem[i].quantity);
                }
                i++;
            });
            re_calculate_total_price();
        },
    });
}

function re_calculate_total_price () {
    var total_price = 0;
    $("#table_main tbody tr").each(function() {

        var product_code = $(this).find('.project_code_1 > span').html();
        //console.log (product_code);
        var price = $(this).find('.price').html();
        $(this).find('.price').html(((price)));
        var quantity = $(this).find('.quantity').html();
        $(this).find('.quantity').html(parseInt(quantity));
        if (product_code != '') {
                var product_total = price * quantity
            $(this).find('.product_total').html(formatNumber(product_total));
            total_price += product_total;
        }
    });

    $('#lbl_TotalPrice').text(formatNumber(total_price));
    $('#txt_TotalPrice').val($('#lbl_TotalPrice').text());
    
    $('#lbl_Amount').text(formatNumber(total_price * 1));
    $('#txt_Amount').val($('#lbl_Amount').text());
}

function reset_form() {
    $('#txt_OrderID').attr("disabled", "disabled");
    $('#txt_OrderID').val('<new>');

    reset_table();
    
    $('#txt_OrderDate').val(new Date().toJSON().slice(0,10).split('-').reverse().join('/'));

    $('#txt_Contact').val('');
    $('#txt_MemberName').val('');

    $('#lbl_TotalPrice').text('0.00');
   
    $('#lbl_Amount').text('0.00');
}

function reset_table() {
    $('#table_main > tbody').html('');
    for(var i=1; i<= ROW_NUMBER; i++) {
        $('.table-add').click();
    }    
}

function re_order_no () {
    var i = 1;
    $("#table_main tbody tr").each(function() {
        $(this).find('.order_no').html(i);
        i++;
    });
}


function disable_ui () {
    $('#txt_OrderDate').attr("disabled", "disabled");
    $('#btn_OrderDate').attr("disabled", "disabled");
}

function enable_ui () {
    $('#txt_OrderDate').removeAttr("disabled");
    $('#btn_OrderDate').removeAttr("disabled");
}



function formatNumber (num) {
    if (num === '') return '';
    num = parseFloat(num); 
    return num.toFixed(2).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,");
}

function isInt(n){
    return Number(n) === n && n % 1 === 0;
}

function isFloat(n){
    return Number(n) === n && n % 1 !== 0;
}

var dateRegex = /^(?=\d)(?:(?:31(?!.(?:0?[2469]|11))|(?:30|29)(?!.0?2)|29(?=.0?2.(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00)))(?:\x20|$))|(?:2[0-8]|1\d|0?[1-9]))([-.\/])(?:1[012]|0?[1-9])\1(?:1[6-9]|[2-9]\d)?\d\d(?:(?=\x20\d)\x20|$))?(((0?[1-9]|1[012])(:[0-5]\d){0,2}(\x20[AP]M))|([01]\d|2[0-3])(:[0-5]\d){1,2})?$/;
//var numberRegex = /^-?\d+\.?\d*$/;
var numberRegex = /^-?\d*\.?\d*$/
