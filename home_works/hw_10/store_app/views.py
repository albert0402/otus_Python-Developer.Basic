from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from .models import Product, Category
from .forms import ProductModelForm, CategoryModelForm


def main_page(request):
    return render(request, "store_app/home.html")


def about(request):
    return render(request, "store_app/about.html")


# --------- Categories ---------
def category_list(request):
    categories = Category.objects.all()
    return render(request, "store_app/category_list.html", {"categories": categories})


def add_category(request):
    if request.method == "POST":
        form = CategoryModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("category_list")
    else:
        form = CategoryModelForm()
    return render(request, "store_app/edit_category.html", {"form": form, "action": "Добавить категорию"})


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        form = CategoryModelForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("category_list")
    else:
        form = CategoryModelForm(instance=category)
    return render(request, "store_app/edit_category.html", {"form": form, "action": "Редактировать категорию"})


# --------- Products ---------
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort')

    if category_id:
        products = products.filter(categories__id=category_id)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    if sort == "price_asc":
        products = products.order_by('price')
    elif sort == "price_desc":
        products = products.order_by('-price')
    elif sort == "name_asc":
        products = products.order_by('name')
    elif sort == "name_desc":
        products = products.order_by('-name')

    return render(request, "store_app/product_list.html", {"products": products, "categories": categories})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "store_app/product_detail.html", {"product": product})


def add_product(request):
    if request.method == "POST":
        form = ProductModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductModelForm()
    return render(request, "store_app/product_form.html", {"form": form, "action": "Добавить товар"})


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductModelForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductModelForm(instance=product)
    return render(request, "store_app/product_form.html", {"form": form, "action": "Редактировать товар"})


# --------- Delete Product ---------
class DeleteProductView(DeleteView):
    model = Product
    template_name = "store_app/product_confirm_delete.html"
    success_url = reverse_lazy("product_list")