from autoslug.fields import AutoSlugField

from django.db import models
from django.utils import timezone


class PostTag(models.Model):
    """A blog post tag.

    Used to categorize blog posts, allowing posts to be filtered and
    grouped by a particular topic.

    :param title: The tag's title. This describes the topic or category
        a particular tag represents.
    """
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Post(models.Model):
    """A blog post.

    :param author: Author of post.
    :param title: Title of post.
    :param text: Content of post.
    :param tags: Post's assigned :class:`PostTag` objects (categories).
    :param created_date: Date that post was created.
    :param published_date: Date that post was published.
    :param slug: Slug of post title, used for post's URL.
    """
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    tags = models.ManyToManyField(PostTag, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique_with='published_date')

    def publish(self):
        """Set published_date so post can be displayed on blog."""
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-published_date',)
