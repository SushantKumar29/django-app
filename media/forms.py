from django import forms
from .models import Media


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['name', 'media_file', 'description']
        labels = {
            'name': 'Enter name',
            'media_file': 'Choose image/video',
            'description': 'Enter description'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            field_attrs = {
                'placeholder': f'Media {str(field)}',
                'class': 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(field_attrs)
        self.fields['description'].widget.attrs.update({'rows': 3})
