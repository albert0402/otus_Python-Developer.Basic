import random
from django.core.management.base import BaseCommand
from store_app.models import Product, Category


class Command(BaseCommand):
    help = "Fills the database with random categories and products"

    def handle(self, *args, **kwargs):
        # Delete old records
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Create categories
        categories = []
        category_names = ["Electronics", "Clothing", "Toys", "Books", "Sports"]
        for name in category_names:
            category = Category.objects.create(
                name=name, description=f"Description of {name}"
            )
            categories.append(category)

        # Create products
        product_names = [
            "Phone",
            "T-shirt",
            "Robot",
            "Novel",
            "Dumbbells",
            "Headphones",
            "Jacket",
            "Lego Set",
            "Encyclopedia",
            "Ball",
        ]
        for name in product_names:
            Product.objects.create(
                name=name,
                description=f"Description of {name}",
                price=random.uniform(10, 1000),
                category=random.choice(categories),
            )

        self.stdout.write(self.style.SUCCESS("Database successfully populated!"))
