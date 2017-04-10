$(function () {

    var form = $('#payment_form > form');

    var handler = StripeCheckout.configure({
        key: 'pk_test_XSL2saGHkUJcJkOTk8PtVcwQ',
        image: 'https://stripe.com/img/documentation/checkout/marketplace.png',
        locale: 'auto',
        token: function (token) {
            // You can access the token ID with `token.id`.
            // Get the token ID to your server-side code for use.
            $('#id_stripe_token').val(token.id);
            form.submit();


        }
    });

    form.submit(function (e) {
        if($('#id_stripe_token').val()){
            return;
        }
        // Open Checkout with further options:
        handler.open({
            name: 'FOMO Music Store',
            description: 'FOMO Instrument',
        });
        e.preventDefault();
    });

    // Close Checkout on page navigation:
    window.addEventListener('popstate', function () {
        handler.close();
    });

});