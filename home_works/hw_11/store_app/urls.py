from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('about/', views.about, name='about'),

    # Category URLs FBV (Function-Based Views)
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    
    # Product URLs CBV (Class-Based Views)
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/add/', views.ProductCreateView.as_view(), name='add_product'),
    path('products/edit/<int:pk>/', views.ProductUpdateView.as_view(), name='edit_product'),
    path('products/delete/<int:pk>/', views.DeleteProductView.as_view(), name='delete_product'),
]