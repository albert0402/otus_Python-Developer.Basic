from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    DeleteView, DetailView, ListView, CreateView, UpdateView
)
from django.contrib import messages
from .models import Product, Category
from .forms import ProductModelForm, CategoryModelForm
from .tasks import send_category_notification, send_product_notification

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
            category = form.save()
            # Отправка уведомления о добавлении категории
            send_category_notification.delay(
                action="добавлена",
                category_id=category.id
            )
            messages.success(request, "Категория успешно добавлена!")
            return redirect("category_list")
    else:
        form = CategoryModelForm()
    return render(request, "store_app/category_edit.html", {"form": form, "action": "Добавить категорию"})

def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        form = CategoryModelForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            # Отправка уведомления об изменении категории
            send_category_notification.delay(
                action="изменена",
                category_id=category.id
            )
            messages.success(request, "Категория успешно обновлена!")
            return redirect("category_list")
    else:
        form = CategoryModelForm(instance=category)
    return render(request, "store_app/category_edit.html", {"form": form, "action": "Редактировать категорию"})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        # Отправка уведомления перед удалением
        send_category_notification.delay(
            action="удалена",
            category_id=category.id
        )
        category.delete()
        messages.success(request, "Категория успешно удалена!")
        return redirect(reverse('category_list'))
    
    return render(request, "store_app/category_delete.html", {'category': category})

# --------- Products ---------
class ProductListView(ListView):
    model = Product
    template_name = "store_app/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("categories")
        
        category_id = self.request.GET.get("category")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        sort = self.request.GET.get("sort")

        if category_id:
            queryset = queryset.filter(categories__id=category_id)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        sort_options = {
            "price_asc": "price",
            "price_desc": "-price",
            "name_asc": "name",
            "name_desc": "-name",
        }
        if sort in sort_options:
            queryset = queryset.order_by(sort_options[sort])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = "store_app/product_detail.html"
    context_object_name = "product"

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductModelForm
    template_name = "store_app/edit_product.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Отправка уведомления о добавлении товара
        send_product_notification.delay(
            action="добавлен",
            product_id=self.object.id
        )
        messages.success(self.request, "Товар успешно добавлен!")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Добавить товар"
        return context

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductModelForm
    template_name = "store_app/edit_product.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Отправка уведомления об изменении товара
        send_product_notification.delay(
            action="изменен",
            product_id=self.object.id
        )
        messages.success(self.request, "Товар успешно обновлен!")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Редактировать товар"
        return context

class DeleteProductView(DeleteView):
    model = Product
    template_name = "store_app/delete_product.html"
    success_url = reverse_lazy("product_list")

    def delete(self, request, *args, **kwargs):
        # Отправка уведомления перед удалением
        product = self.get_object()
        send_product_notification.delay(
            action="удален",
            product_id=product.id
        )
        messages.success(request, "Товар успешно удален!")
        return super().delete(request, *args, **kwargs)