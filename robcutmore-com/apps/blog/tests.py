from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Post, PostTag
from .templatetags.blog_tags import get_post_list

def add_post_tag(title):
    tag = PostTag.objects.get_or_create(title=title)[0]
    return tag

def add_post(title, text, tags=None):
    user = add_user('Test')
    post = Post.objects.get_or_create(author=user, title=title, text=text)[0]

    tags = tags if tags else []
    post_tags = [add_post_tag(tag) for tag in tags]
    post.tags.add(*post_tags)

    return post

def add_user(username):
    user = User.objects.get_or_create(username=username)[0]
    return user

class BlogTagsTests(TestCase):
    def test_get_post_list_with_no_posts(self):
        """get_post_list should return no posts when none exist."""
        result = get_post_list()

        self.assertQuerysetEqual(result['posts'].object_list, [])
        self.assertIsNone(result['tag'])
        self.assertFalse(result['filtered'])

    def test_get_post_list_with_published_posts(self):
        """get_post_list should return all published posts."""
        first_post = add_post(title='Title 1', text='Text 1')
        first_post.publish()
        second_post = add_post(title='Title 2', text='Text 2')
        second_post.publish()

        result = get_post_list()

        posts = [first_post, second_post]
        result_posts = result['posts'].object_list

        for post in posts:
            self.assertTrue(post in result_posts)
        self.assertEqual(len(result_posts), len(posts))

        self.assertIsNone(result['tag'])
        self.assertFalse(result['filtered'])

    def test_get_post_list_with_published_and_unpublished_posts(self):
        """get_post_list should return only published posts."""
        published_post = add_post(title='Title 1', text='Text 1')
        published_post.publish()
        unpublished_post = add_post(title='Title 2', text='Text 2')

        result = get_post_list()
        result_posts = result['posts'].object_list

        self.assertTrue(published_post in result_posts)
        self.assertFalse(unpublished_post in result_posts)
        self.assertEqual(len(result_posts), 1)

        self.assertIsNone(result['tag'])
        self.assertFalse(result['filtered'])

    def test_get_post_list_with_tag_filter(self):
        """get_post_list should return only published posts for given tag."""
        tag = 'tag1'
        first_post = add_post(title='Title 1', text='Text 1', tags=[tag])
        first_post.publish()
        second_post = add_post(title='Title 2', text='Text 2', tags=[tag])
        second_post.publish()
        post_without_tag = add_post(title='Title 3', text='Text 3')
        post_without_tag.publish()

        result = get_post_list(tag=tag)

        posts_with_tag = [first_post, second_post]
        result_posts = result['posts'].object_list

        for post_with_tag in posts_with_tag:
            self.assertTrue(post_with_tag in result_posts)
        self.assertFalse(post_without_tag in result_posts)
        self.assertEqual(len(result_posts), len(posts_with_tag))

        self.assertEqual(result['tag'], tag)
        self.assertTrue(result['filtered'])

    def test_get_post_list_with_page_filter(self):
        """get_post_list should return only published posts for given page."""
        posts = []
        for i in range(10):
            post = add_post(title='Title {0}'.format(i), text='Text {0}'.format(i))
            post.publish()
            posts.append(post)

        first_page_posts = posts[5:]
        second_page_posts = posts[:5]

        # Test first page.
        result = get_post_list(page=1)
        first_page_result_posts = result['posts'].object_list

        for first_page_post in first_page_posts:
            self.assertTrue(first_page_post in first_page_result_posts)
        for second_page_post in second_page_posts:
            self.assertFalse(second_page_post in first_page_result_posts)

        # Test second page.
        result = get_post_list(page=2)
        second_page_result_posts = result['posts'].object_list

        for first_page_post in first_page_posts:
            self.assertFalse(first_page_post in second_page_result_posts)
        for second_page_post in second_page_posts:
            self.assertTrue(second_page_post in second_page_result_posts)

