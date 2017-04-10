$(function() {

    $('#cart_count_span').html(${ request.user.get_cart_count() });

    $('#buy_now_form').ajaxForm({
        target: '#purchase_container',
    });


});