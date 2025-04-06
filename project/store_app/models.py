from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


# ======================
# User Configuration
# ======================

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('ADMIN', 'Администратор'),
        ('STAFF', 'Персонал'),
        ('CUSTOMER', 'Покупатель'),
    )
    
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='CUSTOMER')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="custom_user_groups",
        related_query_name="custom_user",
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_permissions",
        related_query_name="custom_user",
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username


# ======================
# Shop Configuration
# ======================

class Category(models.Model):
    """Модель категории товаров"""
    name = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name="Название"
    )
    description = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Описание"
    )
    image = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Путь к изображению относительно папки static (например: 'categories/filters.jpg')",
        verbose_name="Изображение"
    )

    def __str__(self):
        return self.name

    def get_products(self):
        """Получить все товары категории"""
        return self.products.all()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    """Модель товара"""
    name = models.CharField(
        max_length=100,
        verbose_name="Название"
    )
    description = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Описание"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        null=True, 
        blank=True,
        verbose_name="Дата создания"
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="Доступен"
    )
    categories = models.ManyToManyField(
        Category, 
        related_name="products", 
        blank=True,
        verbose_name="Категории"
    )
    image = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Путь к изображению товара",
        verbose_name="Изображение товара"
    )

    def __str__(self):
        return self.name

    def get_category_names(self):
        """Получить названия всех категорий через запятую"""
        return ", ".join([cat.name for cat in self.categories.all()]) or "Без категории"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']


class Order(models.Model):
    """Модель заказа"""
    STATUS_CHOICES = (
        ('PENDING', 'В обработке'),
        ('PROCESSING', 'В процессе'),
        ('COMPLETED', 'Завершен'),
        ('CANCELLED', 'Отменен'),
    )
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Пользователь"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name="Статус"
    )
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0,
        verbose_name="Общая сумма"
    )
    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий"
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        verbose_name="Телефон"
    )
    address = models.TextField(
        blank=True,
        verbose_name="Адрес доставки"
    )    

    def update_total(self):
        """Обновить общую сумму заказа"""
        self.total_price = sum(item.total_price for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']


class OrderItem(models.Model):
    """Элемент заказа"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Количество"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Цена за единицу"
    )

    @property
    def total_price(self):
        """Общая стоимость позиции"""
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"