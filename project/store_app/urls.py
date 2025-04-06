from django.urls import path, include
from . import views

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    # Основные страницы
    path("", views.main_page, name="main_page"),
    path("about/", views.about, name="about"),
    path("parts/", views.parts, name="parts"),
    path("delivery/", views.delivery, name="delivery"),
    path("map_page/", views.map_page, name="map_page"),
    path("contact/", views.contact, name="contact"),
    # Category URLs FBV (Function-Based Views)
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.add_category, name="add_category"),
    path(
        "categories/edit/<int:category_id>/", views.edit_category, name="edit_category"
    ),
    path(
        "categories/delete/<int:category_id>/",
        views.delete_category,
        name="delete_category",
    ),
    # Product URLs CBV (Class-Based Views)
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path(
        "products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"
    ),
    path("products/add/", views.ProductCreateView.as_view(), name="add_product"),
    path(
        "products/edit/<int:pk>/",
        views.ProductUpdateView.as_view(),
        name="edit_product",
    ),
    path(
        "products/delete/<int:pk>/",
        views.DeleteProductView.as_view(),
        name="delete_product",
    ),
]
