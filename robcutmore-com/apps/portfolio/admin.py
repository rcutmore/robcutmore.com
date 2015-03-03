from django.contrib import admin
from .models import Project, ProjectTag

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

admin.site.register(ProjectTag)