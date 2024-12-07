from django.contrib import admin

from django.contrib import admin

from projectStickFit.posts.forms import PostForm
from projectStickFit.posts.models import Posts


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    model = Posts
    add_form = PostForm

    list_display = ('pk', 'title', 'image', 'short_caption', 'created_at', 'updated_at')
    search_fields = ('content',)
    ordering = ('created_at',)

    fieldsets = (
        (None, {'fields': ('title', 'image', 'caption')}),
    )

    def short_caption(self, obj):
        return obj.caption[:50] + '...' if len(obj.caption) > 50 else obj.caption

    short_caption.short_description = 'Caption'

