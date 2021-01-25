from django import forms
from .models import Customer, Order

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']

class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ('product','customer','status',)