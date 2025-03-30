import pytest
from django.urls import reverse
from django.test import Client
from store_app.models import Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def category():
    return Category.objects.create(name="Tech", description="Tech products")


@pytest.fixture
def product(category):
    product = Product.objects.create(
        name="Laptop", 
        description="Gaming laptop", 
        price=1500, 
        is_available=True
    )
    product.categories.add(category)
    return product


@pytest.mark.django_db
def test_main_page(client):
    response = client.get(reverse("main_page"))
    assert response.status_code == 200
    assert "store_app/home.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_about_page(client):
    response = client.get(reverse("about"))
    assert response.status_code == 200
    assert "store_app/about.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_category_list(client, category):
    response = client.get(reverse("category_list"))
    assert response.status_code == 200
    assert category.name in response.content.decode()


@pytest.mark.django_db
def test_add_category_get(client):
    response = client.get(reverse("add_category"))
    assert response.status_code == 200
    assert "store_app/edit_category.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_add_category_post(client):
    response = client.post(
        reverse("add_category"), 
        {"name": "Books", "description": "All kinds of books"}
    )
    assert response.status_code == 302
    assert Category.objects.filter(name="Books").exists()


@pytest.mark.django_db
def test_edit_category_get(client, category):
    response = client.get(reverse("edit_category", args=[category.id]))
    assert response.status_code == 200
    assert "store_app/edit_category.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_edit_category_post(client, category):
    response = client.post(
        reverse("edit_category", args=[category.id]), 
        {"name": "Updated Tech", "description": "Updated"}
    )
    assert response.status_code == 302
    category.refresh_from_db()
    assert category.name == "Updated Tech"


@pytest.mark.django_db
def test_product_list(client, product):
    response = client.get(reverse("product_list"))
    assert response.status_code == 200
    assert product.name in response.content.decode()


@pytest.mark.django_db
def test_product_list_filtering(client, product, category):
    # Test category filter
    response = client.get(reverse("product_list") + f"?category={category.id}")
    assert response.status_code == 200
    assert product.name in response.content.decode()

    # Test price filters
    response = client.get(reverse("product_list") + "?min_price=1000")
    assert response.status_code == 200
    assert product.name in response.content.decode()

    response = client.get(reverse("product_list") + "?max_price=2000")
    assert response.status_code == 200
    assert product.name in response.content.decode()

    # Test sorting
    for sort_option in ["price_asc", "price_desc", "name_asc", "name_desc"]:
        response = client.get(reverse("product_list") + f"?sort={sort_option}")
        assert response.status_code == 200


@pytest.mark.django_db
def test_product_list_no_products(client):
    response = client.get(reverse("product_list"))
    assert response.status_code == 200
    assert "Нет товаров" in response.content.decode()


@pytest.mark.django_db
def test_product_detail(client, product):
    response = client.get(reverse("product_detail", args=[product.id]))
    assert response.status_code == 200
    assert product.name in response.content.decode()


@pytest.mark.django_db
def test_product_detail_not_found(client):
    response = client.get(reverse("product_detail", args=[999]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_add_product_get(client):
    response = client.get(reverse("add_product"))
    assert response.status_code == 200
    assert "store_app/edit_product.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_add_product_post(client, category):
    image = SimpleUploadedFile(
        "test_image.jpg", 
        b"file_content", 
        content_type="image/jpeg"
    )
    response = client.post(
        reverse("add_product"),
        {
            "name": "Tablet",
            "description": "New tablet",
            "price": 500,
            "is_available": "on",
            "categories": [category.id],
            "image": image
        }
    )
    assert response.status_code == 302
    assert Product.objects.filter(name="Tablet").exists()


@pytest.mark.django_db
def test_edit_product_get(client, product):
    response = client.get(reverse("edit_product", args=[product.id]))
    assert response.status_code == 200
    assert "store_app/edit_product.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_edit_product_post(client, product, category):
    response = client.post(
        reverse("edit_product", args=[product.id]),
        {
            "name": "New Laptop",
            "description": "Updated model",
            "price": 1200,
            "is_available": "on",
            "categories": [category.id]
        }
    )
    assert response.status_code == 302
    product.refresh_from_db()
    assert product.name == "New Laptop"


@pytest.mark.django_db
def test_delete_product_view(client, product):
    response = client.get(reverse("delete_product", args=[product.id]))
    assert response.status_code == 200
    assert "store_app/delete_product.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_delete_product_post(client, product):
    response = client.post(reverse("delete_product", args=[product.id]))
    assert response.status_code == 302
    assert not Product.objects.filter(id=product.id).exists()


@pytest.mark.django_db
def test_delete_product_not_found(client):
    response = client.post(reverse("delete_product", args=[999]))
    assert response.status_code == 404