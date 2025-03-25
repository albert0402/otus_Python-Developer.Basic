import pytest
from store_app.models import Category, Product

@pytest.mark.django_db
def test_create_category():
    """Проверка создания категории"""
    category = Category.objects.create(name="Electronics", description="Gadgets and devices")
    assert category.id is not None
    assert category.name == "Electronics"

@pytest.mark.django_db
def test_read_category(category):
    """Проверка чтения данных категории"""
    fetched_category = Category.objects.get(id=category.id)
    assert fetched_category.name == "Test Category"

@pytest.mark.django_db
def test_update_category(category):
    """Проверка обновления категории"""
    category.name = "Updated Category"
    category.save()
    updated_category = Category.objects.get(id=category.id)
    assert updated_category.name == "Updated Category"

@pytest.mark.django_db
def test_delete_category(category):
    """Проверка удаления категории"""
    category_id = category.id
    category.delete()
    assert not Category.objects.filter(id=category_id).exists()

@pytest.mark.django_db
def test_category_str(category):
    """Проверка строкового представления категории"""
    assert str(category) == category.name

@pytest.mark.django_db
def test_category_get_products(category, product):
    """Проверка метода get_products у Category"""
    category.products.add(product)
    assert list(category.get_products()) == [product]

@pytest.mark.django_db
def test_create_product():
    """Проверка создания продукта"""
    product = Product.objects.create(
        name="Smartphone",
        description="Flagship phone",
        price=50000,
        is_available=True
    )
    assert product.id is not None
    assert product.name == "Smartphone"

@pytest.mark.django_db
def test_read_product(product):
    """Проверка чтения данных продукта"""
    fetched_product = Product.objects.get(id=product.id)
    assert fetched_product.name == "Test Product"

@pytest.mark.django_db
def test_update_product(product):
    """Проверка обновления продукта"""
    product.price = 1099.99
    product.save()
    updated_product = Product.objects.get(id=product.id)
    assert updated_product.price == 1099.99

@pytest.mark.django_db
def test_delete_product(product):
    """Проверка удаления продукта"""
    product_id = product.id
    product.delete()
    assert not Product.objects.filter(id=product_id).exists()

@pytest.mark.django_db
def test_product_str(product):
    """Проверка строкового представления продукта"""
    assert str(product) == product.name

@pytest.mark.django_db
def test_product_get_category_names(product, category):
    """Проверка метода get_category_names у Product"""
    product.categories.add(category)
    assert product.get_category_names() == category.name

@pytest.mark.django_db
def test_product_get_category_names_multiple(product):
    """Проверка метода get_category_names с несколькими категориями"""
    category1 = Category.objects.create(name="Tech")
    category2 = Category.objects.create(name="Gadgets")
    product.categories.add(category1, category2)
    assert product.get_category_names() == "Tech, Gadgets"

@pytest.mark.django_db
def test_product_get_category_names_empty(product):
    """Проверка метода get_category_names без категорий"""
    assert product.get_category_names() == "Без категории"