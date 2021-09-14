from django import forms
from accounts.models import User, RegionalManager


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

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'gender', 'profile_picture']

    # Give same CSS class to all the fields
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
          self.fields[myField].widget.attrs['class'] = 'form-control file'


class RegionalManagerForm(forms.ModelForm):
    is_editing = forms.BooleanField(widget=forms.HiddenInput(attrs={
        "type": "hidden",
        'value': 'True',
    }), initial=1)
    is_editing = forms.BooleanField(required=False,initial=True)
    class Meta:
        model = RegionalManager
        fields = ['country', 'state', 'city', 'pin_code', 'address_line_1', 'address_line_2']
        exclude = ('user',)

        # Give same CSS class to all the fields
    def __init__(self, *args, **kwargs):
        super(RegionalManagerForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
          self.fields[myField].widget.attrs['class'] = 'form-control'
