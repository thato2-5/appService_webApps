$(document).ready(function() {
    // Hide loading overlay after page load
    $(window).on('load', function() {
        $('#loading-overlay').fadeOut();
    });

    // Handle click events
    $('#subscribeBtn').click(function() {
        alert('Subscribe button clicked!');
    });

    $('#signInBtn').click(function() {
        alert('Sign In button clicked!');
    });
});
