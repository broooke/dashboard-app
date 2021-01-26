from django.shortcuts import render,redirect
from .models import (
					Customer, Product,
					Order,Tag
					)
from .forms import CustomerForm, OrderForm
from django.contrib import messages
from .filters import OrderFilter
from django.forms import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group

# Create your views here.
@login_required(login_url='login')
@admin_only
def homeView(request):
	customers = Customer.objects.all().order_by('name')
	orders = Order.objects.all()
	orders_total = orders.count()
	orders_delivered = orders.filter(status='Delivered').count()
	orders_pending = orders.filter(status='Pending').count()

	context = {
	'customers':customers,
	'orders':orders,
	'orders_total':orders_total,
	'orders_delivered':orders_delivered,
	'orders_pending':orders_pending,
	}

	return render(request,'main/home.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def customerView(request, user_id):
	customer = Customer.objects.get(id=user_id)
	orders = Order.objects.filter(customer=customer)
	total_orders = customer.total_orders()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs

	# if 'product' in request.GET:
	# 	product = request.GET['product']
	# 	status = request.GET['status']
	# 	orders = orders.filter(product__name__icontains=product,
	# 		status__icontains=status)


	context={
		'orders':orders,
		'customer':customer,
		'total_orders':total_orders,
		'myFilter':myFilter,
	}

	return render(request,'main/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def productsView(request):
	products = Product.objects.all().order_by('name')

	context = {
		'products':products,
	}
	return render(request,'main/products.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def createOrderView(request, customer_id):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status',), extra=10)
	customer = Customer.objects.get(id=customer_id)
	if request.method == 'POST':
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('home')
		else:
			messages.info(request, 'Three credits remain in your account.')
	else:
		# form = OrderForm(initial={'customer':customer})
		formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

	context = {'formset':formset}

	return render(request,'main/createorder.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def orderUpdateView(request, order_id):
	order = Order.objects.get(id=order_id)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('home')

	context = {'form':form}

	return render(request,'main/orderupdate.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def orderDeleteView(request, order_id):
	order = Order.objects.get(id=order_id)

	if request.method == 'POST':
		order.delete()
		return redirect('home')

	context = {'order':order}

	return render(request,'main/deleteorder.html', context)

@unauthenticated_user
def signupView(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			messages.success(request, 'Account was created for ' + user.username)
			return redirect('login')
	else:
		form = UserCreationForm()

	context = {'form':form}

	return render(request,'main/signup.html', context)

@unauthenticated_user
def loginView(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('home')
	else:
		form = AuthenticationForm()

	context = {'form':form}

	return render(request,'main/login.html', context)

def logoutView(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def userPageView(request):
	orders = request.user.customer.order_set.all()
	total_orders = orders.count()
	orders_delivered = orders.filter(status='Delivered').count()
	orders_pending = orders.filter(status='Pending').count()

	context={'orders':orders,'total_orders':total_orders,
	'orders_delivered':orders_delivered,'orders_pending':orders_pending}
	return render(request, 'main/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def deleteCustomerView(request, customer_id):
	customer = Customer.objects.get(id=customer_id)
	customer.delete()
	return redirect('home')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def settingsView(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)
	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()
			return redirect('settings')


	context={'form':form, 'customer':customer}
	return render(request, 'main/settings.html', context)