from django.contrib import admin

from projectStickFit.forum.forms import ForumThreadForm
from projectStickFit.forum.models import ForumThreads


@admin.register(ForumThreads)
class ForumThreadAdmin(admin.ModelAdmin):
    model = ForumThreads
    add_form = ForumThreadForm

    list_display = ('pk', 'title', 'short_content', 'created_at', 'updated_at')
    search_fields = ('content',)
    ordering = ('created_at',)

    fieldsets = (
        (None, {'fields': ('title', 'content')}),
    )

    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    short_content.short_description = 'Content'
