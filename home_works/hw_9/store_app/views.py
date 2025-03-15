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
    context = {'products': products}
    return render(request, template_name='store_app/product_list.html', context=context)

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
            return redirect('product_list')  # Перенаправление на список товаров
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