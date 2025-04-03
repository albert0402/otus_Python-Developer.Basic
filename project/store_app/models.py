from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Путь к изображению относительно папки static (например: 'categories/filters.jpg')",
    )

    def __str__(self):
        return self.name

    def get_products(self):
        """Get all products"""
        return self.products.all()


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, related_name="products", blank=True)

    def __str__(self):
        return self.name

    def get_category_names(self):
        """Get all category names joined by comma"""
        return ", ".join([cat.name for cat in self.categories.all()]) or "Без категории"
