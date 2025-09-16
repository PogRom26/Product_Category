import pytest
import json
from src.utils import read_data_from_json, greate_object_from_json
from src.class_config import Category


# Тест для функции read_data_from_json
def test_read_data_from_json(tmp_path, product_list):
    # Создаём временный JSON-файл
    test_data = [
        {
            "name": "Test Category",
            "description": "Test Description",
            "products": [
                {
                    "name": "Product 1",
                    "description": "Desc 1",
                    "price": 19.99,
                    "quantity": 5,
                },
                {
                    "name": "Product 2",
                    "description": "Desc 2",
                    "price": 29.99,
                    "quantity": 3,
                },
            ],
        }
    ]
    json_file = tmp_path / "test_products.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f)

    # Читаем данные
    data = read_data_from_json(str(json_file))

    # Проверяем, что данные прочитаны корректно
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Test Category"
    assert data[0]["description"] == "Test Description"
    assert len(data[0]["products"]) == 2
    assert data[0]["products"][0]["name"] == "Product 1"


# Тест для обработки несуществующего файла
def test_read_data_from_json_file_not_found(tmp_path):
    non_existent_file = tmp_path / "non_existent.json"
    with pytest.raises(FileNotFoundError):
        read_data_from_json(str(non_existent_file))


# Тест для проверки создания объектов из JSON-данных
def test_create_object_from_json():
    """Тест создания объектов Category и Product из JSON-данных"""
    json_data = [
        {
            "name": "Sample Category",
            "description": "This is a sample category",
            "products": [
                {
                    "name": "Product 1",
                    "description": "Description 1",
                    "price": 19.99,
                    "quantity": 5,
                },
                {
                    "name": "Product 2",
                    "description": "Description 2",
                    "price": 29.99,
                    "quantity": 3,
                },
                {
                    "name": "Product 3",
                    "description": "Description 3",
                    "price": 39.99,
                    "quantity": 7,
                },
            ],
        }
    ]

    # Создаем объекты из JSON
    categories = greate_object_from_json(json_data)

    # Проверяем результат
    assert len(categories) == 1
    category = categories[0]
    assert isinstance(category, Category)
    assert category.name == "Sample Category"
    assert category.description == "This is a sample category"

    # Проверяем продукты (доступ к приватному атрибуту __products)
    assert len(category._Category__products) == 3  # Проверяем количество продуктов
    assert category._Category__products[0].name == "Product 1"
    assert category._Category__products[0].price == 19.99
    assert category._Category__products[0].quantity == 5
    assert "Product 1, 19.99 руб. Остаток: 5 шт." in category.products  # Проверяем строку products


# Тест для пустых данных
def test_greate_object_from_json_empty():
    json_data = []
    categories = greate_object_from_json(json_data)
    assert categories == []


# Тест для категории с пустым списком продуктов
def test_greate_object_from_json_empty_products(empty_category):
    json_data = [
        {
            "name": "Empty Category",
            "description": "This is an empty category",
            "products": [],
        }
    ]
    categories = greate_object_from_json(json_data)

    assert len(categories) == 1
    category = categories[0]
    assert isinstance(category, Category)
    assert category.name == "Empty Category"
    assert category.description == "This is an empty category"
