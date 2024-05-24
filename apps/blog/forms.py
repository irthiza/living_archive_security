from django import forms
from .models import Blog
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit,Column, HTML
from allauth.account.forms import LoginForm, SignupForm
from django.urls import reverse_lazy


class BlogForm(forms.ModelForm):
    passcode = forms.CharField(label='Passcode', required=False)
    class Meta:
        model = Blog
        fields = ['title', 'body', 'is_private', 'passcode']
        widgets = {
            "author": forms.Select(attrs={'class': 'form-control select2'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.is_private:
            self.fields['passcode'].widget.attrs['class'] = 'passcode-field d-none'
        else:
            self.fields['passcode'].widget.attrs['class'] = 'passcode-field'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6 mb-0'),
                Column('is_private', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('passcode', css_class='form-group col-md-6 mb-0 passcode-field'),  # Add this line
            ),
            Row(
                Column('body', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary')
                ),
            )
        )

    def save(self, commit=True):
        blog = super().save(commit=False)
        if not blog.is_private:
            blog.passcode = '' 
        if commit:
            blog.save()
        return blog

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=100, label='Name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['placeholder'] = self.fields[fieldname].label
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
           
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save'), css_class='kt-login__actions'
                )
            )
        )

    def custom_signup(self, request, user):
        user.username = self.cleaned_data['username']
        user.is_staff = True
        user.save()


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['placeholder'] = self.fields[fieldname].label
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('login', placeholder='Username', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('password', placeholder='Password', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column(
                    HTML('<label class="checkbox"><input type="checkbox" checked="checked" name="remember">'
                         '<span></span> &nbsp;Remember Me</label>'),
                    css_class='form-group text-left col-md-6 mb-5'),
                
            ),
            Row(
                Column(
                    Submit('submit', 'Submit'), css_class='kt-login__actions'
                )
            )
        )

class PasscodeForm(forms.Form):
    passcode = forms.CharField(widget=forms.PasswordInput)