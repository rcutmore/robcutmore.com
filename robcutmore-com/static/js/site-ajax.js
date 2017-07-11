$(document).ready( function() {

    /**
     * Scrolls to top of page.
     */
    var scrollToTop = function() {
        $('html, body').animate({ scrollTop: 0 }, 'slow');
    }

    /**
     * Determines filter parameters for given tag.
     * @param {string} tag Tag to filter for.
     * @return {object} GET request parameters and filtered URL page.
     */
    var tagFilter = function(tag) {
        // If there is a tag then set required information for filter
        // otherwise set blank data which will result in no filter.
        let filter;
        if (tag.length > 0) {
            filter = {
                params: {tag: tag},
                url: tag + '/'
            };
        } else {
            filter = {
                params: {},
                url: ''
            };
        }
        return filter;
    };

    /**
     * Determines filter parameters for given page and tag.
     * @param {string} page Page number to show.
     * @param {string} tag Tag to filter for.
     * @return {object} GET request parameters.
     */
    var pageFilter = function(page, tag) {
        // Only set parameters if they aren't blank.
        let filter = {};
        if (page.length > 0) {
            filter['page'] = page;
        }
        if (tag.length > 0) {
            filter['tag'] = tag;
        }
        return filter;
    };

    /**
     * Filters blog list when user clicks tag.
     */
    $('#post-list').on('click', '.tag', function() {
        // Get filter parameters.
        let tag = $(this).attr('data-tag');
        let filter = tagFilter(tag);

        // Filter posts and update URL for browser.
        $.get('/blog/filter/', filter.params, function(data) {
            let protocol = window.location.protocol;
            let url = protocol + '//www.robcutmore.com/blog/' + filter.url;
            history.pushState({}, '', url);
            $('#post-list').html(data);
        });
        scrollToTop();
    });

    /**
     * Filters blog list when pagination buttons are clicked.
     */
    $('#post-list').on('click', '.pagination-button', function() {
        // Get filter parameters.
        let page = $(this).attr('data-page');
        let tag = $(this).attr('data-tag');
        let filter = pageFilter(page, tag);

        // Filter posts and update URL for browser.
        $.get('/blog/filter/', filter, function(data) {
            history.pushState({}, '', '?page=' + filter.page);
            $('#post-list').html(data);
        });
        scrollToTop();
    });

    /**
     * Filters portfolio list when user clicks tag.
     */
    $('#project-list').on('click', '.tag', function() {
        // Get filter parameters.
        let tag = $(this).attr('data-tag');
        let filter = tagFilter(tag);

        // Filter projects and update URL for browser.
        $.get('/portfolio/filter/', filter.params, function(data) {
            let protocol = window.location.protocol;
            let url = protocol + '//www.robcutmore.com/portfolio/' + filter.url;
            history.pushState({}, '', url);
            $('#project-list').html(data);
        });
        scrollToTop();
    });

    /**
     * Filters portfolio list when pagination buttons are clicked.
     */
    $('#project-list').on('click', '.pagination-button', function(data) {
        // Get filter parameters.
        let page = $(this).attr('data-page');
        let tag = $(this).attr('data-tag');
        let filter = pageFilter(page, tag);

        // Filter projects and update URL for browser.
        $.get('/portfolio/filter/', filter, function(data) {
            history.pushState({}, '', '?page=' + filter.page);
            $('#project-list').html(data);
        });
        scrollToTop();
    });

});
