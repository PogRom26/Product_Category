from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов"""

    @abstractmethod
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self._price = price if price > 0 else 0
        self.quantity = quantity

    @abstractmethod
    def __str__(self):
        """Абстрактный метод для строкового представления продукта"""
        pass

    @abstractmethod
    def __add__(self, other):
        """Абстрактный метод для сложения продуктов"""
        pass

    @property
    @abstractmethod
    def price(self):
        """Абстрактный геттер для цены"""
        pass

    @price.setter
    @abstractmethod
    def price(self, value):
        """Абстрактный сеттер для цены"""
        pass


class Product(BaseProduct):
    """Класс для определения продуктов, их названия, описания, цены и остатков"""

    product_count = 0

    def __init__(self, name, description, price, quantity):
        super().__init__(name, description, price, quantity)
        Product.product_count += 1

    def __str__(self):
        """Строковое представление продукта в формате: Название продукта, 80 руб. Остаток: 15 шт."""
        return f"{self.name}, {self._price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")

        if not isinstance(other, type(self)):
            raise TypeError("Нельзя складывать товары из разных классов продуктов")

        return (self._price * self.quantity) + (other._price * other.quantity)

    @classmethod
    def new_product(cls, product_data):
        """Класс-метод для создания объекта Product из словаря с параметрами"""
        if not isinstance(product_data, dict):
            raise ValueError("Параметры товара должны быть переданы в виде словаря")

        required_keys = {"name", "description", "price", "quantity"}
        if not all(key in product_data for key in required_keys):
            raise ValueError("В словаре должны быть ключи: name, description, price, quantity")

        return cls(product_data["name"], product_data["description"], product_data["price"], product_data["quantity"])

    @property
    def price(self):
        """Геттер для получения цены"""
        return self._price

    @price.setter
    def price(self, value):
        """Сеттер для установки цены с проверкой"""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self._price = value


class Smartphone(Product):
    """Класс для смартфонов, наследуется от Product"""

    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency  # производительность
        self.model = model  # модель
        self.memory = memory  # объем встроенной памяти
        self.color = color  # цвет

    def __str__(self):
        """Строковое представление смартфона с дополнительными атрибутами"""
        base_str = super().__str__()
        return (
            f"{base_str}\n"
            f"Модель: {self.model}, Производительность: {self.efficiency}, "
            f"Память: {self.memory} ГБ, Цвет: {self.color}"
        )


class LawnGrass(Product):
    """Класс для газонной травы, наследуется от Product"""

    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country  # страна-производитель
        self.germination_period = germination_period  # срок прорастания
        self.color = color  # цвет

    def __str__(self):
        """Строковое представление газонной травы с дополнительными атрибутами"""
        base_str = super().__str__()
        return (
            f"{base_str}\n"
            f"Страна: {self.country}, Срок прорастания: {self.germination_period}, "
            f"Цвет: {self.color}"
        )


class Category:
    """Класс категорий товаров, включающий название, описание, и список самих продуктов"""

    name = str
    description = str
    __products = list  # Приватный атрибут

    category_count = 0
    product_count = 0

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.__products = (
            products if products is not None else []
        )  # Инициализация пустым списком, если products не передан

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product):
        """Метод для добавления продукта в приватный список товаров"""
        # Проверяем, что передан объект класса Product или его наследников
        if not isinstance(product, Product):
            raise TypeError("Добавляемый объект должен быть экземпляром класса Product или его наследников")

        self.__products.append(product)
        Category.product_count += 1

    def __str__(self):
        """Строковое представление категории в формате: Название категории, количество продуктов: X шт."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    @property
    def products(self):
        """Геттер для вывода списка товаров в формате: Название продукта, цена руб. Остаток: количество шт."""
        if not self.__products:
            return "Список товаров пуст"
        return "\n".join(
            f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт." for product in self.__products
        )
