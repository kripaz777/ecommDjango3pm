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

