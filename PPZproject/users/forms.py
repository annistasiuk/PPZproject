from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Playlist

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'category']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Username:',
            'first_name': 'First name:',
            'last_name': 'Last name:',
            'email': 'Email:',
            'password1': 'Password:',
        }
        widgets = {
            'username': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.EmailInput(),
            'password1': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_customer = True  # якщо це твоє кастомне поле
        if commit:
            user.save()
        return user
