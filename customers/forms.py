from django import forms

from .models import Customer


class LoginForm(forms.Form):

    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль'

    def clean_email(self):
        email = self.cleaned_data['email']
        customer = Customer.objects.filter(email=email).first()
        if not customer:
            raise forms.ValidationError('Пользователь с таким e-mail не существует')
        return email

    def clean_password(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        customer = Customer.objects.filter(email=email).first()
        if not customer and not customer.check_password(password):
            raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data['password']

    class Meta:
        model = Customer
        fields = ['email', 'password']


class RegistrationForm(forms.ModelForm):

    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'

    def clean_email(self):
        email = self.cleaned_data['email']
        customer = Customer.objects.filter(email=email).first()
        if customer:
            raise forms.ValidationError('Пользователь с таким e-mail уже существует')
        return email

    def clean_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password1

    class Meta:
        model = Customer
        fields = ['email', 'password1', 'password2']


class ConfirmEmailForm(forms.Form):

    d1 = forms.IntegerField(min_value=1, max_value=9)
    d2 = forms.IntegerField(min_value=1, max_value=9)
    d3 = forms.IntegerField(min_value=1, max_value=9)
    d4 = forms.IntegerField(min_value=1, max_value=9)
    d5 = forms.IntegerField(min_value=1, max_value=9)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['d1'].widget.attrs['class'] = 'form-control'
        self.fields['d1'].widget.attrs['min'] = '0'
        self.fields['d2'].widget.attrs['class'] = 'form-control'
        self.fields['d2'].widget.attrs['min'] = '0'
        self.fields['d3'].widget.attrs['class'] = 'form-control'
        self.fields['d3'].widget.attrs['min'] = '0'
        self.fields['d4'].widget.attrs['class'] = 'form-control'
        self.fields['d4'].widget.attrs['min'] = '0'
        self.fields['d5'].widget.attrs['class'] = 'form-control'
        self.fields['d5'].widget.attrs['min'] = '0'

    class Meta:
        model = Customer
        fields = ['d1', 'd2', 'd3', 'd4', 'd5']
