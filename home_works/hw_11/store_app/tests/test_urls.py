import pytest
from django.urls import reverse, resolve
from store_app import views

@pytest.mark.parametrize("url_name, view_func, kwargs", [
    ("main_page", views.main_page, None),
    ("about", views.about, None),
    ("category_list", views.category_list, None),
    ("add_category", views.add_category, None),
    ("edit_category", views.edit_category, {"category_id": 1}),
    ("product_list", views.product_list, None),
    ("product_detail", views.product_detail, {"product_id": 1}),
    ("add_product", views.add_product, None),
    ("edit_product", views.edit_product, {"product_id": 1}),
    ("delete_product", views.DeleteProductView, {"pk": 1}),
])
def test_urls(url_name, view_func, kwargs):
    """Проверка соответствия имен маршрутов и функций-представлений"""
    url = reverse(url_name, kwargs=kwargs) if kwargs else reverse(url_name)
    resolved_func = resolve(url).func
    if hasattr(resolved_func, "view_class"):
        resolved_func = resolved_func.view_class
    assert resolved_func == view_func