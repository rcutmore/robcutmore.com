from django.contrib import admin
from .models import Post, PostTag

class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

admin.site.register(Post, PostAdmin)
admin.site.register(PostTag)