class PostTests(TestCase):
    def test_publish_sets_published_date(self):
        """publish should set published_date to the current date and time."""
        post = add_post(title='Title 1', text='Text 1')
        time_before_publish = timezone.now()

        post.publish()
        post = Post.objects.get(id=post.id)

        self.assertIsNotNone(post.published_date)
        self.assertTrue(time_before_publish <= post.published_date)

    def test_creation_date_before_published_date(self):
        """publish should set published_date_later_than_created_date."""
        post = add_post(title='Title 1', text='Text 1')
        post.publish()
        post = Post.objects.get(id=post.id)

        self.assertTrue(post.created_date <= post.published_date)

    def test_published_date_not_set_before_publish(self):
        """published_date should not be set before post is published."""
        post = add_post(title='Title 1', text='Text 1')

        self.assertIsNone(post.published_date)

class PostListTests(TestCase):
    def test_post_list_with_no_posts(self):
        """post_list should display message when no posts exist."""
        response = self.client.get(reverse('blog:post_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no blog posts.')

    def test_post_list_with_published_posts(self):
        """post_list should display all published posts."""
        first_post = add_post(title='Title 1', text='Text 1')
        first_post.publish()
        second_post = add_post(title='Title 2', text='Text 2')
        second_post.publish()

        response = self.client.get(reverse('blog:post_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, first_post.title)
        self.assertContains(response, first_post.text)
        self.assertContains(response, second_post.title)
        self.assertContains(response, second_post.text)

    def test_post_list_with_unpublished_posts(self):
        """post_list should only display published posts, not any unpublished posts."""
        first_post = add_post(title='Title 1', text='Text 1')
        first_post.publish()
        second_post = add_post(title='Title 2', text='Text 2')

        response = self.client.get(reverse('blog:post_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, first_post.title)
        self.assertContains(response, first_post.text)
        self.assertNotContains(response, second_post.title)
        self.assertNotContains(response, second_post.text)

    def test_post_list_tags(self):
        """post_list should display post tags."""
        tags = ['tag1', 'tag2', 'tag3']
        post = add_post(title='Title 1', text='Text 1', tags=tags)
        post.publish()

        response = self.client.get(reverse('blog:post_list'))
        
        self.assertEqual(response.status_code, 200)

        for tag in tags:
            self.assertContains(response, tag)

    def test_post_list_pagination(self):
        """post_list should display pagination buttons with more than 5 posts."""
        for i in range(15):
            post = add_post(title='Title {0}'.format(i), text='Text {0}'.format(i))
            post.publish()

        url = reverse('blog:post_list')

        # Test first page.
        response = self.client.get(url)
        self.assertNotContains(response, 'Previous')
        self.assertContains(response, 'Next')

        # Test second page.
        response = self.client.get('{url}?page=2'.format(url=url))
        self.assertContains(response, 'Previous')
        self.assertContains(response, 'Next')

        # Test third page.
        response = self.client.get('{url}?page=3'.format(url=url))
        self.assertContains(response, 'Previous')
        self.assertNotContains(response, 'Next')


class PostDetailTests(TestCase):
    def test_post_detail_for_nonexistent_post(self):
        """post_detail should show 404 page for non-existent post."""
        url_args = {
            'post_month': 1,
            'post_day': 1,
            'post_year': 2015,
            'post_slug': 'test-slug',
        }
        response = self.client.get(reverse('blog:post_detail', kwargs=url_args))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_for_published_post(self):
        """post_detail should display published post content."""
        tags = ['tag1', 'tag2', 'tag3']
        post = add_post(title='Title 1', text='Text 1', tags=tags)
        post.publish()

        url_args = {
            'post_month': post.published_date.month,
            'post_day': post.published_date.day,
            'post_year': post.published_date.year,
            'post_slug': post.slug,
        }
        response = self.client.get(reverse('blog:post_detail', kwargs=url_args))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        self.assertContains(response, post.text)

        for tag in tags:
            self.assertContains(response, tag)