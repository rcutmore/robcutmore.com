from django.contrib.auth.models import User
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
        post = add_post("Test Author", "Test title", "Test text")
        time_before_publish = timezone.now()

        post.publish()
        post = Post.objects.get(id=post.id)

        self.assertIsNotNone(post.published_date)
        self.assertTrue(time_before_publish <= post.published_date)

    def test_creation_date_before_published_date(self):
        """publish should set published_date_later_than_created_date."""
        post = add_post("Test Author", "Test title", "Test text")
        post.publish()
        post = Post.objects.get(id=post.id)

        self.assertTrue(post.created_date <= post.published_date)

    def test_published_date_not_set_before_publish(self):
        """published_date should not be set before post is published."""
        post = add_post("Test Author", "Test title", "Test text")

        self.assertIsNone(post.published_date)