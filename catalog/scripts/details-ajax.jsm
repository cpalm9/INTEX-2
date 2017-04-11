$(function() {

    $('#simpleCart_quantity').html(${ request.user.get_cart_count() });

    $('#simpleCart_total').html(${ request.user.get_cart_total() });


    $('#buy_now_form').ajaxForm({
        target: '#purchase_container',
    });


});