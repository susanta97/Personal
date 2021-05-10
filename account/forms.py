from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Add a valid email address.' , widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder':'Email *' ,}))

    first_name=forms.CharField(max_length=30 , required=True , widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder':'First Name *'}))
    last_name=forms.CharField(max_length=30 , required=True , widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder':'Last Name *'}))
    contact=forms.CharField(max_length=10 ,help_text='Add a valid contact number', widget=forms.NumberInput(attrs={'class':'form-control' , 'placeholder':'Contact *'}))
    username=forms.CharField(max_length=10 , widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder':'Username *'}))

    password1 = forms.CharField(max_length=30 , required=True ,  widget=forms.PasswordInput(attrs={'class':'form-control' , 'placeholder':'Password *'}))

    password2 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))


    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2','first_name' , 'last_name' , 'contact')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].label = False


    def clean_first_name(self):
        data=self.cleaned_data['first_name']
        if data == 'shreya':
            raise forms.ValidationError('shreya is not allow')
        return data

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)

    # def clean(self):
    #     data = super(RegistrationForm, self).clean()
    #     print(data['first_name'])
    #     return data

    def save(self, commit=True):
        account = super(RegistrationForm, self).save(commit=False)
        first_name = self.data.get('first_name')
        last_name = self.data.get('last_name')
        contact = self.data.get('contact')

        account.first_name = first_name
        account.last_name = last_name
        account.contact = contact

        if commit:
            account.save()
        return account




class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder':'password'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email address'}))


    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, required=False
                             )
    class Meta:
        model = Account
        fields = ('username', 'email', 'profile_image', 'hide_email')

    # def clean_email(self):
    #     email = self.cleaned_data['email'].lower()
    #     try:
    #         account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
    #     except Account.DoesNotExist:
    #         return email
    #     raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)

    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email=self.initial['email']
        # account.email = self.cleaned_data['email'].lower()
        account.profile_image = self.cleaned_data['profile_image']

        account.hide_email = self.cleaned_data['hide_email']
        if commit:
            account.save()
        return account
