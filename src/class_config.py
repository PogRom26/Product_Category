class Product:
    """Класс для определения продуктов, их названия, описания, цены и остатков"""

    name = str
    description = str
    __price = float  # Приватный атрибут цены
    quantity = int

    product_count = 0

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price if price > 0 else 0  # Инициализация с проверкой
        self.quantity = quantity
        Product.product_count += 1

    def __str__(self):
        """Строковое представление продукта в формате: Название продукта, 80 руб. Остаток: 15 шт."""
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """
        Сложение двух продуктов.
        Результат - общая стоимость всех товаров на складе.
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")

        return (self.__price * self.quantity) + (other.__price * other.quantity)

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
        return self.__price

    @price.setter
    def price(self, value):
        """Сеттер для установки цены с проверкой"""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value


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
        if isinstance(product, Product):  # Проверка, что передан объект класса Product
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise ValueError("Добавляемый объект должен быть экземпляром класса Product")

    def __str__(self):
        """Строковое представление продукта в формате: Название категории, количество продуктов: 200 шт."""
        return f"{self.name}, количество продуктов: {self.product_count} шт."

    @property
    def products(self):
        """Геттер для вывода списка товаров в формате: Название продукта, цена руб. Остаток: количество шт."""
        if not self.__products:
            return "Список товаров пуст"
        return "\n".join(
            f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт." for product in self.__products
        )
