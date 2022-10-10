$(document).ready(function() {
    $('.form').submit(function(event) {
        event.preventDefault();
        var form = $(this);
        var url = form.attr('action');
        var data = form.serialize();
        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            success: function(data) {
                $('#result').html(data);
            }
        });
    });
});

