from django.shortcuts import render,redirect
from django.views.generic import View
from .models import *
# Create your views here.
class BaseView(View):
	views = {}

class HomeView(BaseView):
	def get(self,request):
		self.views['categories'] = Category.objects.all()
		self.views['subcategories'] = SubCategory.objects.all()
		self.views['products'] = Product.objects.all()
		self.views['ads1'] = Ad.objects.filter(rank = 1)
		self.views['ads2'] = Ad.objects.filter(rank = 2)
		self.views['ads3'] = Ad.objects.filter(rank = 3)
		self.views['ads4'] = Ad.objects.filter(rank = 4)

		self.views['sliders'] = Slider.objects.all()

		return render(request,'index.html',self.views)

class SubCategoryView(BaseView):
	def get(self,request,slug):
		subcat = SubCategory.objects.get(slug = slug).id
		self.views['subcat_products'] = Product.objects.filter(subcategory_id = subcat)
		self.views['subcat_title'] = SubCategory.objects.get(slug = slug).name
		return render(request,'subcategory.html',self.views)

class DetailView(BaseView):
	def get(self,request,slug):
		self.views['detail_products'] = Product.objects.filter(id = slug)
		return render(request,'single.html',self.views)

class SearchView(BaseView):
	def get(self,request):
		if request.method == 'GET':
			query = request.GET['query']
			self.views['search_name'] = query
			self.views['search_product'] = Product.objects.filter(name__icontains = query)
		return render(request,'search.html',self.views)

from django.contrib.auth.models import User
from django.contrib import messages
def signup(request):
	if request.method == "POST":
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		cpassword = request.POST['cpassword']
		if password == cpassword:
			if User.objects.filter(username = username).exists():
				messages.error(request,"The username is already usded.")
				return redirect('core:signup')

			elif User.objects.filter(email = email).exists():
				messages.error(request,"The email is already used.")
				return redirect('core:signup')

			else:
				user = User.objects.create_user(
					username = username,
					email = email,
					password = password
					)
				user.save()
				return redirect('/')
		else:
			messages.error(request,"The email is already used.")
			return redirect('core:signup')

	return render(request,'register.html')

from django.contrib.auth.decorators import login_required
@login_required
def cart(request,id):
	my_product = Product.objects.get(id = id)
	if Cart.objects.filter(product_id = id,user=request.user.username,checkout = False).exists():
		price = my_product.price
		discounted_price = my_product.discounted_price
		if discounted_price > 0:
			original_price = discounted_price
		else:
			original_price = price

		quantity = Cart.objects.get(product_id = id).quantity
		quantity = quantity +1
		total = quantity*original_price
		Cart.objects.filter(product_id = id).update(quantity = quantity,total = total)

	else:
		price = my_product.price
		discounted_price = my_product.discounted_price
		if discounted_price > 0:
			original_price = discounted_price
		else:
			original_price = price
		data = Cart.objects.create(
			user = request.user.username,
			product_id = id,
			quantity = 1,
			items = Product.objects.get(id = id),
			total = original_price)
		data.save()

	return redirect('/my_cart')

def deletecart(request,id):
	if Cart.objects.filter(product_id = id,user=request.user.username,checkout = False).exists():
		Cart.objects.filter(product_id = id,user=request.user.username,checkout = False).delete()
	return redirect('/my_cart')

def removecart(request,id):
	cart = Cart.objects.filter(product_id = id,user=request.user.username,checkout = False)
	quantity = Cart.objects.get(product_id = id,user=request.user.username,checkout = False).quantity
	my_product = Product.objects.get(id = id)
	price = my_product.price
	discounted_price = my_product.discounted_price
	if discounted_price > 0:
		original_price = discounted_price
	else:
		original_price = price
	if cart.exists():
		if quantity>1:
			quantity = quantity -1
			total = quantity*original_price
			cart.update(quantity = quantity,total = total)
	return redirect('/my_cart')



class CartView(BaseView):
	def get(self,request):
		self.views["my_cart"] = Cart.objects.filter(user=request.user.username,checkout = False)
		return render(request,'wishlist.html',self.views)

from django.core.mail import EmailMessage
def contact(request):
	if request.method == "POST":
		name = request.POST['name']
		email = request.POST['email']
		message = request.POST['message']
		data = Contact.objects.create(
			name = name,
			email = email,
			message = message
			)
		data.save()
		try:
			email = EmailMessage(
	    			'Hello',
	    			'Hello thanks for messaging us. We will get back to you.',
	    			'aiforcoral@gmail.com',
				    [email],
				)
			email.send()
		except:
			pass
		else:
			message.success(request,'Emeil has sent !')
			return redirect('core:contact')
	return render(request,'contact.html')


# -----------------------------------API--------------------------
from rest_framework import routers, serializers, viewsets
from .serializers import *
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = (DjangoFilterBackend,OrderingFilter,SearchFilter)
    filter_fields = ['id','name','price','labels','category','subcategory']
    ordering_fields = ['price','title','id']
    search_fields = ['name','description','overview']