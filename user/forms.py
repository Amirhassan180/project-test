from django import forms
from django.contrib.auth.forms import UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User

from .models import Profile


class UserInfoForm(forms.ModelForm):
    # Define form fields with labels and make them optional
    phone = forms.CharField(required=False, label='شماره تلفن')
    address1 = forms.CharField(required=False, label='آدرس ۱')
    address2 = forms.CharField(required=False, label='آدرس 2')
    city = forms.CharField(required=False, label='شهر')
    state = forms.CharField(required=False, label='استان')
    zipCode = forms.CharField(required=False, label='کد پستی')
    country = forms.CharField(required=False, label='کشور')

    class Meta:
        model = Profile
        fields = ('phone', 'address1', 'address2', 'city', 'state', 'zipCode', 'country')

    def __init__(self, *args, **kwargs):
        # Call the parent class's constructor
        super(UserInfoForm, self).__init__(*args, **kwargs)

        # Iterate through visible fields to add CSS classes and placeholders
        for item in self.visible_fields():
            item.field.widget.attrs['class'] = 'form-control'
            # Set the placeholder if it exists in the placeholders dictionary


class ChangePasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for item in self.visible_fields():
            item.field.widget.attrs.update({'class': 'form-control'})


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'نام کاربری',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'ایمیل',
        }

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        # حذف فیلد password از فرم در صورت وجود
        self.fields.pop('password', None)

        for item in self.visible_fields():
            item.field.widget.attrs['class'] = 'form-control'


class LoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for item in self.visible_fields():
            item.field.widget.attrs['class'] = 'form-control'

    username = forms.CharField(required=True, label="نام کاربری")
    password = forms.CharField(required=True, label="رمز عبور", widget=forms.PasswordInput)


class RegisterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for item in self.visible_fields():
            item.field.widget.attrs['class'] = 'form-control'

    name = forms.CharField(required=True, label='نام')
    family = forms.CharField(required=True, label='نام خانوادگی')
    email = forms.CharField(required=True, label='ایمیل')
    username = forms.CharField(required=True, label="نام کاربری")
    password = forms.CharField(required=True, label="رمز عبور", widget=forms.PasswordInput)
