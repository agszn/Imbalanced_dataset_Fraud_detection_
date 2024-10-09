from django import forms
from django.contrib.auth.models import User
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        strip=False,
        required=True,
        help_text='',
        error_messages={
            'unique': "A user with that username already exists.",
        },
        widget=forms.TextInput(attrs={
            'class': 'rounded-md py-2 px-3 tm-bg-brown ',  # Added styling classes
            'placeholder': 'Enter Username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-md py-2 px-3 tm-bg-brown ',
            'placeholder': 'Enter Password',
        })
    )


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-md py-2 px-3 tm-bg-brown ',
            'placeholder': 'Enter Password',
        }),
        strip=False,
        required=True,
        error_messages={
            'password_mismatch': "The two password fields didn't match.",
        },
    )
    password2 = forms.CharField(
        label='Repeat Password', 
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-md py-2 px-3 tm-bg-brown ',
            'placeholder': 'Repeat Password',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'rounded-md py-2 px-3 tm-bg-brown ',
                'placeholder': 'Enter Username',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'rounded-md py-2 px-3 tm-bg-brown ',
                'placeholder': 'Enter First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'rounded-md py-2 px-3 tm-bg-brown ',
                'placeholder': 'Enter Last Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'rounded-md py-2 px-3 tm-bg-brown ',
                'placeholder': 'Enter Email',
            }),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password does not match')
        return cd['password2']



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-md py-2 px-3 tm-bg-brown ',
            'placeholder': 'Enter Password',
        }),
        strip=False,
        required=True,
        error_messages={
            'password_mismatch': "The two password fields didn't match.",
        },
    )
    password2 = forms.CharField(
        label='Repeat Password', 
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-md py-2 px-3 tm-bg-brown ',
            'placeholder': 'Repeat Password',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'rounded-md py-2 px-3 tm-bg-brown ',
                'placeholder': 'Enter Username',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'rounded-md py-2 px-3 tm-bg-brown ',
                'placeholder': 'Enter First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'rounded-md py-2 px-3 tm-bg-brown ',
                'placeholder': 'Enter Last Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'rounded-md py-2 px-3 tm-bg-brown ',
                'placeholder': 'Enter Email',
            }),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password does not match')
        return cd['password2']
    
    
class EditProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']


from django import forms
class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control image-upload',  # Add Bootstrap class + custom class
            'accept': 'image/*',                   # Accept only image files
            'placeholder': 'Upload Retinal Image',  # Placeholder text
        })
    )

from django import forms
from .models import Transaction
from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['card_holder_name', 'card_number', 'transaction_amount', 'merchant_name', 'merchant_type', 'location']
        
        # Adding widgets with CSS classes
        widgets = {
            'card_holder_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter card holder name'
            }),
            'card_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter card number',
                'maxlength': '16'
            }),
            'transaction_amount': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter amount'
            }),
            'merchant_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter merchant name'
            }),
            'merchant_type': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter merchant type'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter location'
            }),
        }
