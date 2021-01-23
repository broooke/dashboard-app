from django.shortcuts import render

# Create your views here.

def homeView(request):
	return render(request,'main/home.html')

def customerView(request):
	return render(request,'main/customer.html')

def productsView(request):
	return render(request,'main/products.html')