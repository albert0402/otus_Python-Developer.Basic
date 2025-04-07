import pytest
from django.contrib.admin.sites import site
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from store_app.admin import CategoryAdmin, ProductAdmin
from store_app.models import Category, Product


@pytest.fixture
def request_factory():
    """Создает объект запроса с поддержкой сессий и сообщений"""
    factory = RequestFactory()
    request = factory.get("/")

    # Добавляем поддержку сессии
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()

    # Добавляем поддержку сообщений
    setattr(request, "_messages", FallbackStorage(request))

    return request


@pytest.fixture
def category():
    """Фикстура для создания тестовой категории"""
    return Category.objects.create(name="Test Category", description="Test Description")


@pytest.fixture
def product(category):
    """Фикстура для создания тестового товара с привязкой к категории"""
    product = Product.objects.create(
        name="Test Product",
        description="Test Description",
        price=100.00,
        is_available=True
    )
    product.categories.add(category)
    return product


@pytest.mark.django_db
def test_category_admin_actions(request_factory):
    """Тестирование действия админки для добавления новой категории"""
    request = request_factory
    category_admin = CategoryAdmin(model=Category, admin_site=site)

    initial_count = Category.objects.count()
    category_admin.add_new_category(request, Category.objects.all())

    assert Category.objects.count() == initial_count + 1
    assert Category.objects.filter(name="New Category").exists()


@pytest.mark.django_db
def test_product_admin_actions(request_factory, category):
    """Тестирование действия админки для добавления нового товара"""
    request = request_factory
    product_admin = ProductAdmin(model=Product, admin_site=site)

    initial_count = Product.objects.count()
    product_admin.add_new_product(request, Product.objects.all())

    assert Product.objects.count() == initial_count + 1
    new_product = Product.objects.filter(name="New Product").first()
    assert new_product is not None
    assert new_product.categories.exists()


@pytest.mark.django_db
def test_update_product_details(request_factory, product):
    """Тестирование действия админки для обновления деталей товара"""
    request = request_factory
    product_admin = ProductAdmin(model=Product, admin_site=site)

    product_admin.update_product_details(request, Product.objects.filter(id=product.id))
    product.refresh_from_db()

    assert product.name == "Updated Product"
    assert product.description == "Updated description"
    assert product.price == 99.99


@pytest.mark.django_db
def test_set_price_action(request_factory, product):
    """Тестирование действия админки для установки цены"""
    request = request_factory
    product_admin = ProductAdmin(model=Product, admin_site=site)

    product_admin.set_price(request, Product.objects.filter(id=product.id))
    product.refresh_from_db()

    assert product.price == 500.00


@pytest.mark.django_db
def test_mark_out_of_stock_action(request_factory, product):
    """Тестирование действия админки для пометки товара как отсутствующего"""
    request = request_factory
    product_admin = ProductAdmin(model=Product, admin_site=site)

    assert product.is_available is True
    product_admin.mark_out_of_stock(request, Product.objects.filter(id=product.id))
    product.refresh_from_db()

    assert product.is_available is False


@pytest.mark.django_db
def test_category_admin_display():
    """Тестирование конфигурации отображения CategoryAdmin"""
    category_admin = CategoryAdmin(model=Category, admin_site=site)
    
    assert list(category_admin.list_display) == ['name', 'description']
    assert category_admin.ordering == ('name',)
    assert category_admin.search_fields == ('name', 'description')


@pytest.mark.django_db
def test_product_admin_display():
    """Тестирование конфигурации отображения ProductAdmin"""
    product_admin = ProductAdmin(model=Product, admin_site=site)
    
    assert list(product_admin.list_display) == ['name', 'price', 'get_categories', 'is_available']
    assert product_admin.ordering == ('name', 'price')
    assert product_admin.search_fields == ('name', 'description')
    assert 'created_at' in product_admin.readonly_fields


@pytest.mark.django_db
def test_get_categories_method(product, category):
    """Тестирование метода get_categories для отображения категорий товара"""
    product_admin = ProductAdmin(model=Product, admin_site=site)
    result = product_admin.get_categories(product)
    
    assert category.name in result
    assert result == "Test Category"
