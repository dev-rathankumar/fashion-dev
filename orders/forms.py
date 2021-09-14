from orders.models import Payment
from django import forms
from accounts.models import User, Customer


class BillingUserInfoForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
    }), label="Email")
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'type': 'number',
        'maxlength': 12,
        'oninput' : 'javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);',
        'class': 'inputNumber',
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']



class BillingCustomerInfoForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
    }), label="Email")
    address_line_1 = forms.CharField(required=True,)
    city = forms.CharField(required=True,)
    pin_code = forms.CharField(required=True,)

    class Meta:
        model = Customer
        fields = ['address_line_1', 'address_line_2', 'city', 'pin_code', 'country', 'state']


class DDPaymentForm(forms.ModelForm):
    dd_attachment = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput(attrs={
        "class": "file",
        "type": "file",
        "data-show-preview": "false"
    }))
    class Meta:
        model = Payment
        fields = ['amount', 'payment_id', 'date_of_dd_payment', 'dd_attachment']
        widgets = {
        'date_of_dd_payment': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'required':'required', 'type':'date'}),
        }