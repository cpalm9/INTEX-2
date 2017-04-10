$(function() {


    console.log('hello world');

    $('.deleteLink').click(function(event) {
        //don't do the normal behavior of the event
        event.preventDefault();

        //Find link to reference correct uid
        var link = $(this).attr('href');
        $('#useryesBtn').attr('href', link);


        //Show a popup
        $('#usermyModal').modal();

    });

});