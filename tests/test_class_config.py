from abc import ABC

import pytest

from src.class_config import (BaseProduct, Category, LawnGrass, Product,
                              ReprMixin, Smartphone)


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
        product_data = {"name": "Монитор", "description": "Игровой монитор", "price": 25000.0, "quantity": 8}
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

    def test_add_same_base_products(self):
        """Тест сложения двух одинаковых базовых продуктов"""
        product1 = Product("Товар1", "Описание1", 100.0, 2)
        product2 = Product("Товар2", "Описание2", 50.0, 3)
        result = product1 + product2
        expected = (100.0 * 2) + (50.0 * 3)  # 200 + 150 = 350
        assert result == expected

    def test_add_same_smartphones(self):
        """Тест сложения двух смартфонов одного класса"""
        phone1 = Smartphone("Phone1", "Desc1", 500.0, 2, "A15", "Model1", 64, "Black")
        phone2 = Smartphone("Phone2", "Desc2", 300.0, 4, "A16", "Model2", 128, "White")
        result = phone1 + phone2
        expected = (500.0 * 2) + (300.0 * 4)  # 1000 + 1200 = 2200
        assert result == expected

    def test_add_same_lawn_grass(self):
        """Тест сложения двух газонных трав одного класса"""
        grass1 = LawnGrass("Grass1", "Desc1", 20.0, 10, "RU", "10 дней", "Green")
        grass2 = LawnGrass("Grass2", "Desc2", 30.0, 5, "DE", "14 дней", "Dark Green")
        result = grass1 + grass2
        expected = (20.0 * 10) + (30.0 * 5)  # 200 + 150 = 350
        assert result == expected

    def test_add_smartphone_with_base_product(self):
        """Тест сложения смартфона с базовым продуктом (должна быть ошибка)"""
        phone = Smartphone("Phone", "Desc", 500.0, 2, "A15", "Model", 64, "Black")
        base_product = Product("Base", "Desc", 100.0, 5)

        with pytest.raises(TypeError, match="Нельзя складывать товары из разных классов продуктов"):
            phone + base_product


    def test_add_lawn_grass_with_smartphone(self):
        """Тест сложения газонной травы со смартфоном (должна быть ошибка)"""
        grass = LawnGrass("Grass", "Desc", 20.0, 10, "RU", "10 дней", "Green")
        phone = Smartphone("Phone", "Desc", 500.0, 2, "A15", "Model", 64, "Black")

        with pytest.raises(TypeError, match="Нельзя складывать товары из разных классов продуктов"):
            grass + phone

    def test_add_smartphone_with_lawn_grass(self):
        """Тест сложения смартфона с газонной травой (должна быть ошибка)"""
        phone = Smartphone("Phone", "Desc", 500.0, 2, "A15", "Model", 64, "Black")
        grass = LawnGrass("Grass", "Desc", 20.0, 10, "RU", "10 дней", "Green")

        with pytest.raises(TypeError, match="Нельзя складывать товары из разных классов продуктов"):
            phone + grass

    def test_add_lawn_grass_with_base_product(self):
        """Тест сложения газонной травы с базовым продуктом (должна быть ошибка)"""
        grass = LawnGrass("Grass", "Desc", 20.0, 10, "RU", "10 дней", "Green")
        base_product = Product("Base", "Desc", 100.0, 5)

        with pytest.raises(TypeError, match="Нельзя складывать товары из разных классов продуктов"):
            grass + base_product


    def test_add_product_with_string(self):
        """Тест сложения продукта со строкой (должна быть ошибка)"""
        product = Product("Товар", "Описание", 100.0, 5)

        with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
            product + "не продукт"

    def test_add_product_with_number(self):
        """Тест сложения продукта с числом (должна быть ошибка)"""
        product = Product("Товар", "Описание", 100.0, 5)

        with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
            product + 123

    def test_add_product_with_list(self):
        """Тест сложения продукта со списком (должна быть ошибка)"""
        product = Product("Товар", "Описание", 100.0, 5)

        with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
            product + [1, 2, 3]

    def test_add_product_with_none(self):
        """Тест сложения продукта с None (должна быть ошибка)"""
        product = Product("Товар", "Описание", 100.0, 5)

        with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
            product + None

    def test_add_product_with_dict(self):
        """Тест сложения продукта со словарем (должна быть ошибка)"""
        product = Product("Товар", "Описание", 100.0, 5)

        with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
            product + {"name": "test"}

    def test_commutative_property_same_products(self):
        """Тест коммутативного свойства для одинаковых продуктов"""
        product1 = Product("Товар1", "Описание", 100.0, 3)
        product2 = Product("Товар2", "Описание", 200.0, 2)

        result1 = product1 + product2
        result2 = product2 + product1

        assert result1 == result2
        assert result1 == (100.0 * 3) + (200.0 * 2)  # 300 + 400 = 700


    def test_mixed_quantities(self):
        """Тест сложения продуктов с разными количествами"""
        product1 = Product("Товар1", "Описание", 10.0, 100)
        product2 = Product("Товар2", "Описание", 5.0, 200)
        result = product1 + product2
        expected = (10.0 * 100) + (5.0 * 200)  # 1000 + 1000 = 2000
        assert result == expected

    def test_high_price_products(self):
        """Тест сложения продуктов с высокой ценой"""
        product1 = Product("Дорогой1", "Описание", 10000.0, 2)
        product2 = Product("Дорогой2", "Описание", 5000.0, 4)
        result = product1 + product2
        expected = (10000.0 * 2) + (5000.0 * 4)  # 20000 + 20000 = 40000
        assert result == expected


