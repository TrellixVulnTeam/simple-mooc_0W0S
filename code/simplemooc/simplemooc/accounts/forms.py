from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField(label='E-mail')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use.')
        return email


class EditAccountForm(forms.ModelForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        queryset = User.objects.filter(
            email=email).exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError('Email already in use.')
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
