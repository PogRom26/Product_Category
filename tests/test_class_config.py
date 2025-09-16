import pytest
from src.class_config import Product, Category


# Tests for Product class
def test_product_initialization():
    """Test Product class initialization with valid data"""
    product = Product("Laptop", "High-end gaming laptop", 1000.0, 10)
    assert product.name == "Laptop"
    assert product.description == "High-end gaming laptop"
    assert product.price == 1000.0
    assert product.quantity == 10
    assert Product.product_count > 0


def test_product_negative_price():
    """Test Product initialization with negative price"""
    product = Product("Phone", "Smartphone", -500.0, 5)
    assert product.price == 0  # Should set to 0 for negative price


def test_product_price_setter_valid():
    """Test Product price setter with valid price"""
    product = Product("Tablet", "10-inch tablet", 300.0, 8)
    product.price = 400.0
    assert product.price == 400.0


def test_new_product_valid():
    """Test classmethod new_product with valid dictionary"""
    product_data = {"name": "Mouse", "description": "Wireless mouse", "price": 50.0, "quantity": 20}
    product = Product.new_product(product_data)
    assert isinstance(product, Product)
    assert product.name == "Mouse"
    assert product.description == "Wireless mouse"
    assert product.price == 50.0
    assert product.quantity == 20


def test_new_product_invalid_dict():
    """Test classmethod new_product with invalid dictionary"""
    product_data = {"name": "Keyboard", "price": 75.0}
    with pytest.raises(ValueError, match="В словаре должны быть ключи: name, description, price, quantity"):
        Product.new_product(product_data)


def test_new_product_not_dict():
    """Test classmethod new_product with non-dictionary input"""
    with pytest.raises(ValueError, match="Параметры товара должны быть переданы в виде словаря"):
        Product.new_product(["invalid", "data"])


# Tests for Category class
def test_category_initialization():
    """Test Category class initialization"""
    category = Category("Electronics", "Electronic devices", [])
    assert category.name == "Electronics"
    assert category.description == "Electronic devices"
    assert category.products == "Список товаров пуст"
    assert Category.category_count > 0


def test_category_add_product():
    """Test adding a valid Product to Category"""
    category = Category("Gadgets", "Cool gadgets", [])
    product = Product("Smartwatch", "Fitness tracker", 200.0, 15)
    category.add_product(product)
    assert Category.product_count > 0
    assert product.name in category.products
    assert "200.0 руб. Остаток: 15 шт." in category.products


def test_category_add_invalid_product():
    """Test adding invalid product to Category"""
    category = Category("Gadgets", "Cool gadgets", [])
    with pytest.raises(ValueError, match="Добавляемый объект должен быть экземпляром класса Product"):
        category.add_product("Not a product")


def test_category_products_format():
    """Test products property formatting"""
    category = Category("Appliances", "Home appliances", [])
    product1 = Product("Fridge", "Large refrigerator", 1000.0, 5)
    product2 = Product("Microwave", "Compact microwave", 150.0, 10)
    category.add_product(product1)
    category.add_product(product2)
    expected = "Fridge, 1000.0 руб. Остаток: 5 шт.\nMicrowave, 150.0 руб. Остаток: 10 шт."
    assert category.products == expected


def test_category_empty_products():
    """Test products property for empty category"""
    category = Category("Empty", "No products", [])
    assert category.products == "Список товаров пуст"