class TestSmartphone:
    """Тесты для класса Smartphone"""

    def test_smartphone_creation(self):
        """Тест создания смартфона со всеми параметрами"""
        smartphone = Smartphone(
            "iPhone 15 Pro", "Флагманский смартфон", 99999.0, 5, "A17 Pro", "iPhone 15 Pro", 256, "Титановый синий"
        )

        assert smartphone.name == "iPhone 15 Pro"
        assert smartphone.description == "Флагманский смартфон"
        assert smartphone.price == 99999.0
        assert smartphone.quantity == 5
        assert smartphone.efficiency == "A17 Pro"
        assert smartphone.model == "iPhone 15 Pro"
        assert smartphone.memory == 256
        assert smartphone.color == "Титановый синий"

    def test_smartphone_inheritance(self):
        """Тест, что Smartphone наследуется от Product"""
        smartphone = Smartphone("Test Phone", "Desc", 100.0, 1, "A15", "Model", 128, "Black")

        assert isinstance(smartphone, Product)
        assert hasattr(smartphone, "name")
        assert hasattr(smartphone, "price")
        assert hasattr(smartphone, "quantity")

    def test_smartphone_str_representation(self):
        """Тест строкового представления смартфона"""
        smartphone = Smartphone(
            "Samsung Galaxy S24", "Android флагман", 79999.0, 8, "Snapdragon 8 Gen 3", "Galaxy S24", 512, "Черный"
        )

        str_repr = str(smartphone)

        # Проверяем базовую информацию из родительского класса
        assert "Samsung Galaxy S24" in str_repr
        assert "79999.0" in str_repr
        assert "8" in str_repr  # количество

        # Проверяем специфическую информацию для смартфона
        assert "Модель: Galaxy S24" in str_repr
        assert "Производительность: Snapdragon 8 Gen 3" in str_repr
        assert "Память: 512 ГБ" in str_repr
        assert "Цвет: Черный" in str_repr

    def test_smartphone_with_zero_quantity(self):
        """Тест создания смартфона с нулевым количеством"""
        smartphone = Smartphone("Xiaomi", "Бюджетный", 20000.0, 0, "Snapdragon", "Redmi", 64, "Blue")

        assert smartphone.quantity == 0
        assert "Остаток: 0 шт." in str(smartphone)

    def test_smartphone_with_negative_price(self):
        """Тест создания смартфона с отрицательной ценой (должна установиться 0)"""
        smartphone = Smartphone("Test Phone", "Desc", -100.0, 5, "A15", "Model", 128, "Black")

        assert smartphone.price == 0

    def test_smartphone_price_property(self):
        """Тест работы property для цены смартфона"""
        smartphone = Smartphone("Test Phone", "Desc", 50000.0, 2, "A15", "Model", 128, "Black")

        # Тест геттера
        assert smartphone.price == 50000.0

        # Тест сеттера с положительным значением
        smartphone.price = 45000.0
        assert smartphone.price == 45000.0

        # Тест сеттера с отрицательным значением (цена не должна измениться)
        smartphone.price = -100.0
        assert smartphone.price == 45000.0

    def test_smartphone_addition_same_type(self):
        """Тест сложения двух смартфонов"""
        phone1 = Smartphone("Phone1", "Desc", 50000.0, 3, "A15", "M1", 128, "Black")
        phone2 = Smartphone("Phone2", "Desc", 30000.0, 2, "A16", "M2", 256, "White")

        result = phone1 + phone2
        expected = (50000.0 * 3) + (30000.0 * 2)  # 150000 + 60000 = 210000
        assert result == expected

    def test_smartphone_addition_different_type(self):
        """Тест попытки сложения смартфона с другим типом продукта"""
        phone = Smartphone("Phone", "Desc", 50000.0, 3, "A15", "M1", 128, "Black")
        grass = LawnGrass("Grass", "Desc", 1000.0, 10, "RU", "10 дней", "Green")

        with pytest.raises(TypeError, match="Нельзя складывать товары из разных классов продуктов"):
            phone + grass


