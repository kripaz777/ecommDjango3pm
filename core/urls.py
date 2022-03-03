from django.urls import path
from .views import *

app_name = "core"

urlpatterns = [
    path('', HomeView.as_view(),name = 'core'),
    path('subcategory/<slug>', SubCategoryView.as_view(),name = 'core'),
    path('search', SearchView.as_view(),name = 'search'),
    path('signup', signup,name = 'signup'),

]