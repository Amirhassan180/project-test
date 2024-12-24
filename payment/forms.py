from django import forms

from .models import ShippingAddress


class ShippingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ShippingForm, self).__init__(*args, **kwargs)
        for item in self.visible_fields():
            item.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ShippingAddress
        fields = '__all__'
        exclude = ['user']

    shipping_full_name = forms.CharField(required=True, label='نام و نام خانوادگی')
    shipping_phone_number = forms.CharField(required=True, label='شماره تلفن')
    shipping_email = forms.EmailField(required=True, label='ایمیل')
    shipping_address1 = forms.CharField(required=True, label='آدرس ۱')
    shipping_address2 = forms.CharField(required=False, label='آدرس ۲')
    shipping_city = forms.CharField(required=True, label='شهر')
    shipping_state = forms.CharField(required=False, label='استان')
    shipping_zipCode = forms.CharField(required=False, label='کد پستی')
    shipping_country = forms.CharField(required=True, label='کشور')


class PaymentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        for item in self.visible_fields():
            item.field.widget.attrs['class'] = 'form-control'

    cart_name = forms.CharField(required=True, label='نام کارت')
    cart_number = forms.CharField(required=True, label='شماره کارت')
    cart_exp_date = forms.CharField(required=True, label='تاریخ انقظا')
    cart_cvv_number = forms.CharField(required=True, label='cvv')
    cart_address1 = forms.CharField(required=True, label='آدرس 1')
    cart_address2 = forms.CharField(required=False, label='آدرس 2')
    cart_city = forms.CharField(required=True, label='شهر')
    cart_state = forms.CharField(required=True, label='استان')
    cart_zipCode = forms.CharField(required=True, label='کدپستی')
    cart_country = forms.CharField(required=True, label='کشور')
