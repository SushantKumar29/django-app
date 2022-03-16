from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            field_attrs = {
                # 'placeholder': f'{str(field)}',
                'class': 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(field_attrs)
            # self.fields[field].help_text = None
            self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only'
            self.fields['password1'].help_text = 'Your password cannot be too similar to your other personal information.\n\nYour password must contain at least 8 characters.\n\nYour password cannot be a commonly used password.\n\nYour password cannot be entirely numeric.\n\nYour password must contain atleast one numeric value.'
            self.fields['password2'].help_text = 'Enter the same password as before, for verification.'

    def clean(self):
        data = self.cleaned_data

        username = data.get('username')
        # email = data.get('email')
        qs = User.objects.all().filter(username__iexact=username)
        if qs.exists():
            self.add_error(
                'username', f'"{username}" is already taken. Please pick another')

        return data
