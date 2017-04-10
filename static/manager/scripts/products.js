$(function() {

    console.log($('.update_button'));

    $('.update_button').click(function() {

        //get product id
        var pid = $(this).attr('data-pid');
        console.log(pid);

        //ask the server for the quantity
        $(this).siblings('.qtyText').load('/manager/products.get_quantity/' + pid);

    });


    $('.deleteLink').click(function(event) {
        //don't do the normal behavior of the event
        event.preventDefault();

        //Find link to reference correct pid
        var link = $(this).attr('href');
        $('#yesBtn').attr('href', link);


        //Show a popup
        $('#myModal').modal();



    });


});