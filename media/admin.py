from django.contrib import admin
from .models import Media


class MediaAdmin(admin.ModelAdmin):
    model = Media
    list_display = ['id', 'media_file', 'created_at', 'updated_at']
    search_fields = ['description']


admin.site.register(Media, MediaAdmin)
