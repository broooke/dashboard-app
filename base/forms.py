from django import forms
from .models import Customer, Order

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ('name','telephone','email',)

class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ('product','customer','status',)