from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Product, Category
from .forms import ProductModelForm, CategoryModelForm

def main_page(request):
    return render(request, template_name='store_app/home.html')

def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, template_name='store_app/category_list.html', context=context)

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Получаем минимальную и максимальную цену из базы
    min_price = products.order_by("price").first().price if products.exists() else 0
    max_price = products.order_by("-price").first().price if products.exists() else 1000

    # Фильтр по категории
    category_id = request.GET.get("category")
    if category_id:
        products = products.filter(categories__id=category_id)

    # Фильтр по цене
    min_price_filter = request.GET.get("min_price")
    max_price_filter = request.GET.get("max_price")
    if min_price_filter:
        products = products.filter(price__gte=min_price_filter)
    if max_price_filter:
        products = products.filter(price__lte=max_price_filter)

    # Фильтр по наличию
    in_stock = request.GET.get("in_stock")
    on_order = request.GET.get("on_order")
    if in_stock and not on_order:
        products = products.filter(is_available=True)
    elif on_order and not in_stock:
        products = products.filter(is_available=False)
    
    # Сортировка
    sort_option = request.GET.get("sort")
    if sort_option == "date":
        products = products.order_by("-created_at")
    elif sort_option == "price_asc":
        products = products.order_by("price")
    elif sort_option == "price_desc":
        products = products.order_by("-price")

    context = {
        "products": products,
        "categories": categories,
        "min_price": min_price,
        "max_price": max_price,
    }
    return render(request, "store_app/product_list.html", context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'store_app/product_detail.html', context=context)

def about(request):
    return HttpResponse('About the store')

def add_product(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductModelForm()
    return render(request, 'store_app/add_product.html', {'form': form})

def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductModelForm(instance=product)
    return render(request, 'store_app/edit_product.html', {'form': form, 'product': product})

def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryModelForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryModelForm(instance=category)
    return render(request, 'store_app/edit_category.html', {'form': form, 'category': category})

def add_category(request):
    if request.method == 'POST':
        form = CategoryModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')  
    else:
        form = CategoryModelForm()
    return render(request, 'store_app/add_category.html', {'form': form})