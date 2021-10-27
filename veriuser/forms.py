from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username',
                                                             'class':'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'user@email.com',
                                                             'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'******',
                                                             'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'******',
                                                             'class':'form-control'}))

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'

class UserLoginForm(forms.Form):
    username = forms.ChoiceField(widget=forms.TextInput(attrs={'placeholder':'Username',
                                                               'class':'form-control'}))
    password = forms.ChoiceField(widget=forms.PasswordInput(attrs={'placeholder':'******',
                                                                   'class':'form-control'}))