from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, null=True)
	telephone = models.CharField(max_length=12, null=True)
	email = models.EmailField(max_length=100, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	profile_picture = models.ImageField(default="default.png", null=True, blank=True)

	def __str__(self):
		return self.name

	def total_orders(self):
		return self.order_set.all()

	@property
	def get_image(self):
		url = ''
		try:
			url = self.profile_picture.url
		except:
			url = ''
		return url
		

class Tag(models.Model):
	name = models.CharField(max_length=100, null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY = (
			('Indoor','Indoor'),
			('Out Door','Out Door'),
			)

	name = models.CharField(max_length=100, null=True)
	price = models.FloatField(null=True)
	description = models.CharField(max_length=400,null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True)
	category = models.CharField(max_length=100, null=True, choices=CATEGORY)
	tag = models.ManyToManyField(Tag)
	def __str__(self):
		return self.name

class Order(models.Model):
	STATUS = (
			('Pending','Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered','Delivered'),
			)

	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=1000, null=True)

	def __str__(self):
		return self.status		

	# def get_status(self):
	# 	a = []
	# 	for status in self.STATUS:
	# 		a.append(status[0])
	# 	return a

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
	first_name = models.CharField(max_length=200, null=True, blank=True)
	last_name = models.CharField(max_length=200, null=True, blank=True)
	phone = models.CharField(max_length=30, null=True, blank=True)

	def __str__(self):
		return str(self.user)


