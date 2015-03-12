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

    // Filter blog list when pagination button is clicked.
    $('#post-list').on('click', '.pagination-button', function() {
        var page = $(this).attr('data-page');
        var tag = $(this).attr('data-tag');

        var params = {};
        if (page.length > 0) {
            params['page'] = page;
        }
        if (tag.length > 0) {
            params['tag'] = tag;
        }

        $.get('/blog/filter/', params, function(data) {
            $('#post-list').html(data);
        });
    });

    // Filter portfolio list when tag is clicked.
    $('#project-list').on('click', '.tag', function() {
        var tag = $(this).attr('data-tag');
        var params;

        if (tag.length > 0) {
            params = {'tag': tag};
        } else {
            params = {};
        }
        
        $.get('/portfolio/filter/', params, function(data) {
            $('#project-list').html(data);
        });
    });

});