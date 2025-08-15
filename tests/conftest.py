import pytest
from src.class_config import Product, Category


# Фикстура для одного продукта
@pytest.fixture
def sample_product():
    return Product(
        name="Sample Product",
        description="This is a sample product",
        price=99.99,
        quantity=10,
    )


# Фикстура для списка продуктов
@pytest.fixture
def product_list():
    return [
        Product(name="Product 1", description="Description 1", price=19.99, quantity=5),
        Product(name="Product 2", description="Description 2", price=29.99, quantity=3),
        Product(name="Product 3", description="Description 3", price=39.99, quantity=7),
    ]


# Фикстура для категории с продуктами
@pytest.fixture
def sample_category(product_list):
    return Category(
        name="Sample Category",
        description="This is a sample category",
        products=product_list,
    )


# Фикстура для пустой категории
@pytest.fixture
def empty_category():
    return Category(name="Empty Category", description="This is an empty category", products=[])