class TestLawnGrass:
    """Тесты для класса LawnGrass"""

    def test_lawn_grass_creation(self):
        """Тест создания газонной травы со всеми параметрами"""
        lawn_grass = LawnGrass(
            "Газонная трава Премиум",
            "Высококачественная газонная трава",
            1500.0,
            100,
            "Германия",
            "14 дней",
            "Ярко-зеленый",
        )

        assert lawn_grass.name == "Газонная трава Премиум"
        assert lawn_grass.description == "Высококачественная газонная трава"
        assert lawn_grass.price == 1500.0
        assert lawn_grass.quantity == 100
        assert lawn_grass.country == "Германия"
        assert lawn_grass.germination_period == "14 дней"
        assert lawn_grass.color == "Ярко-зеленый"

    def test_lawn_grass_inheritance(self):
        """Тест, что LawnGrass наследуется от Product"""
        lawn_grass = LawnGrass("Test Grass", "Desc", 50.0, 10, "RU", "10 дней", "Green")

        assert isinstance(lawn_grass, Product)
        assert hasattr(lawn_grass, "name")
        assert hasattr(lawn_grass, "price")
        assert hasattr(lawn_grass, "quantity")

    def test_lawn_grass_str_representation(self):
        """Тест строкового представления газонной травы"""
        lawn_grass = LawnGrass(
            "Трава для гольф полей",
            "Высококачественная трава для спортивных площадок",
            2500.0,
            50,
            "США",
            "21 день",
            "Темно-зеленый",
        )

        str_repr = str(lawn_grass)

        # Проверяем базовую информацию из родительского класса
        assert "Трава для гольф полей" in str_repr
        assert "2500.0" in str_repr
        assert "50" in str_repr  # количество

        # Проверяем специфическую информацию для газонной травы
        assert "Страна: США" in str_repr
        assert "Срок прорастания: 21 день" in str_repr
        assert "Цвет: Темно-зеленый" in str_repr

    def test_lawn_grass_with_large_quantity(self):
        """Тест создания газонной травы с большим количеством"""
        lawn_grass = LawnGrass("Оптовая трава", "Desc", 500.0, 1000, "RU", "7 дней", "Green")

        assert lawn_grass.quantity == 1000
        assert "Остаток: 1000 шт." in str(lawn_grass)

    def test_lawn_grass_with_low_price(self):
        """Тест создания газонной травы с низкой ценой"""
        lawn_grass = LawnGrass("Бюджетная трава", "Desc", 10.0, 200, "RU", "20 дней", "Light Green")

        assert lawn_grass.price == 10.0

    def test_lawn_grass_price_property(self):
        """Тест работы property для цены газонной травы"""
        lawn_grass = LawnGrass("Test Grass", "Desc", 100.0, 50, "RU", "10 дней", "Green")

        # Тест геттера
        assert lawn_grass.price == 100.0

        # Тест сеттера с положительным значением
        lawn_grass.price = 120.0
        assert lawn_grass.price == 120.0

        # Тест сеттера с нулевым значением (цена не должна измениться)
        lawn_grass.price = 0
        assert lawn_grass.price == 120.0

    def test_lawn_grass_addition_same_type(self):
        """Тест сложения двух газонных трав"""
        grass1 = LawnGrass("Grass1", "Desc", 20.0, 100, "RU", "10 дней", "Green")
        grass2 = LawnGrass("Grass2", "Desc", 30.0, 50, "DE", "14 дней", "Dark Green")

        result = grass1 + grass2
        expected = (20.0 * 100) + (30.0 * 50)  # 2000 + 1500 = 3500
        assert result == expected

    def test_lawn_grass_addition_different_type(self):
        """Тест попытки сложения газонной травы с другим типом продукта"""
        grass = LawnGrass("Grass", "Desc", 20.0, 100, "RU", "10 дней", "Green")
        phone = Smartphone("Phone", "Desc", 50000.0, 3, "A15", "M1", 128, "Black")

        with pytest.raises(TypeError, match="Нельзя складывать товары из разных классов продуктов"):
            grass + phone


class TestSmartphoneAndLawnGrassIntegration:
    """Интеграционные тесты для Smartphone и LawnGrass"""

    def test_both_classes_have_color_attribute(self):
        """Тест, что оба класса имеют атрибут color"""
        smartphone = Smartphone("Phone", "Desc", 100.0, 1, "A15", "M1", 128, "Black")
        lawn_grass = LawnGrass("Grass", "Desc", 10.0, 1, "RU", "10 дней", "Green")

        assert hasattr(smartphone, "color")
        assert hasattr(lawn_grass, "color")
        assert smartphone.color == "Black"
        assert lawn_grass.color == "Green"

    def test_different_class_types(self):
        """Тест, что классы имеют разные типы"""
        smartphone = Smartphone("Phone", "Desc", 100.0, 1, "A15", "M1", 128, "Black")
        lawn_grass = LawnGrass("Grass", "Desc", 10.0, 1, "RU", "10 дней", "Green")

        assert type(smartphone) == Smartphone
        assert type(lawn_grass) == LawnGrass
        assert type(smartphone) != type(lawn_grass)

    def test_both_inherit_from_product(self):
        """Тест, что оба класса наследуются от Product"""
        smartphone = Smartphone("Phone", "Desc", 100.0, 1, "A15", "M1", 128, "Black")
        lawn_grass = LawnGrass("Grass", "Desc", 10.0, 1, "RU", "10 дней", "Green")

        assert isinstance(smartphone, Product)
        assert isinstance(lawn_grass, Product)

    def test_class_method_new_product_inheritance(self):
        """Тест работы классового метода new_product для наследников"""
        smartphone_data = {"name": "New Smartphone", "description": "Latest model", "price": 80000.0, "quantity": 5}

        # Этот тест может потребовать адаптации, так как new_product не принимает
        # специфические параметры наследников
        with pytest.raises(TypeError):
            # Будет ошибка, так как не хватает специфических параметров
            smartphone = Smartphone.new_product(smartphone_data)


