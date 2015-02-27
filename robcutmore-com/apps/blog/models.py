from autoslug.fields import AutoSlugField

from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
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