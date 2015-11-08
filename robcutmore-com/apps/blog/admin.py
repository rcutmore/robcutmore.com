from django.contrib import admin

from .models import Post, PostTag


# Customize appearance of Post's tags field on admin site.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

admin.site.register(PostTag)
