# store_app/apps.py
from django.apps import AppConfig

class StoreAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store_app'
    verbose_name = 'Store Application'