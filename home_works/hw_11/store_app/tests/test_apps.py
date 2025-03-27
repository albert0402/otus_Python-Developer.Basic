import pytest
from django.apps import apps
from store_app.apps import StoreAppConfig

@pytest.mark.django_db
def test_app_config():
    """Проверка конфигурации приложения"""
    app_config = apps.get_app_config("store_app")
    assert isinstance(app_config, StoreAppConfig)
    assert app_config.name == "store_app"