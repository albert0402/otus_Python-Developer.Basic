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

class DeleteCategoryView(DeleteView):
    model = Category
    template_name = "store_app/category_delete.html"
    success_url = reverse_lazy("category_list")

# --------- Products ---------
def product_list(request):
    products = Product.objects.prefetch_related("categories").all()
    categories = Category.objects.all()

    category_id = request.GET.get("category")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort = request.GET.get("sort")

    if category_id:
        products = products.filter(categories__id=category_id)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    sort_options = {
        "price_asc": "price",
        "price_desc": "-price",
        "name_asc": "name",
        "name_desc": "-name",
    }
    if sort in sort_options:
        products = products.order_by(sort_options[sort])

    return render(request, "store_app/product_list.html", {"products": products, "categories": categories})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "store_app/product_detail.html", {"product": product})

def add_product(request):
    if request.method == "POST":
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductModelForm()
    return render(request, "store_app/edit_product.html", {"form": form, "action": "Добавить товар"})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductModelForm(instance=product)
    return render(request, "store_app/edit_product.html", {"form": form, "action": "Редактировать товар"})

class DeleteProductView(DeleteView):
    model = Product
    template_name = "store_app/delete_product.html"
    success_url = reverse_lazy("product_list")