class TestCategoryAddProduct:
    """Тесты для метода add_product класса Category"""

    def test_add_base_product(self):
        """Тест добавления базового продукта"""
        category = Category("Электроника", "Техника")
        product = Product("Телефон", "Смартфон", 10000.0, 5)

        category.add_product(product)

        # Проверяем, что продукт добавлен
        assert len(category.products.split("\n")) == 1
        assert "Телефон" in category.products
        assert "10000.0" in category.products

    def test_add_smartphone(self):
        """Тест добавления смартфона (наследник Product)"""
        category = Category("Смартфоны", "Мобильные устройства")
        smartphone = Smartphone("iPhone 15", "Флагман", 99999.0, 3, "A17 Pro", "15 Pro", 256, "Black")

        category.add_product(smartphone)

        # Проверяем, что смартфон добавлен
        products_list = category.products.split("\n")
        assert len(products_list) == 1
        assert "iPhone 15" in category.products
        assert "99999.0" in category.products

    def test_add_lawn_grass(self):
        """Тест добавления газонной травы (наследник Product)"""
        category = Category("Садоводство", "Товары для сада")
        lawn_grass = LawnGrass("Премиум трава", "Качественная", 1500.0, 100, "Германия", "14 дней", "Зеленый")

        category.add_product(lawn_grass)

        # Проверяем, что газонная трава добавлена
        products_list = category.products.split("\n")
        assert len(products_list) == 1
        assert "Премиум трава" in category.products
        assert "1500.0" in category.products

    def test_add_multiple_products(self):
        """Тест добавления нескольких продуктов разных типов"""
        category = Category("Разные товары", "Разнообразная продукция")

        product1 = Product("Базовый товар", "Описание", 500.0, 10)
        product2 = Smartphone("Смартфон", "Мобильный", 30000.0, 2, "A15", "M1", 128, "White")
        product3 = LawnGrass("Трава", "Для газона", 800.0, 50, "Россия", "10 дней", "Green")

        category.add_product(product1)
        category.add_product(product2)
        category.add_product(product3)

        # Проверяем, что все три продукта добавлены
        products_list = category.products.split("\n")
        assert len(products_list) == 3
        assert "Базовый товар" in category.products
        assert "Смартфон" in category.products
        assert "Трава" in category.products

    def test_add_product_updates_count(self):
        """Тест, что добавление продукта увеличивает счетчик"""
        initial_count = Category.product_count
        category = Category("Тестовая категория", "Описание")
        product = Product("Тестовый товар", "Описание", 100.0, 1)

        category.add_product(product)

        # Проверяем, что счетчик увеличился на 1
        assert Category.product_count == initial_count + 1

    def test_add_string_raises_error(self):
        """Тест, что добавление строки вызывает TypeError"""
        category = Category("Тест", "Описание")

        with pytest.raises(
            TypeError, match="Добавляемый объект должен быть экземпляром класса Product или его наследников"
        ):
            category.add_product("просто строка")

    def test_add_number_raises_error(self):
        """Тест, что добавление числа вызывает TypeError"""
        category = Category("Тест", "Описание")

        with pytest.raises(
            TypeError, match="Добавляемый объект должен быть экземпляром класса Product или его наследников"
        ):
            category.add_product(12345)

    def test_add_list_raises_error(self):
        """Тест, что добавление списка вызывает TypeError"""
        category = Category("Тест", "Описание")

        with pytest.raises(
            TypeError, match="Добавляемый объект должен быть экземпляром класса Product или его наследников"
        ):
            category.add_product(["товар1", "товар2"])

    def test_add_dict_raises_error(self):
        """Тест, что добавление словаря вызывает TypeError"""
        category = Category("Тест", "Описание")

        with pytest.raises(
            TypeError, match="Добавляемый объект должен быть экземпляром класса Product или его наследников"
        ):
            category.add_product({"name": "товар", "price": 100})

    def test_add_none_raises_error(self):
        """Тест, что добавление None вызывает TypeError"""
        category = Category("Тест", "Описание")

        with pytest.raises(
            TypeError, match="Добавляемый объект должен быть экземпляром класса Product или его наследников"
        ):
            category.add_product(None)

    def test_add_boolean_raises_error(self):
        """Тест, что добавление boolean вызывает TypeError"""
        category = Category("Тест", "Описание")

        with pytest.raises(
            TypeError, match="Добавляемый объект должен быть экземпляром класса Product или его наследников"
        ):
            category.add_product(True)

    def test_add_empty_category(self):
        """Тест добавления продукта в пустую категорию"""
        category = Category("Пустая категория", "Нет товаров")
        product = Product("Первый товар", "Описание", 100.0, 5)

        category.add_product(product)

        # Проверяем, что продукт добавлен и список не пустой
        assert category.products != "Список товаров пуст"
        assert "Первый товар" in category.products


    def test_product_order_preservation(self):
        """Тест сохранения порядка добавления продуктов"""
        category = Category("Тест", "Описание")

        products = [
            Product("Первый", "Описание", 100.0, 1),
            Product("Второй", "Описание", 200.0, 2),
            Product("Третий", "Описание", 300.0, 3),
        ]

        for product in products:
            category.add_product(product)

        # Проверяем порядок продуктов в строковом представлении
        products_str = category.products
        lines = products_str.split("\n")

        assert "Первый" in lines[0]
        assert "Второй" in lines[1]
        assert "Третий" in lines[2]

    def test_add_same_product_twice(self):
        """Тест добавления одного и того же продукта дважды"""
        category = Category("Тест", "Описание")
        product = Product("Один товар", "Описание", 100.0, 5)

        category.add_product(product)
        category.add_product(product)  # Добавляем второй раз

        # Проверяем, что продукт добавлен дважды
        products_list = category.products.split("\n")
        assert len(products_list) == 2
        # Оба элемента должны содержать название товара
        assert all("Один товар" in line for line in products_list)

    def test_mixed_valid_invalid_products(self):
        """Тест смешанного добавления валидных и невалидных объектов"""
        category = Category("Тест", "Описание")
        valid_product = Product("Валидный товар", "Описание", 100.0, 1)

        # Добавляем валидный продукт
        category.add_product(valid_product)

        # Пытаемся добавить невалидный объект
        with pytest.raises(TypeError):
            category.add_product("невалидный")

        # Проверяем, что валидный продукт остался в списке
        assert "Валидный товар" in category.products
        assert len(category.products.split("\n")) == 1

    def test_category_count_increases(self):
        """Тест, что счетчик категорий увеличивается при создании"""
        initial_category_count = Category.category_count
        initial_product_count = Category.product_count

        category = Category("Новая категория", "Описание")
        product1 = Product("Товар1", "Описание", 100.0, 2)
        product2 = Product("Товар2", "Описание", 200.0, 3)

        category.add_product(product1)
        category.add_product(product2)

        # Проверяем счетчики
        assert Category.category_count == initial_category_count + 1
        assert Category.product_count == initial_product_count + 2


