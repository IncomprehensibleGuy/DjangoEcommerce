from django import forms

from .models import Order, ReceiveMethod


class CreateOrderForm(forms.ModelForm):

    RECEIVE_METHOD_CHOICES = [(method.title, method.title) for method in ReceiveMethod.objects.all()]

    def get_default_receive_method(self, receive_method):
        for choice in self.RECEIVE_METHOD_CHOICES:
            if receive_method in choice:
                return choice

    payment_method = forms.ChoiceField(choices=Order.PAYMENT_METHOD_CHOICES, widget=forms.RadioSelect)
    delivery_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['placeholder'] = 'Населённый пункт'
        self.fields['receive_method'].widget.attrs['class'] = 'select form-control'
        #self.fields['receive_method'].choices = self.RECEIVE_METHOD_CHOICES
        #self.fields['receive_method'].initial = self.get_default_receive_method('Самовывоз')
        self.fields['address'].label = 'Город, Улица, Номер дома, Корпус'
        self.fields['delivery_date'].label = 'Дата доставки'
        self.fields['payment_method'].widget.attrs['class'] = 'payment-list'

        self.payment_method_card = Order.PAYMENT_METHOD_CHOICES[0][1]
        self.payment_method_cash = Order.PAYMENT_METHOD_CHOICES[1][1]

    class Meta:
        model = Order
        fields = (
            'city', 'receive_method', 'address', 'apartment_number', 'porch_number','floor_number','intercom',
            'full_passport_name','phone','email','delivery_date','delivery_time','payment_method','comment',
        )
