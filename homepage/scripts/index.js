$(function() {
    // update the time every 1 seconds
    window.setInterval(function() {
        $('.browser-time').text('The current browser time is ' + new Date() + '.');
    }, 1000);

});