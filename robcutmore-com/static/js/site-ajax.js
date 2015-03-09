$(document).ready( function() {

    // Filter blog list when tag is clicked.
    $('#post-list').on('click', '.tag', function() {
        var tag = $(this).attr('data-tag');
        var params;

        if (tag.length > 0) {
            params = {'tag': tag};
        } else {
            params = {};
        }

        $.get('/blog/filter/', params, function(data) {
            $('#post-list').html(data);
        });
    });

});