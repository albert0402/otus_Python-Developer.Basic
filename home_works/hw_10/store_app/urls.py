from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),  
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('about/', views.about, name='about'),
]