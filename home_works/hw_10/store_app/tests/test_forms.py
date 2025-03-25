import pytest
from store_app.forms import ProductModelForm, CategoryModelForm
from store_app.models import Product, Category

@pytest.mark.django_db
def test_product_form_valid_data():
    category = Category.objects.create(name="Test Category", description="Test Description")
    form = ProductModelForm(data={
        'name': 'Test Product',
        'description': 'A great product',
        'price': 100,
        'categories': [category.id],
        'is_available': True
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_product_form_invalid_price():
    form = ProductModelForm(data={
        'name': 'Test Product',
        'description': 'A great product',
        'price': -10,  # Неверное значение
        'categories': [],
        'is_available': True
    })
    assert not form.is_valid()
    assert 'price' in form.errors
    assert form.errors['price'] == ["Цена не может быть отрицательной."]

@pytest.mark.django_db
def test_product_form_invalid_name():
    form = ProductModelForm(data={
        'name': 'ab',  # Слишком короткое имя
        'description': 'A great product',
        'price': 50,
        'categories': [],
        'is_available': True
    })
    assert not form.is_valid()
    assert 'name' in form.errors
    assert form.errors['name'] == ["Название товара должно содержать не менее 3 символов."]

@pytest.mark.django_db
def test_category_form_valid_data():
    form = CategoryModelForm(data={
        'name': 'Electronics',
        'description': 'Devices and gadgets'
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_category_form_invalid_name():
    form = CategoryModelForm(data={
        'name': 'ab',  # Слишком короткое имя
        'description': 'Devices and gadgets'
    })
    assert not form.is_valid()
    assert 'name' in form.errors
    assert form.errors['name'] == ["Название категории должно содержать не менее 3 символов."]