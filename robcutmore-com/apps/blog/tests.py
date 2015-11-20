"""
Contains tests for blog app.
"""
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Post, PostTag
from .templatetags.blog_tags import get_post_list


def add_post_tag(title):
    """Add new post tag with the given title.

    :param title: Title of tag.
    :returns: :class:`PostTag` object.
    """
    return PostTag.objects.get_or_create(title=title)[0]


def add_post(title, text, tags=None):
    """Add new post with the given attributes.

    :param title: Title of post.
    :param text: Content of post.
    :param tags: Tags to assign post.
    :returns: :class:`Post` object.
    """
    # Create post.
    user = add_user('Test')
    post = Post.objects.get_or_create(author=user, title=title, text=text)[0]

    # Add tags to post.
    tags = tags if tags else []
    post_tags = [add_post_tag(tag) for tag in tags]
    post.tags.add(*post_tags)
    return post


def add_user(username):
    """Add new user with the given username.

    :param username: Username for new user.
    :returns: :class:`User` object.
    """
    return User.objects.get_or_create(username=username)[0]


class BlogTemplateTagsTests(TestCase):
    """Tests custom template tags for blog app."""

    def test_get_post_list_with_no_posts(self):
        """get_post_list should return no posts when none exist."""
        result = get_post_list()
        self.assertQuerysetEqual(result['posts'].object_list, [])
        self.assertIsNone(result['tag'])
        self.assertFalse(result['filtered'])

    def test_get_post_list_with_published_posts(self):
        """get_post_list should return all published posts."""
        # Add two published posts.
        first_post = add_post(title='Title 1', text='Text 1')
        first_post.publish()
        second_post = add_post(title='Title 2', text='Text 2')
        second_post.publish()
        posts = [first_post, second_post]

        result = get_post_list()
        result_posts = result['posts'].object_list

        # Make sure two test posts are retrieved.
        for post in posts:
            self.assertTrue(post in result_posts)
        self.assertEqual(len(result_posts), len(posts))
        self.assertIsNone(result['tag'])
        self.assertFalse(result['filtered'])

    def test_get_post_list_with_published_and_unpublished_posts(self):
        """get_post_list should return only published posts."""
        # Add published and unpublished posts.
        published_post = add_post(title='Title 1', text='Text 1')
        published_post.publish()
        unpublished_post = add_post(title='Title 2', text='Text 2')

        result = get_post_list()
        result_posts = result['posts'].object_list

        # Make sure only published post is retrieved.
        self.assertTrue(published_post in result_posts)
        self.assertFalse(unpublished_post in result_posts)
        self.assertEqual(len(result_posts), 1)
        self.assertIsNone(result['tag'])
        self.assertFalse(result['filtered'])

    def test_get_post_list_with_tag_filter(self):
        """get_post_list should return only published posts with given tag."""
        # Add test posts.
        tag = 'tag1'
        first_post = add_post(title='Title 1', text='Text 1', tags=[tag])
        first_post.publish()
        second_post = add_post(title='Title 2', text='Text 2', tags=[tag])
        second_post.publish()
        posts_with_tag = [first_post, second_post]
        post_without_tag = add_post(title='Title 3', text='Text 3')
        post_without_tag.publish()

        result = get_post_list(tag=tag)
        result_posts = result['posts'].object_list

        # Make sure only posts with tag are retrieved.
        for post_with_tag in posts_with_tag:
            self.assertTrue(post_with_tag in result_posts)
        self.assertFalse(post_without_tag in result_posts)
        self.assertEqual(len(result_posts), len(posts_with_tag))
        self.assertEqual(result['tag'], tag)
        self.assertTrue(result['filtered'])

    def test_get_post_list_with_page_filter(self):
        """get_post_list should return only published posts for given page."""
        # Publish test posts.
        posts = []
        for i in range(10):
            post = add_post(
                title='Title {}'.format(i),
                text='Text {}'.format(i))
            post.publish()
            posts.append(post)

        first_page_posts = posts[5:]
        second_page_posts = posts[:5]

        # Check first page results.
        result = get_post_list(page=1)
        first_page_result_posts = result['posts'].object_list
        for first_page_post in first_page_posts:
            self.assertTrue(first_page_post in first_page_result_posts)
        self.assertFalse(
            any(post in first_page_result_posts for post in second_page_posts))

        # Check second page results.
        result = get_post_list(page=2)
        second_page_result_posts = result['posts'].object_list
        for second_page_post in second_page_posts:
            self.assertTrue(second_page_post in second_page_result_posts)
        self.assertFalse(
            any(post in second_page_result_posts for post in first_page_posts))