class TestBaseProduct:
    """Тесты для абстрактного базового класса BaseProduct"""

    def test_base_product_is_abstract(self):
        """Тест, что BaseProduct является абстрактным классом"""
        assert issubclass(BaseProduct, ABC)

        # Попытка создать экземпляр абстрактного класса должна вызвать ошибку
        with pytest.raises(TypeError):
            BaseProduct("Test", "Description", 100, 10)


class TestReprMixin:
    """Тесты для миксина ReprMixin"""

    def test_repr_mixin_initialization_logging(self, capsys):
        """Тест логирования при создании объекта"""
        product = Product("Test Product", "Test Description", 1000, 5)
        captured = capsys.readouterr()

        assert "Product(" in captured.out
        assert "Test Product" in captured.out
        assert "Test Description" in captured.out
        assert "1000" in captured.out
        assert "5" in captured.out

    def test_repr_mixin_with_smartphone(self, capsys):
        """Тест логирования для класса Smartphone"""
        smartphone = Smartphone(
            "Test Phone", "Phone Description", 50000, 3,
            "High", "Model X", 128, "Black"
        )
        captured = capsys.readouterr()

        assert "Smartphone(" in captured.out
        assert "Test Phone" in captured.out
        assert "Phone Description" in captured.out
        assert "50000" in captured.out
        assert "3" in captured.out

    def test_repr_method(self):
        """Тест метода __repr__"""
        product = Product("Test Product", "Test Description", 1000, 5)
        repr_str = repr(product)

        assert "Product(" in repr_str
        assert "name=" in repr_str
        assert "description=" in repr_str
        assert "price=" in repr_str
        assert "quantity=" in repr_str


class TestProductInheritance:
    """Тесты наследования и MRO"""

    def test_product_inheritance_chain(self):
        """Тест цепочки наследования класса Product"""
        assert issubclass(Product, ReprMixin)
        assert issubclass(Product, BaseProduct)
        assert issubclass(Smartphone, Product)
        assert issubclass(LawnGrass, Product)

    def test_mro_order(self):
        """Тест порядка разрешения методов (MRO)"""
        mro = Product.__mro__
        assert mro[0] == Product
        assert ReprMixin in mro
        assert BaseProduct in mro

    def test_abstract_methods_implementation(self):
        """Тест, что все абстрактные методы реализованы"""
        # Создание объектов должно работать без ошибок
        product = Product("Test", "Desc", 100, 10)
        smartphone = Smartphone("Phone", "Desc", 200, 5, "High", "X", 64, "Black")
        grass = LawnGrass("Grass", "Desc", 50, 100, "RU", "14 days", "Green")

        # Проверка, что методы работают
        assert str(product) is not None
        assert isinstance(product.price, (int, float))

        # Проверка сложения продуктов
        total = product + product
        assert isinstance(total, (int, float))


