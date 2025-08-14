import os
import json

from src.class_config import Product, Category

def read_data_from_json(path:str = "../data/products.json") -> any:
    full_path = os.path.abspath(path)
    with open(full_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

print(read_data_from_json())