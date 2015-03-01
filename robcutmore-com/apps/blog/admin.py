from django.contrib import admin
from .models import Post, PostTag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

admin.site.register(PostTag)