class PostTests(TestCase):
    """Tests :class:`Post` object model."""

    def test_publish_sets_published_date(self):
        """publish should set published_date to current date/time."""
        # Publish test post and save date/time.
        test_post = add_post(title='Title 1', text='Text 1')
        time_before_publish = timezone.now()
        test_post.publish()

        # Fetch post and compare published_date/time.
        post = Post.objects.get(id=test_post.id)
        self.assertIsNotNone(post.published_date)
        self.assertTrue(time_before_publish <= post.published_date)

    def test_creation_date_before_published_date(self):
        """publish should set published_date later than created_date."""
        # Publish test post.
        test_post = add_post(title='Title 1', text='Text 1')
        test_post.publish()

        # Fetch post to compare created and published date/time.
        post = Post.objects.get(id=test_post.id)
        self.assertTrue(post.created_date <= post.published_date)

    def test_published_date_not_set_before_publish(self):
        """published_date should not be set before post is published."""
        post = add_post(title='Title 1', text='Text 1')
        self.assertIsNone(post.published_date)


class PostListTests(TestCase):
    """Tests post list page of blog app."""

    def test_post_list_with_no_posts(self):
        """post_list should display message when no posts exist."""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no blog posts.')

    def test_post_list_with_published_posts(self):
        """post_list should display all published posts."""
        # Publish test posts.
        first_post = add_post(title='Title 1', text='Text 1')
        first_post.publish()
        second_post = add_post(title='Title 2', text='Text 2')
        second_post.publish()

        # Check that post list contains test posts.
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, first_post.title)
        self.assertContains(response, first_post.text)
        self.assertContains(response, second_post.title)
        self.assertContains(response, second_post.text)

    def test_post_list_with_unpublished_posts(self):
        """post_list should only display published posts."""
        # Create test posts: one published and one unpublished.
        published_post = add_post(title='Title 1', text='Text 1')
        published_post.publish()
        unpublished_post = add_post(title='Title 2', text='Text 2')

        # Check that post list contains only published post.
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, published_post.title)
        self.assertContains(response, published_post.text)
        self.assertNotContains(response, unpublished_post.title)
        self.assertNotContains(response, unpublished_post.text)

    def test_post_list_tags(self):
        """post_list should display post tags."""
        # Publish test post with tags.
        tags = ['tag1', 'tag2', 'tag3']
        post = add_post(title='Title 1', text='Text 1', tags=tags)
        post.publish()

        # Check that post list contains each tag.
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        for tag in tags:
            self.assertContains(response, tag)

    def test_post_list_pagination(self):
        """post_list should show pagination buttons with many posts."""
        # Publish enough test posts so that pagination is required.
        # post_list should show 5 posts per page, so 15 posts will
        # be split up over 3 pages.
        for i in range(15):
            post = add_post(
                title='Title {0}'.format(i),
                text='Text {0}'.format(i))
            post.publish()

        url = reverse('blog:post_list')

        # Check buttons on first page.
        response = self.client.get(url)
        self.assertNotContains(response, 'Previous')
        self.assertContains(response, 'Next')

        # Check buttons on second page.
        response = self.client.get('{url}?page=2'.format(url=url))
        self.assertContains(response, 'Previous')
        self.assertContains(response, 'Next')

        # Check buttons on third page.
        response = self.client.get('{url}?page=3'.format(url=url))
        self.assertContains(response, 'Previous')
        self.assertNotContains(response, 'Next')


class PostDetailTests(TestCase):
    """Tests post detail page of blog app."""

    def test_post_detail_for_nonexistent_post(self):
        """post_detail should show 404 page for non-existent post."""
        args = {
            'post_month': 1,
            'post_day': 1,
            'post_year': 2015,
            'post_slug': 'non-existent-post',
        }
        response = self.client.get(reverse('blog:post_detail', kwargs=args))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_for_published_post(self):
        """post_detail should display published post content."""
        # Publish test post.
        tags = ['tag1', 'tag2', 'tag3']
        post = add_post(title='Title 1', text='Text 1', tags=tags)
        post.publish()

        args = {
            'post_month': post.published_date.month,
            'post_day': post.published_date.day,
            'post_year': post.published_date.year,
            'post_slug': post.slug,
        }
        response = self.client.get(reverse('blog:post_detail', kwargs=args))

        # Check that post detail contains all test post attributes.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        self.assertContains(response, post.text)
        for tag in tags:
            self.assertContains(response, tag)
