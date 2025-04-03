import pytest
from store_app.models import Category, Product


@pytest.fixture
def category():
    """Фикстура для создания тестовой категории"""
    return Category.objects.create(
        name="Test Category", description="Category Description"
    )


@pytest.fixture
def product(category):
    """Фикстура для создания тестового продукта"""
    return Product.objects.create(
        name="Test Product",
        description="Product Description",
        price=999.99,
        is_available=True,
    )
