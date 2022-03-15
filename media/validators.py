import magic
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class FileValidator(object):
    error_messages = {
        'content_type': "Files of type %(content_type)s are not allowed. Allowed types are 'png', 'jpeg', 'gif', 'mp4'",
    }

    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.content_types = content_types

    def __call__(self, data):
        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)

            if content_type not in self.content_types:
                params = {'content_type': content_type}
                raise ValidationError(self.error_messages['content_type'],
                                      'content_type', params)

    def __eq__(self, other):
        return (
            isinstance(other, FileValidator) and
            self.content_types == other.content_types
        )
