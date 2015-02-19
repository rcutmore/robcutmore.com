from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Post

def add_post(author, title, text):
    user = add_user(author)
    post = Post.objects.get_or_create(author=user, title=title, text=text)[0]
    return post

def add_user(username):
    user = User.objects.get_or_create(username=username)[0]
    return user

class PostTests(TestCase):
    def test_publish_sets_published_date(self):
        """publish should set published_date to the current date and time."""
        post = add_post('Test Author', 'Test title', 'Test text')
        time_before_publish = timezone.now()

        post.publish()
        post = Post.objects.get(id=post.id)

        self.assertIsNotNone(post.published_date)
        self.assertTrue(time_before_publish <= post.published_date)

    def test_creation_date_before_published_date(self):
        """publish should set published_date_later_than_created_date."""
        post = add_post('Test Author', 'Test title', 'Test text')
        post.publish()
        post = Post.objects.get(id=post.id)

        self.assertTrue(post.created_date <= post.published_date)

    def test_published_date_not_set_before_publish(self):
        """published_date should not be set before post is published."""
        post = add_post('Test Author', 'Test title', 'Test text')

        self.assertIsNone(post.published_date)

class PostListTests(TestCase):
    def test_post_list_with_no_posts(self):
        """post_list should display message when no posts exist."""
        response = self.client.get(reverse('blog:post_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no blog posts.')
        self.assertQuerysetEqual(response.context['posts'], [])

    def test_post_list_with_published_posts(self):
        """post_list should display all published posts."""
        first_post = add_post('Test Author', 'Test title 1', 'Test text 1')
        first_post.publish()
        second_post = add_post('Test Author', 'Test title 2', 'Test text 2')
        second_post.publish()

        response = self.client.get(reverse('blog:post_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, first_post.title)
        self.assertContains(response, first_post.text)
        self.assertContains(response, second_post.title)
        self.assertContains(response, second_post.text)

        post_count = len(response.context['posts'])
        self.assertEqual(post_count, 2)

    def test_post_list_with_unpublished_posts(self):
        """post_list should only display published posts, not any unpublished posts."""
        first_post = add_post('Test Author', 'Test title 1', 'Test text 1')
        first_post.publish()
        second_post = add_post('Test Author', 'Test title 2', 'Test text 2')

        response = self.client.get(reverse('blog:post_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, first_post.title)
        self.assertContains(response, first_post.text)
        self.assertNotContains(response, second_post.title)
        self.assertNotContains(response, second_post.text)

        post_count = len(response.context['posts'])
        self.assertEqual(post_count, 1)