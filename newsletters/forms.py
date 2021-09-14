from django import forms
from .models import NewsletterUser


class EmailSubscribeForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "type": "email",
        "name": "email",
        "id": "email",
        "placeholder": "Enter your email address",
        "class": "input-group__field newsletter-input"
    }), label="")
    class Meta:
        model = NewsletterUser
        fields = ('email',)
