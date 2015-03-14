$(document).ready( function() {

    // Filter blog list when tag is clicked.
    $('#post-list').on('click', '.tag', function() {
        var tag = $(this).attr('data-tag');

        var params;
        var urlTag;
        if (tag.length > 0) {
            params = {'tag': tag};
            urlTag = tag + '/';
        } else {
            params = {};
            urlTag = '';
        }

        $.get('/blog/filter/', params, function(data) {
            history.pushState({}, '', 'http://robcutmore.com/blog/' + urlTag);
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
            history.pushState({}, '', '?page=' + page);
            $('#post-list').html(data);
        });
    });

    // Filter portfolio list when tag is clicked.
    $('#project-list').on('click', '.tag', function() {
        var tag = $(this).attr('data-tag');

        var params;
        var urlTag;
        if (tag.length > 0) {
            params = {'tag': tag};
            urlTag = tag + '/'
        } else {
            params = {};
            urlTag = '';
        }
        
        $.get('/portfolio/filter/', params, function(data) {
            history.pushState({}, '', 'http://robcutmore.com/portfolio/' + urlTag);
            $('#project-list').html(data);
        });
    });

    // Filter project list when pagination button is clicked.
    $('#project-list').on('click', '.pagination-button', function(data) {
        var page = $(this).attr('data-page');
        var tag = $(this).attr('data-tag');

        var params = {};
        if (page.length > 0) {
            params['page'] = page;
        }
        if (tag.length > 0) {
            params['tag'] = tag;
        }

        $.get('/portfolio/filter/', params, function(data) {
            history.pushState({}, '', '?page=' + page);
            $('#project-list').html(data);
        });
    });

});