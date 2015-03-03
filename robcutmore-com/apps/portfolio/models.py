from django.db import models

class ProjectTag(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    tags = models.ManyToManyField(ProjectTag, null=True)

    def __str__(self):
        return self.title