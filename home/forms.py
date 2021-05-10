from django import  forms

from account.models import Account


class send_email_form(forms.Form):
    name=forms.CharField(max_length=30 , required=True , widget=forms.TextInput(attrs={}))
    email=forms.EmailField(max_length=60 , required=True , widget=forms.EmailInput(attrs={}))
    subject=forms.CharField(max_length=20 , required=True)
    text=forms.CharField(max_length=100 , required=True , widget=forms.Textarea(attrs={'rows':'5', 'cols':'5'}))

    def clean(self):
        data=super(send_email_form , self).clean()
        email=self.cleaned_data['email']
        if Account.objects.filter(email=email).exists():
            return data
        else:
            raise forms.ValidationError('email address is not exists')