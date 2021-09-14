from django import forms
from .models import User, GenderChoice

class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
    }), label="Email")
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput(attrs={
        "class": "file",
        "type": "file",
        # "data-browse-on-zone-click": "true",
        "data-show-preview": "false"
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'type': 'number',
        'maxlength': 12,
        'oninput' : 'javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);',
        'class': 'inputNumber',
    }))
    gender = forms.CharField(widget=forms.Select(choices=GenderChoice,attrs={'required': 'required',}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'gender', 'profile_picture']

    