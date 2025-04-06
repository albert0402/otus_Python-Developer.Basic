from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from store_app.models import Category, Product, User, Order, OrderItem
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

admin.site.unregister(Group)  # Опционально

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'phone', 'address', 'user_type')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type', 'is_staff', 'is_active'),
        }),
    )
    
    ordering = ('username',)


# Кастомная админка для модели OrderItem (inline для Order)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'total_price')
    
    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = _('Total Price')


# Кастомная админка для модели Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'total_price')
    inlines = [OrderItemInline]
    
    fieldsets = (
        (None, {'fields': ('user', 'status')}),
        (_('Order info'), {'fields': ('total_price', 'comment')}),
        (_('Dates'), {'fields': ('created_at', 'updated_at')}),
    )


# Существующая админка для Category (с небольшими улучшениями)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "product_count")
    ordering = ("name",)
    search_fields = ("name", "description")
    search_help_text = _("Search by category name or description")

    fieldsets = (
        (_("Category Details"), {"fields": ("name", "description", "image")}),
    )

    actions = ["add_new_category"]

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = _('Product Count')

    @admin.action(description=_("Add new category"))
    def add_new_category(self, request, queryset):
        Category.objects.create(name="New Category", description="Default description")
        self.message_user(request, _("New category added"))


# Существующая админка для Product (с небольшими улучшениями)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "get_categories", "is_available", "created_at")
    ordering = ("name", "price")
    search_fields = ("name", "description")
    search_help_text = _("Search by product name or description")
    list_filter = ("is_available", "categories")

    fieldsets = (
        (
            _("Product Info"),
            {"fields": ("name", "description", "categories", "is_available", "image")},
        ),
        (
            _("Pricing"),
            {"fields": ("price",)},
        ),
        (
            _("Metadata"),
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = ("created_at",)

    actions = [
        "add_new_product",
        "update_product_details",
        "set_price",
        "publish_products",
        "mark_out_of_stock",
    ]

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = _("Categories")

    @admin.action(description=_("Add new product"))
    def add_new_product(self, request, queryset):
        if Category.objects.exists():
            category = Category.objects.first()
        else:
            category = Category.objects.create(
                name=_("Default Category"), 
                description=_("Auto-created")
            )

        Product.objects.create(
            name=_("New Product"),
            description=_("Default description"),
            price=0.0,
            is_available=True,
        ).categories.add(category)
        self.message_user(request, _("New product added"))

    @admin.action(description=_("Update product details"))
    def update_product_details(self, request, queryset):
        updated_count = queryset.update(
            name=_("Updated Product"), 
            description=_("Updated description"), 
            price=99.99
        )
        self.message_user(request, _("%(count)d product(s) updated") % {'count': updated_count})

    @admin.action(description=_("Set price to 500"))
    def set_price(self, request, queryset):
        updated_count = queryset.update(price=500.00)
        self.message_user(request, _("Price updated for %(count)d product(s)") % {'count': updated_count})

    @admin.action(description=_("Mark as out of stock"))
    def mark_out_of_stock(self, request, queryset):
        updated_count = queryset.update(is_available=False)
        self.message_user(request, _("%(count)d product(s) marked as out of stock") % {'count': updated_count})


# Админка для OrderItem (если нужен отдельный доступ)
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price', 'total_price')
    list_filter = ('order__status',)
    search_fields = ('product__name', 'order__user__username')
    
    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = _('Total Price')