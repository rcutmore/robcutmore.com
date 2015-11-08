from django.contrib import admin

from .models import Project, ProjectTag


# Customize appearance of Project's tags field on admin site.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

admin.site.register(ProjectTag)
