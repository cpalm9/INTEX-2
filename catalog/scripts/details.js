$(function() {

    $('#buy_now_form').ajaxForm({
        target: '#purchase_container',
    });


    $('.modalPics').click(function(event) {
        //don't do the normal behavior of the event
        event.preventDefault();

        //Find link to reference correct pid
        var link = $(this).attr('href');
        $('#yesBtn').attr('href', link);

        //Show a popup
        $('#myModal').modal();
    });

    var images = $('.modal-body img');
    images.hide();
    $('#nextBtn').click(function () {
        current = images.filter(':visible');
        current.hide();
        current = current.next('img');
        if (current.length == 0) {
            current = $(images[0]);
        }
        current.show();
    }) .trigger('click');

    images.hide();
    $('#previousBtn').click(function () {
        current = images.filter(':visible');
        current.hide();
        current = current.prev('img');
        if (current.length == 0) {
            current = $(images[2]);
        }
        current.show();
    }) .trigger('click');


});