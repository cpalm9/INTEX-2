$(function(){

    var productType = $('#id_type');

    $('#id_serial_number').closest('p').hide();

    $('#id_type').change(function (event) {
        var value = productType.val();

        if (value == 'bulk'){
            $('#id_reorder_qty').closest('p').show();
            $('#id_reorder_trigger').closest('p').show();
            $('#id_quantity').closest('p').show();
            $('#id_serial_number').closest('p').hide();

        }
        else if (value == 'unique'){
            $('#id_serial_number').closest('p').show();
            $('#id_reorder_qty').closest('p').hide();
            $('#id_reorder_trigger').closest('p').hide();
            $('#id_quantity').closest('p').hide();
        }
        else{
            $('#id_serial_number').closest('p').show();
            $('#id_reorder_qty').closest('p').hide();
            $('#id_reorder_trigger').closest('p').hide();
            $('#id_quantity').closest('p').show();
        }


    })

});