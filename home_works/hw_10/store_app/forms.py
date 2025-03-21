from django import forms
from .models import Product, Category


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 
            'description', 
            'price', 
            'categories', 
            'is_available'
        ]
        labels = {
            'name': 'Название товара',
            'description': 'Описание товара',
            'price': 'Цена',
            'categories': 'Категории',
            'is_available': 'Доступен',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Введите название товара'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Введите описание товара'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Введите цену'
            }),
            'categories': forms.SelectMultiple(attrs={
                'class': 'form-control'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name.strip()) < 3:
            raise forms.ValidationError("Название товара должно содержать не менее 3 символов.")
        return name.strip()


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': 'Название категории',
            'description': 'Описание категории',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Введите название категории'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Введите описание категории'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name.strip()) < 3:
            raise forms.ValidationError("Название категории должно содержать не менее 3 символов.")
        return name.strip()
