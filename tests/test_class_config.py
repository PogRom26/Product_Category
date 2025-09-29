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


class TestProductStr:
    """Тесты для строкового представления Product"""

    def test_str_representation_basic(self):
        """Тест базового строкового представления"""
        product = Product("Телефон", "Смартфон", 50000.0, 10)
        expected = "Телефон, 50000.0 руб. Остаток: 10 шт."
        assert str(product) == expected

    def test_str_representation_zero_quantity(self):
        """Тест с нулевым количеством"""
        product = Product("Ноутбук", "Игровой ноутбук", 100000.0, 0)
        expected = "Ноутбук, 100000.0 руб. Остаток: 0 шт."
        assert str(product) == expected

    def test_str_representation_large_quantity(self):
        """Тест с большим количеством"""
        product = Product("Книга", "Программирование на Python", 1500.0, 1000)
        expected = "Книга, 1500.0 руб. Остаток: 1000 шт."
        assert str(product) == expected

    def test_str_representation_decimal_price(self):
        """Тест с дробной ценой"""
        product = Product("Кофе", "Арабика", 350.50, 25)
        expected = "Кофе, 350.5 руб. Остаток: 25 шт."
        assert str(product) == expected

    def test_str_representation_special_characters(self):
        """Тест со специальными символами в названии"""
        product = Product("iPhone 15 Pro Max", "Флагманский смартфон", 120000.0, 5)
        expected = "iPhone 15 Pro Max, 120000.0 руб. Остаток: 5 шт."
        assert str(product) == expected

    def test_str_representation_russian_chars(self):
        """Тест с русскими символами"""
        product = Product("Хлеб", "Ржаной хлеб", 50.0, 100)
        expected = "Хлеб, 50.0 руб. Остаток: 100 шт."
        assert str(product) == expected

    def test_str_implicit_conversion(self):
        """Тест неявного преобразования в строку"""
        product = Product("Мышь", "Компьютерная мышь", 1500.0, 30)

        # Проверка через print (capture output)
        import io
        import sys

        captured_output = io.StringIO()
        sys.stdout = captured_output
        print(product)
        sys.stdout = sys.__stdout__

        assert captured_output.getvalue().strip() == "Мышь, 1500.0 руб. Остаток: 30 шт."

    def test_str_in_f_string(self):
        """Тест использования в f-строке"""
        product = Product("Клавиатура", "Механическая клавиатура", 5000.0, 15)
        result = f"Товар: {product}"
        expected = "Товар: Клавиатура, 5000.0 руб. Остаток: 15 шт."
        assert result == expected

    def test_str_with_class_method(self):
        """Тест строкового представления для продукта созданного через classmethod"""
        product_data = {
            "name": "Монитор",
            "description": "Игровой монитор",
            "price": 25000.0,
            "quantity": 8
        }
        product = Product.new_product(product_data)
        expected = "Монитор, 25000.0 руб. Остаток: 8 шт."
        assert str(product) == expected

    def test_str_format_consistency(self):
        """Тест согласованности формата"""
        product = Product("Test", "Test Description", 123.45, 67)
        result = str(product)

        # Проверяем структуру строки
        assert product.name in result
        assert f"{product.price} руб." in result
        assert f"Остаток: {product.quantity} шт." in result
        assert ", " in result  # разделитель между названием и ценой



class TestProductAddition:
    """Тесты для метода сложения продуктов"""

    def test_add_two_products_positive_quantities(self):
        """Тест сложения двух продуктов с положительными количествами"""
        # Arrange
        product1 = Product("Телефон", "Смартфон", 100, 10)
        product2 = Product("Ноутбук", "Игровой ноутбук", 200, 2)

        # Act
        result = product1 + product2

        # Assert
        expected = (100 * 10) + (200 * 2)  # 1000 + 400 = 1400
        assert result == expected

    def test_add_two_products_with_zero_quantity(self):
        """Тест сложения продуктов, когда у одного количество равно 0"""
        # Arrange
        product1 = Product("Книга", "Художественная литература", 500, 0)
        product2 = Product("Ручка", "Шариковая ручка", 50, 5)

        # Act
        result = product1 + product2

        # Assert
        expected = (500 * 0) + (50 * 5)  # 0 + 250 = 250
        assert result == expected

    def test_add_two_products_both_zero_quantity(self):
        """Тест сложения продуктов, когда у обоих количество равно 0"""
        # Arrange
        product1 = Product("Товар1", "Описание1", 100, 0)
        product2 = Product("Товар2", "Описание2", 200, 0)

        # Act
        result = product1 + product2

        # Assert
        assert result == 0

    def test_add_products_commutative_property(self):
        """Тест коммутативности сложения (a + b = b + a)"""
        # Arrange
        product_a = Product("Товар A", "Описание A", 150, 3)
        product_b = Product("Товар B", "Описание B", 75, 8)

        # Act
        result1 = product_a + product_b
        result2 = product_b + product_a

        # Assert
        assert result1 == result2

    def test_add_product_with_high_price_low_quantity(self):
        """Тест сложения продукта с высокой ценой и низким количеством"""
        # Arrange
        expensive_product = Product("Золото", "Инвестиционное золото", 5000, 1)
        cheap_product = Product("Хлеб", "Белый хлеб", 50, 10)

        # Act
        result = expensive_product + cheap_product

        # Assert
        expected = (5000 * 1) + (50 * 10)  # 5000 + 500 = 5500
        assert result == expected

    def test_add_product_with_negative_price_handling(self):
        """Тест сложения продуктов, где цена была установлена через сеттер с проверкой"""
        # Arrange
        product1 = Product("Товар1", "Описание1", 100, 5)
        product2 = Product("Товар2", "Описание2", -50, 10)  # Отрицательная цена будет установлена в 0

        # Act
        result = product1 + product2

        # Assert - product2 цена будет 0 из-за проверки в __init__
        expected = (100 * 5) + (0 * 10)  # 500 + 0 = 500
        assert result == expected

    def test_add_product_type_error(self):
        """Тест выброса TypeError при попытке сложить с объектом другого типа"""
        # Arrange
        product = Product("Телефон", "Смартфон", 100, 10)
        invalid_object = "не продукт"

        # Act & Assert
        with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
            product + invalid_object

    def test_add_product_with_itself(self):
        """Тест сложения продукта с самим собой"""
        # Arrange
        product = Product("Уникальный товар", "Единственный в своем роде", 300, 4)

        # Act
        result = product + product

        # Assert
        expected = (300 * 4) * 2  # Удвоенная стоимость
        assert result == expected

    def test_add_products_decimal_prices(self):
        """Тест сложения продуктов с десятичными ценами"""
        # Arrange
        product1 = Product("Товар1", "Описание1", 99.99, 2)
        product2 = Product("Товар2", "Описание2", 49.50, 3)

        # Act
        result = product1 + product2

        # Assert
        expected = (99.99 * 2) + (49.50 * 3)
        assert result == expected

    def test_add_products_large_quantities(self):
        """Тест сложения продуктов с большими количествами"""
        # Arrange
        product1 = Product("Мелкий товар", "Массовый товар", 1, 1000)
        product2 = Product("Средний товар", "Товар средней цены", 100, 50)

        # Act
        result = product1 + product2

        # Assert
        expected = (1 * 1000) + (100 * 50)  # 1000 + 5000 = 6000
        assert result == expected