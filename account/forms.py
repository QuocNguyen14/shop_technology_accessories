from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)

from .models import Customer, Address


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line", "address_line2", "town_city", "postcode"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Tên người nhận"}
        )

        self.fields["phone"].widget.attrs.update({"class": "form-control mb-2 account-form", "placeholder": "Phone"})
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Địa chỉ 1"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Địa chỉ 2"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Thành phố"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Mã bưu chính"}
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):
    name = forms.CharField(label='Username', min_length=4, max_length=50, help_text='bắt buộc')
    email = forms.EmailField(max_length=100, help_text='bắt buộc',
                             error_messages={'required': 'Bạn cần nhập email để đăng ký'})
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Xác nhận mật khẩu', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('name', 'email',)

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        r = Customer.objects.filter(name=name)
        if r.count():
            raise forms.ValidationError("Username đã tồn tại")
        return name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Mật khẩu không khớp')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Vui lòng sử dụng email khác, email đã được sử dụng')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Mật khẩu'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Xác nhận mật khẩu'})


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError('Rất tiếc, chúng tôi không thể tìm thấy địa chỉ email đó')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Mật khẩu mới', 'id': 'form-new-pass1'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Xác nhận mật khẩu mới', 'id': 'form-new-pass2'}))


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email (không thể chỉnh sửa)', max_length=200,
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}
        )
    )

    name = forms.CharField(
        label='Tên người dùng', min_length=4, max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Name', 'id': 'form-firstname'}
        )
    )

    class Meta:
        model = Customer
        fields = ('email', 'name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
