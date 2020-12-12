from django import forms

from .models import Customer


class LoginForm(forms.Form):

    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'E-mail'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password'].label = 'Пароль'
        self.fields['password'].widget.attrs['class'] = 'form-control'

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

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = Customer
        fields = ['email', 'password']
