$(document).ready( function() {
    var tagFilter = function() {
        var tag = $(this).attr('data-tag');

        var filter;
        if (tag.length > 0) {
            filter = {
                params: {'tag': tag},
                url = tag + '/',
            };
        } else {
            filter = {
                params: {},
                url = '',
            };
        }

        return filter;
    };

    var pageFilter = function() {
        var page = $(this).attr('data-page');
        var tag = $(this).attr('data-tag');

        var filter = {};
        if (page.length > 0) {
            filter['page'] = page;
        }
        if (tag.length > 0) {
            filter['tag'] = tag;
        }

        return filter;
    };

    // Filter blog list when tag is clicked.
    $('#post-list').on('click', '.tag', function() {
        var filter = tagFilter();

        $.get('/blog/filter/', filter.params, function(data) {
            history.pushState({}, '', 'http://robcutmore.com/blog/' + filter.url);
            $('#post-list').html(data);
        });
    });

    // Filter blog list when pagination button is clicked.
    $('#post-list').on('click', '.pagination-button', function() {
        var filter = pageFilter();

        $.get('/blog/filter/', filter, function(data) {
            history.pushState({}, '', '?page=' + filter.page);
            $('#post-list').html(data);
        });
    });

    // Filter portfolio list when tag is clicked.
    $('#project-list').on('click', '.tag', function() {
        var filter = tagFilter();
        
        $.get('/portfolio/filter/', filter.params, function(data) {
            history.pushState({}, '', 'http://robcutmore.com/portfolio/' + filter.url);
            $('#project-list').html(data);
        });
    });

    // Filter project list when pagination button is clicked.
    $('#project-list').on('click', '.pagination-button', function(data) {
        var filter = pageFilter();

        $.get('/portfolio/filter/', filter, function(data) {
            history.pushState({}, '', '?page=' + filter.page);
            $('#project-list').html(data);
        });
    });

});