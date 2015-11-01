from django import forms

from django.contrib.auth.models import User

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput(),
        }

class EditEmailForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )


class EditPasswordForm(forms.Form):

    password = forms.CharField(
        label='New Password',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))