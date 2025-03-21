from django.contrib import admin
from store_app.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  
    ordering = ('name',) 
    search_fields = ('name', 'description')
    search_help_text = "Search by category name or description"

    fieldsets = (
        ('Category Details', {
            'fields': ('name', 'description')
        }),
    )

    actions = ["add_new_category"]

    @admin.action(description="Add new category")
    def add_new_category(self, request, queryset):
        Category.objects.create(name="New Category", description="Default description")
        self.message_user(request, "New category added")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'get_categories', 'is_available')
    ordering = ('name', 'price')  
    search_fields = ('name', 'description')
    search_help_text = "Search by product name or description"

    fieldsets = (
        ('Product Info', {
            'fields': ('name', 'description', 'categories', 'is_available') 
        }),
        ('Pricing', {
            'fields': ('price',),
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('created_at',)

    actions = ["add_new_product", "update_product_details", "set_price", "publish_products", "mark_out_of_stock"]

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])  
    get_categories.short_description = 'Категории'

    @admin.action(description="Add new product")
    def add_new_product(self, request, queryset):
        if Category.objects.exists():
            category = Category.objects.first()
        else:
            category = Category.objects.create(name="Default Category", description="Auto-created")
        
        Product.objects.create(
            name="New Product",
            description="Default description",
            price=0.0,
            is_available=True
        ).categories.add(category)  
        self.message_user(request, "New product added")

    @admin.action(description="Update product details")
    def update_product_details(self, request, queryset):
        updated_count = queryset.update(
            name="Updated Product",
            description="Updated description",
            price=99.99
        )
        self.message_user(request, f"{updated_count} product(s) updated")

    @admin.action(description="Set price to 500")
    def set_price(self, request, queryset):
        updated_count = queryset.update(price=500.00)
        self.message_user(request, f"Price updated for {updated_count} product(s)")

    @admin.action(description="Mark as out of stock")
    def mark_out_of_stock(self, request, queryset):
        updated_count = queryset.update(is_available=False)
        self.message_user(request, f"{updated_count} product(s) marked as out of stock")