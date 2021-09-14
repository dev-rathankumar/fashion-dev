from django import forms
from ckeditor.widgets import CKEditorWidget
from django.forms import inlineformset_factory
from .models import Email, BusinessEmailSetting
from accounts.models import User


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['subject', 'email_body', 'is_sent']

    # Give same CSS class to all the fields
    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        # self.fields['to_address'].queryset = User.objects.filter(is_customer=True, is_active=True)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class BusinessEmailSettingForm(forms.ModelForm):
    
    email_host_password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'off', 'readonly': 'readonly', 'onfocus': "this.removeAttribute('readonly');"}))
    class Meta:
        model = BusinessEmailSetting
        fields = ['email_host', 'email_host_user', 'email_host_password', 'port', 'email_use_tls']

    # Give same CSS class to all the fields
    def __init__(self, *args, **kwargs):
        super(BusinessEmailSettingForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['required'] = 'required'