class TestProductFunctionality:
    """Тесты основной функциональности Product"""

    def test_product_creation(self):
        """Тест создания продукта"""
        product = Product("Laptop", "Gaming laptop", 50000, 10)

        assert product.name == "Laptop"
        assert product.description == "Gaming laptop"
        assert product.price == 50000
        assert product.quantity == 10

    def test_product_str_method(self):
        """Тест строкового представления продукта"""
        product = Product("Laptop", "Gaming laptop", 50000, 10)
        expected = "Laptop, 50000 руб. Остаток: 10 шт."
        assert str(product) == expected

    def test_product_addition(self):
        """Тест сложения продуктов"""
        product1 = Product("Product1", "Desc1", 100, 5)  # 100 * 5 = 500
        product2 = Product("Product2", "Desc2", 200, 3)  # 200 * 3 = 600

        total = product1 + product2
        assert total == 1100  # 500 + 600


    def test_product_price_validation(self):
        """Тест валидации цены"""
        product = Product("Product", "Desc", 100, 5)

        # Установка корректной цены
        product.price = 150
        assert product.price == 150

        # Установка некорректной цены (должна остаться предыдущее значение)
        product.price = -10
        assert product.price == 150

    def test_new_product_class_method(self):
        """Тест фабричного метода new_product"""
        product_data = {
            "name": "New Product",
            "description": "New Description",
            "price": 300,
            "quantity": 8
        }

        product = Product.new_product(product_data)

        assert product.name == "New Product"
        assert product.description == "New Description"
        assert product.price == 300
        assert product.quantity == 8

    def test_new_product_invalid_data(self):
        """Тест фабричного метода с некорректными данными"""
        # Не словарь
        with pytest.raises(ValueError, match="Параметры товара должны быть переданы в виде словаря"):
            Product.new_product("invalid")

        # Неполный словарь
        incomplete_data = {"name": "Product", "price": 100}
        with pytest.raises(ValueError, match="В словаре должны быть ключи: name, description, price, quantity"):
            Product.new_product(incomplete_data)


class TestSmartphone:
    """Тесты для класса Smartphone"""

    def test_smartphone_creation(self):
        """Тест создания смартфона"""
        smartphone = Smartphone(
            "iPhone", "Smartphone", 80000, 5,
            "A16 Bionic", "15 Pro", 256, "Black"
        )

        assert smartphone.name == "iPhone"
        assert smartphone.price == 80000
        assert smartphone.quantity == 5
        assert smartphone.efficiency == "A16 Bionic"
        assert smartphone.model == "15 Pro"
        assert smartphone.memory == 256
        assert smartphone.color == "Black"

    def test_smartphone_str_method(self):
        """Тест строкового представления смартфона"""
        smartphone = Smartphone(
            "iPhone", "Smartphone", 80000, 5,
            "A16 Bionic", "15 Pro", 256, "Black"
        )

        str_repr = str(smartphone)
        assert "iPhone, 80000 руб. Остаток: 5 шт." in str_repr
        assert "Модель: 15 Pro" in str_repr
        assert "Производительность: A16 Bionic" in str_repr
        assert "Память: 256 ГБ" in str_repr
        assert "Цвет: Black" in str_repr


class TestLawnGrass:
    """Тесты для класса LawnGrass"""

    def test_lawn_grass_creation(self):
        """Тест создания газонной травы"""
        grass = LawnGrass(
            "Premium Grass", "Quality grass", 1500, 100,
            "Russia", "14 days", "Green"
        )

        assert grass.name == "Premium Grass"
        assert grass.price == 1500
        assert grass.quantity == 100
        assert grass.country == "Russia"
        assert grass.germination_period == "14 days"
        assert grass.color == "Green"

    def test_lawn_grass_str_method(self):
        """Тест строкового представления газонной травы"""
        grass = LawnGrass(
            "Premium Grass", "Quality grass", 1500, 100,
            "Russia", "14 дней", "Green"
        )
        str_repr = str(grass)
        assert "Premium Grass, 1500 руб. Остаток: 100 шт." in str_repr
        assert "Страна: Russia" in str_repr
        assert "14 дней" in str_repr
        assert "Green" in str_repr


class TestCategory:
    """Тесты для класса Category (существующая функциональность)"""

    def test_category_creation(self):
        """Тест создания категории"""
        category = Category("Electronics", "Electronic devices")

        assert category.name == "Electronics"
        assert category.description == "Electronic devices"

    def test_category_add_product(self):
        """Тест добавления продукта в категорию"""
        category = Category("Electronics", "Electronic devices")
        product = Product("Laptop", "Gaming laptop", 50000, 10)

        category.add_product(product)

        # Проверяем через свойство products
        products_str = category.products
        assert "Laptop, 50000 руб. Остаток: 10 шт." in products_str

    def test_category_add_invalid_product(self):
        """Тест добавления некорректного продукта в категорию"""
        category = Category("Electronics", "Electronic devices")

        with pytest.raises(TypeError,
                           match="Добавляемый объект должен быть экземпляром класса Product или его наследников"):
            category.add_product("invalid product")

    def test_category_str_method(self):
        """Тест строкового представления категории"""
        category = Category("Electronics", "Electronic devices")
        product1 = Product("Laptop", "Desc", 50000, 10)
        product2 = Product("Phone", "Desc", 30000, 5)

        category.add_product(product1)
        category.add_product(product2)

        expected = "Electronics, количество продуктов: 15 шт."  # 10 + 5
        assert str(category) == expected

    def test_category_empty_products(self):
        """Тест свойства products для пустой категории"""
        category = Category("Electronics", "Electronic devices")
        assert category.products == "Список товаров пуст"


