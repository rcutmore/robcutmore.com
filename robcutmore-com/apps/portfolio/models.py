from django.db import models


class ProjectTag(models.Model):
    """A portfolio project tag.

    Used to categorize portfolio projects, allowing projects to be
    filtered and grouped by a particular topic.

    :param title: The tag's title. This describes the topic or category
        a particular tag represents.
    """
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Project(models.Model):
    """A portfolio project.

    :param title: Title of project.
    :param description: Description of project.
    :param url: URL of project.
    :param tags: Project's assigned :class:`ProjectTag` objects
        (categories).
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    tags = models.ManyToManyField(ProjectTag, null=True)

    def __str__(self):
        return self.title
