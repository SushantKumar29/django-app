import pathlib
import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models import Q


User = settings.AUTH_USER_MODEL


class MediaQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == '':
            return self.none()
        lookups = Q(description__icontains=query)
        return self.filter(lookups)


class MediaManager(models.Manager):
    def get_queryset(self):
        return MediaQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


def file_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_filename = str(uuid.uuid1())
    return f"media/{new_filename}{fpath.suffix}"


class Media(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="")
    media_file = models.FileField(upload_to='media/')
    description = models.TextField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MediaManager()

    def get_absolute_url(self):
        return reverse("media:list")

    def get_media_url(self):
        return self.media_file.path
