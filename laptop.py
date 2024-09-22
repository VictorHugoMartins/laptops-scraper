from typing import Optional, Dict
import json

class Laptop:
    def __init__(self, name: str, price: float, currency: str, brand: str, dimensions: Optional[str], processor: Optional[str],
                 ram: Optional[str], storage: Optional[str], os: Optional[str], image_url: str,
                 review_count: str, rating_stars: int, product_link: str, product_id: str, hdd: Optional[Dict[str, str]], 
                 collection_date: str):
        self.name = name
        self.price = price
        self.currency = currency
        self.brand = brand
        self.dimensions = dimensions
        self.processor = processor
        self.ram = ram
        self.storage = storage
        self.os = os
        self.image_url = image_url
        self.review_count = review_count
        self.rating_stars = rating_stars
        self.product_link = product_link
        self.product_id = product_id
        self.hdd = hdd
        self.collection_date = collection_date

    def __repr__(self):
        return f"Laptop({self.name}, {self.price}, {self.currency}, {self.brand}, {self.dimensions}, {self.processor}, " \
               f"{self.ram}, {self.storage}, {self.os}, {self.image_url}, {self.review_count}, " \
               f"{self.rating_stars}, {self.product_link}, {self.product_id}, {self.hdd}, {self.collection_date})"
    
    def to_json(self) -> str:
        # Converte o objeto em um dicionário e depois em uma string JSON
        return json.dumps(self.__dict__, default=str, indent=4)