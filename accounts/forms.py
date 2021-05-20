from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, forms as auth_forms
from .models import *


class Add_Region(forms.ModelForm):
    class Meta:
        model = Region
        fields = '__all__'


class Add_District(forms.ModelForm):
    class Meta:
        model = District
        fields = '__all__'


class Add_Ward(forms.ModelForm):
    class Meta:
        model = Ward
        fields = '__all__'


class Add_Area(forms.ModelForm):
    class Meta:
        model = Street
        fields = '__all__'

class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = User
        exclude = ['password']


class UserUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['is_active','is_staff','date_joined','last_login','user_roles','approval_status','password','is_superuser','groups','user_permissions']


class Add_UserForm(forms.ModelForm):
    error_message = auth_forms.UserCreationForm.error_messages.update(
        {
            "duplicate_username": _(
                "This username has already been taken."
            )
        }
    )
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'firstname', 'middlename',
                  'lastname', 'mobile', 'is_staff','user_roles','password']

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise forms.ValidationError("Duplicate_username")

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords doesn't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# User Login Form
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")
        return super(UserLoginForm, self).clean()


class ProfileCompleteForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model = User
        fields = [
            'date_of_birth',
            'address',
            'region',
            'district',
            'photo',
            'Bio']
        labels = {
            'date_of_birth':'Date of Birth',
            'address':'Home Address',
            'region':'Home Region',
            'district':'Home District',
            'photo':'User Profile Picture',
            'Bio':'Bio/ Others'
        }
