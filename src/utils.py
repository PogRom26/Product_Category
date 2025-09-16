import os
import json

from src.class_config import Product, Category


def read_data_from_json(path: str = "../data/products.json") -> dict:
    """Функция для чтения данных из json-файла.
    Если адрес не указан, что функция принимает адрес по умолчанию ../data/products.json"""

    full_path = os.path.abspath(path)
    with open(full_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


# print(read_data_from_json())


def greate_object_from_json(data):
    """Функция для создания объектов класса из данных json-файла"""

    categories = []
    for category in data:
        products = []
        for product in category["products"]:
            products.append(Product(**product))
        category["products"] = products
        categories.append(Category(**category))
    return categories


# Примеры использования
# data = read_data_from_json()
# print(data)
# users_data = greate_object_from_json(data)
# print(users_data[0].name)
# print(users_data[0].products[0].name)
