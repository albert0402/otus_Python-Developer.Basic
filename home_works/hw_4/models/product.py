from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import Optional

class Product(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Название продукта")
    price: float = Field(..., gt=0, description="Цена продукта, должна быть больше 0")
    description: Optional[str] = Field(None, max_length=500, description="Описание продукта (опционально)")
    image_url: HttpUrl = Field(..., description="URL изображения продукта")
    stock: int = Field(..., ge=0, description="Количество товара на складе")
    category: str = Field(..., min_length=3, max_length=50, description="Категория продукта")

    @field_validator('price')
    def validate_price(cls, value):
        if value < 10.0:
            raise ValueError("Цена должна быть не меньше 10.0")
        return round(value, 2)

    @field_validator('name')
    def validate_name(cls, value):
        if not value.isalnum():
            raise ValueError("Название должно содержать только буквы и цифры")
        return value.title()

    @field_validator('category')
    def validate_category(cls, value):
        if not value.isalpha():
            raise ValueError("Категория должна содержать только буквы")
        return value.capitalize()