class TestIntegration:
    """Интеграционные тесты"""

    def test_product_count_increment(self):
        """Тест счетчика продуктов"""
        initial_count = Product.product_count

        product1 = Product("Product1", "Desc", 100, 5)
        product2 = Product("Product2", "Desc", 200, 3)
        smartphone = Smartphone("Phone", "Desc", 300, 2, "High", "X", 64, "Black")

        assert Product.product_count == initial_count + 3

    def test_category_with_different_products(self):
        """Тест категории с разными типами продуктов"""
        category = Category("Mixed", "Mixed products")

        product = Product("Product", "Desc", 100, 5)
        smartphone = Smartphone("Phone", "Desc", 200, 3, "High", "X", 64, "Black")
        grass = LawnGrass("Grass", "Desc", 50, 10, "RU", "14 days", "Green")

        category.add_product(product)
        category.add_product(smartphone)
        category.add_product(grass)

        products_str = category.products
        assert "Product, 100 руб. Остаток: 5 шт." in products_str
        assert "Phone, 200 руб. Остаток: 3 шт." in products_str
        assert "Grass, 50 руб. Остаток: 10 шт." in products_str

        # Проверяем общее количество
        assert str(category) == "Mixed, количество продуктов: 18 шт."  # 5 + 3 + 10


class TestBackwardCompatibility:
    """Тесты обратной совместимости"""

    def test_existing_product_attributes(self):
        """Тест, что старые атрибуты продукта работают корректно"""
        product = Product("Test Product", "Test Description", 1000, 5)

        # Проверяем существующие атрибуты
        assert hasattr(product, 'name')
        assert hasattr(product, 'description')
        assert hasattr(product, 'price')
        assert hasattr(product, 'quantity')
        assert hasattr(product, '_price')  # protected атрибут

        # Проверяем значения
        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.price == 1000
        assert product.quantity == 5

    def test_existing_methods_still_work(self):
        """Тест, что старые методы работают корректно"""
        product = Product("Test Product", "Test Description", 1000, 5)

        # Проверяем существующие методы
        assert callable(getattr(product, '__str__'))
        assert callable(getattr(product, '__add__'))
        assert callable(getattr(product, 'new_product'))

        # Проверяем свойства
        assert isinstance(type(product).price, property)

    def test_category_compatibility(self):
        """Тест обратной совместимости категорий"""
        category = Category("Test Category", "Test Description")
        product = Product("Test Product", "Test Description", 1000, 5)

        # Старые методы должны работать
        category.add_product(product)
        assert len([p for p in category.products.split('\n') if p != "Список товаров пуст"]) == 1

        # Строковое представление
        assert "Test Category, количество продуктов: 5 шт." in str(category)


import pytest


