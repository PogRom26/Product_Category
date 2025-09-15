class Product:
    """ Класс для определения продуктов, их названия, описания, цены и остатков"""

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

    @classmethod
    def new_product(cls, product_data):
        """Класс-метод для создания объекта Product из словаря с параметрами"""
        if not isinstance(product_data, dict):
            raise ValueError("Параметры товара должны быть переданы в виде словаря")

        required_keys = {"name", "description", "price", "quantity"}
        if not all(key in product_data for key in required_keys):
            raise ValueError("В словаре должны быть ключи: name, description, price, quantity")

        return cls(
            product_data["name"],
            product_data["description"],
            product_data["price"],
            product_data["quantity"]
        )

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
        self.__products = products if products is not None else []  # Инициализация пустым списком, если products не передан

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product):
        """Метод для добавления продукта в приватный список товаров"""
        if isinstance(product, Product):  # Проверка, что передан объект класса Product
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise ValueError("Добавляемый объект должен быть экземпляром класса Product")

    @property
    def products(self):
        """Геттер для вывода списка товаров в формате: Название продукта, цена руб. Остаток: количество шт."""
        if not self.__products:
            return "Список товаров пуст"
        return "\n".join(f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
                         for product in self.__products)