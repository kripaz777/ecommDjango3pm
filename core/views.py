from django.shortcuts import render
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