class TestProductCreation:
    """Тесты для создания продуктов с нулевым количеством"""

    def test_create_product_with_zero_quantity_raises_error(self):
        """Тест: создание продукта с quantity=0 вызывает ValueError"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            Product("Телефон", "Хороший телефон", 10000, 0)

    def test_create_smartphone_with_zero_quantity_raises_error(self):
        """Тест: создание смартфона с quantity=0 вызывает ValueError"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            Smartphone("iPhone", "Смартфон", 50000, 0, "Высокая", "15 Pro", 256, "Black")

    def test_create_lawn_grass_with_zero_quantity_raises_error(self):
        """Тест: создание газонной травы с quantity=0 вызывает ValueError"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            LawnGrass("Трава", "Газонная", 500, 0, "Россия", "30 дней", "Зеленый")

    def test_create_product_with_positive_quantity_success(self):
        """Тест: создание продукта с quantity>0 проходит успешно"""
        product = Product("Телефон", "Хороший телефон", 10000, 1)
        assert product.quantity == 1
        assert product.name == "Телефон"

    def test_new_product_method_with_zero_quantity_raises_error(self):
        """Тест: метод new_product с quantity=0 вызывает ValueError"""
        product_data = {
            "name": "Телефон",
            "description": "Хороший телефон",
            "price": 10000,
            "quantity": 0
        }
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            Product.new_product(product_data)


class TestCategoryMiddlePrice:
    """Тесты для метода middle_price в классе Category"""

    def test_middle_price_empty_category(self):
        """Тест: средняя цена для пустой категории возвращает 0"""
        category = Category("Пустая категория", "Нет товаров")
        assert category.middle_price() == 0

    def test_middle_price_single_product(self):
        """Тест: средняя цена для категории с одним товаром"""
        product = Product("Телефон", "Смартфон", 30000, 5)
        category = Category("Электроника", "Техника", [product])
        assert category.middle_price() == 30000

    def test_middle_price_multiple_products(self):
        """Тест: средняя цена для категории с несколькими товарами"""
        product1 = Product("Телефон", "Смартфон", 30000, 5)
        product2 = Product("Наушники", "Беспроводные", 5000, 10)
        product3 = Product("Чехол", "Защитный", 1000, 20)

        category = Category("Электроника", "Техника", [product1, product2, product3])

        expected_average = (30000 + 5000 + 1000) / 3
        assert category.middle_price() == expected_average

    def test_middle_price_after_clearing_products(self):
        """Тест: средняя цена после очистки списка товаров возвращает 0"""
        product1 = Product("Телефон", "Смартфон", 30000, 5)
        category = Category("Электроника", "Техника", [product1])

        # Очищаем приватный список товаров
        category._Category__products = []

        assert category.middle_price() == 0

    def test_middle_price_with_different_product_types(self):
        """Тест: средняя цена с разными типами продуктов (наследниками Product)"""
        smartphone = Smartphone("iPhone", "Смартфон", 50000, 5, "Высокая", "15 Pro", 256, "Black")
        lawn_grass = LawnGrass("Трава", "Газонная", 500, 10, "Россия", "30 дней", "Зеленый")
        product = Product("Чехол", "Защитный", 1000, 20)

        category = Category("Разные товары", "Разные типы", [smartphone, lawn_grass, product])

        expected_average = (50000 + 500 + 1000) / 3
        assert category.middle_price() == expected_average


class TestExistingFunctionality:
    """Тесты для существующей функциональности (регрессионные тесты)"""

    def test_product_creation_normal(self):
        """Тест: обычное создание продукта работает корректно"""
        product = Product("Телевизор", "4K", 50000, 3)
        assert product.name == "Телевизор"
        assert product.description == "4K"
        assert product.price == 50000
        assert product.quantity == 3

    def test_product_str_representation(self):
        """Тест: строковое представление продукта"""
        product = Product("Телевизор", "4K", 50000, 3)
        expected_str = "Телевизор, 50000 руб. Остаток: 3 шт."
        assert str(product) == expected_str

    def test_category_creation(self):
        """Тест: создание категории"""
        category = Category("Электроника", "Техника")
        assert category.name == "Электроника"
        assert category.description == "Техника"
        assert category.products == "Список товаров пуст"

    def test_category_add_product(self):
        """Тест: добавление продукта в категорию"""
        category = Category("Электроника", "Техника")
        product = Product("Телевизор", "4K", 50000, 3)

        category.add_product(product)

        # Проверяем через свойство products
        expected_products_str = "Телевизор, 50000 руб. Остаток: 3 шт."
        assert category.products == expected_products_str

    def test_category_str_representation(self):
        """Тест: строковое представление категории"""
        product1 = Product("Телевизор", "4K", 50000, 3)
        product2 = Product("Наушники", "Беспроводные", 5000, 5)
        category = Category("Электроника", "Техника", [product1, product2])

        expected_str = "Электроника, количество продуктов: 8 шт."
        assert str(category) == expected_str

    def test_product_addition(self):
        """Тест: сложение продуктов"""
        product1 = Product("Телевизор", "4K", 50000, 2)
        product2 = Product("Наушники", "Беспроводные", 5000, 3)

        total_value = product1 + product2
        expected_value = (50000 * 2) + (5000 * 3)
        assert total_value == expected_value

    def test_smartphone_creation(self):
        """Тест: создание смартфона"""
        smartphone = Smartphone("iPhone", "Смартфон", 50000, 5, "Высокая", "15 Pro", 256, "Black")
        assert smartphone.name == "iPhone"
        assert smartphone.model == "15 Pro"
        assert smartphone.memory == 256
        assert smartphone.quantity == 5

    def test_lawn_grass_creation(self):
        """Тест: создание газонной травы"""
        lawn_grass = LawnGrass("Трава", "Газонная", 500, 10, "Россия", "30 дней", "Зеленый")
        assert lawn_grass.name == "Трава"
        assert lawn_grass.country == "Россия"
        assert lawn_grass.germination_period == "30 дней"
        assert lawn_grass.quantity == 10


class TestEdgeCases:
    """Тесты для граничных случаев"""

    def test_middle_price_with_price_changes(self):
        """Тест: средняя цена при изменении цен товаров"""
        product1 = Product("Товар1", "Описание1", 10000, 1)
        product2 = Product("Товар2", "Описание2", 20000, 1)
        category = Category("Категория", "Описание", [product1, product2])

        # Изначальная средняя цена
        assert category.middle_price() == 15000

        # Меняем цену одного товара
        product1.price = 5000
        assert category.middle_price() == 12500

    def test_middle_price_very_low_prices(self):
        """Тест: средняя цена с очень низкими ценами"""
        product1 = Product("Товар1", "Описание1", 1, 1)
        product2 = Product("Товар2", "Описание2", 2, 1)
        category = Category("Категория", "Описание", [product1, product2])

        assert category.middle_price() == 1.5

    def test_middle_price_same_prices(self):
        """Тест: средняя цена с одинаковыми ценами"""
        product1 = Product("Товар1", "Описание1", 10000, 1)
        product2 = Product("Товар2", "Описание2", 10000, 1)
        product3 = Product("Товар3", "Описание3", 10000, 1)
        category = Category("Категория", "Описание", [product1, product2, product3])

        assert category.middle_price() == 10000

