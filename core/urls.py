from django.urls import path
from .views import *

app_name = "core"

urlpatterns = [
    path('', HomeView.as_view(),name = 'core'),
    path('subcategory/<slug>', SubCategoryView.as_view(),name = 'core'),
    path('details/<slug>', DetailView.as_view(),name = 'core'),
    path('search', SearchView.as_view(),name = 'search'),
    path('signup', signup,name = 'signup'),
    path('cart/<id>', cart,name = 'cart'),
    path('deletecart/<id>', deletecart,name = 'deletecart'),
    path('removecart/<id>', removecart,name = 'removecart'),
    path('my_cart', CartView.as_view(),name = 'my_cart'),
    path('contact', contact,name = 'contact'),

]