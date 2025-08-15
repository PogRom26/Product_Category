import pytest
from src.class_config import Product, Category


# Фикстура для сброса счётчиков перед каждым тестом
@pytest.fixture(autouse=True)
def reset_counters():
    Product.product_count = 0
    Category.category_count = 0
    Category.product_count = 0
    yield


# Тест инициализации класса Product
def test_product_initialization(sample_product):
    # Проверяем атрибуты
    assert sample_product.name == "Sample Product"
    assert sample_product.description == "This is a sample product"
    assert sample_product.price == 99.99
    assert sample_product.quantity == 10

    # Проверяем типы атрибутов
    assert isinstance(sample_product.name, str)
    assert isinstance(sample_product.description, str)
    assert isinstance(sample_product.price, float)
    assert isinstance(sample_product.quantity, int)


# Тест инициализации нескольких продуктов
def test_product_multiple_initialization():
    product1 = Product(name="Product 1", description="Desc 1", price=19.99, quantity=5)
    product2 = Product(name="Product 2", description="Desc 2", price=29.99, quantity=3)

    # Проверяем атрибуты первого продукта
    assert product1.name == "Product 1"
    assert product1.description == "Desc 1"
    assert product1.price == 19.99
    assert product1.quantity == 5

    # Проверяем атрибуты второго продукта
    assert product2.name == "Product 2"
    assert product2.description == "Desc 2"
    assert product2.price == 29.99
    assert product2.quantity == 3


# Тест инициализации класса Category
def test_category_initialization(sample_category, product_list):
    # Проверяем атрибуты
    assert sample_category.name == "Sample Category"
    assert sample_category.description == "This is a sample category"
    assert sample_category.products == product_list
    assert len(sample_category.products) == 3

    # Проверяем типы атрибутов
    assert isinstance(sample_category.name, str)
    assert isinstance(sample_category.description, str)
    assert isinstance(sample_category.products, list)
    assert all(isinstance(product, Product) for product in sample_category.products)


# Тест инициализации пустой категории
def test_empty_category_initialization(empty_category):
    # Проверяем атрибуты
    assert empty_category.name == "Empty Category"
    assert empty_category.description == "This is an empty category"
    assert empty_category.products == []

    # Проверяем типы атрибутов
    assert isinstance(empty_category.name, str)
    assert isinstance(empty_category.description, str)
    assert isinstance(empty_category.products, list)

    # Проверяем счётчики
    assert Category.category_count == 1
    assert Category.product_count == 0


# Тест инициализации нескольких категорий
def test_multiple_category_initialization(product_list):
    category1 = Category(name="Category 1", description="Desc 1", products=product_list)
    category2 = Category(name="Category 2", description="Desc 2", products=[])

    # Проверяем атрибуты первой категории
    assert category1.name == "Category 1"
    assert category1.description == "Desc 1"
    assert category1.products == product_list
    assert len(category1.products) == 3

    # Проверяем атрибуты второй категории
    assert category2.name == "Category 2"
    assert category2.description == "Desc 2"
    assert category2.products == []

    # Проверяем счётчики
    assert Category.category_count == 2
    assert Category.product_count == 3  # Только category1 содержит продукты
