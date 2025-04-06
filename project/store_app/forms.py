from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Category, User, Order

class UserRegistrationForm(UserCreationForm):
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Номер телефона'
        })
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Адрес доставки'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'address']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Подтверждение пароля'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'user_type']
        labels = {
            'username': 'Логин',
            'email': 'Email',
            'phone': 'Телефон',
            'address': 'Адрес',
            'user_type': 'Тип пользователя'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
        }

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "categories", "is_available", "image"]
        labels = {
            "name": "Название товара",
            "description": "Описание товара",
            "price": "Цена",
            "categories": "Категории",
            "is_available": "Доступен",
            "image": "Изображение товара",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите название товара",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Введите описание товара",
                }
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Введите цену"}
            ),
            "categories": forms.SelectMultiple(attrs={"class": "form-control"}),
            "is_available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "image": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Путь к изображению (например: 'products/oil.jpg')",
                }
            ),
        }

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return round(price, 2)  # Округляем до 2 знаков после запятой

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name.strip()) < 3:
            raise forms.ValidationError(
                "Название товара должно содержать не менее 3 символов."
            )
        return name.strip()

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "image"]
        labels = {
            "name": "Название категории",
            "description": "Описание категории",
            "image": "Изображение категории",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите название категории",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Введите описание категории",
                }
            ),
            "image": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Путь к изображению (например: 'categories/filters.jpg')",
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name.strip()) < 3:
            raise forms.ValidationError(
                "Название категории должно содержать не менее 3 символов."
            )
        return name.strip()

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})
        }

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 70px;'
        })
    )
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput()
    )

class CheckoutForm(forms.Form):
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Номер телефона'
        })
    )
    address = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Адрес доставки'
        })
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Комментарий к заказу (необязательно)'
        })
    )