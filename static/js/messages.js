$(document).ready(function() {
    var hasMessages = $('body').data('has-messages');
    if (hasMessages) {
        $('#messageModal').modal('show');
    }
});
