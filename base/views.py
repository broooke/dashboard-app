from django.shortcuts import render,redirect
from .models import (
					Customer, Product,
					Order,Tag
					)
from .forms import CustomerForm, OrderForm
from django.contrib import messages


# Create your views here.

def homeView(request):
	customers = Customer.objects.all().order_by('name')
	orders = Order.objects.all()
	orders_total = len(orders)
	orders_delivered = len(orders.filter(status='Delivered'))
	orders_pending = len(orders.filter(status='Pending'))
	print(orders_total)

	context = {
	'customers':customers,
	'orders':orders,
	'orders_total':orders_total,
	'orders_delivered':orders_delivered,
	'orders_pending':orders_pending,
	}

	return render(request,'main/home.html', context)

def customerView(request, user_id):
	customer = Customer.objects.get(id=user_id)
	products = Product.objects.all()
	orders = Order.objects.filter(customer=customer)
	orders_status = Order.objects.all()
	a = orders_status.values('status')

	if 'product' in request.GET:
		product = request.GET['product']
		status = request.GET['status']
		orders = orders.filter(product__name__icontains=product,
			status__icontains=status)


	context={
		'orders':orders,
		'customer':customer,
		'products':products,
		'orders_status':orders_status,
	}

	return render(request,'main/customer.html',context)

def productsView(request):
	products = Product.objects.all().order_by('name')

	context = {
		'products':products,
	}
	return render(request,'main/products.html', context)

def createCustomerView(request):
	if request.method == 'POST':
		form = CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('home')
		else:
			messages.info(request, 'Three credits remain in your account.')
	else:
		form = CustomerForm()

	context = {'form':form}

	return render(request,'main/createcustomer.html',context)

def createOrderView(request):
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('home')
		else:
			messages.info(request, 'Three credits remain in your account.')
	else:
		form = OrderForm()

	context = {'form':form}

	return render(request,'main/createorder.html',context)
