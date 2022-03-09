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
            self.fields['username'].help_text = '<small class="form-text text-muted">(Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only)</small>'
            self.fields['password1'].help_text = '<small class="form-text text-muted"> <ul> <li>Your password cannot be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password cannot be a commonly used password.</li><li>Your password cannot be entirely numeric.</li><li>Your password must contain atleast one numeric value</li></ul></small>'
            self.fields['password2'].help_text = '<small class="form-text text-muted">(Enter the same password as before, for verification.)</small>'

    def clean(self):
        data = self.cleaned_data

        username = data.get('username')
        qs = User.objects.all().filter(username__iexact=username)
        print(qs)
        if qs.exists():
            self.add_error(
                'username', f'"{username}" is already taken. Please pick another')

        return data
