import re
import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
from laptop import Laptop
import json

logging.basicConfig(level=logging.DEBUG)

class LaptopScraper:
    def __init__(self):
        self.collection_date: str = datetime.now().strftime('%Y-%m-%d')
        self.list_base_url: str = 'https://webscraper.io/test-sites/e-commerce/static/computers/laptops'
        self.product_base_url: str = 'https://webscraper.io/test-sites/e-commerce/static/product'
        self.all_labels: List[str] = []

    def extract_features(self, description: str) -> Dict[str, Optional[str]]:
        brand = re.search(r'^[A-Za-z]+', description)
        dimensions = re.search(r'\d+(\.\d+)?\s*["\']', description)
        processor = re.search(r'Core\s*[i][0-9]{1,2}-[0-9]{1,4}U', description)
        ram = re.search(r'\d+GB', description)
        storage = re.search(r'\d+GB\s*(SSD|HDD|SSHD)', description)
        os = description.split(',')[-1][1:]

        return {
            'Marca': brand.group(0) if brand else None,
            'Dimensões': dimensions.group(0) if dimensions else None,
            'Processador': processor.group(0) if processor else None,
            'RAM': ram.group(0) if ram else None,
            'Armazenamento': storage.group(0) if storage else None,
            'Sistema Operacional': os.strip() if os else None
        }

    def extract_product_details(self, product_url: str) -> Dict[str, Dict[str, str]]:
        response = requests.get(product_url)
        details: Dict[str, Dict[str, str]] = {}

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            labels = soup.find_all('label')
            for label in labels:
                label_text = label.text.strip().replace(':', '')
                buttons = label.find_next_sibling('div', class_='swatches').find_all('button') if label.find_next_sibling('div', class_='swatches') else []
                
                button_values = {}
                for button in buttons:
                    value = button['value']
                    is_disabled = 'disabled' in button.attrs
                    button_values[value] = 'disabled' if is_disabled else 'enabled'
                
                details[label_text] = button_values

        return details

    def create_laptop(self, name: str, price: str, description: str, image_url: str, 
                      review_count: str, rating_stars: int, product_link: str, product_id: str) -> Laptop:
        features = self.extract_features(description)
        product_details = self.extract_product_details(product_link)

        l = Laptop(
            name=name,
            price=price,
            brand=features['Marca'],
            dimensions=features['Dimensões'],
            processor=features['Processador'],
            ram=features['RAM'],
            storage=features['Armazenamento'],
            os=features['Sistema Operacional'],
            image_url=image_url,
            review_count=review_count,
            rating_stars=rating_stars,
            product_link=product_link,
            product_id=product_id,
            hdd=product_details.get('HDD', {}),
            collection_date=self.collection_date
        )
        return l

    def extract_laptops_from_page(self, url: str, all_brands: bool = False) -> List[Laptop]:
        response = requests.get(url)
        laptops: List[Laptop] = []

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('div', class_='card thumbnail')

            for item in items:
                name = item.find('a', class_='title')['title'].strip()
                price = item.find('h4', class_='price').text.strip()
                description = item.find('p', class_='description').text.strip()
                image_url = item.find('img', class_='img-fluid')['src']
                review_count = item.find('p', class_='review-count').text.strip().replace(' reviews', '')
                rating_stars = len(item.find_all('span', class_='ws-icon-star'))

                product_link = "https://webscraper.io" + item.find('a', class_='title')['href']
                product_id = product_link.split('/')[-1]

                if not all_brands and 'Lenovo' not in description:
                    continue

                laptop = self.create_laptop(name, price, description, image_url, review_count, rating_stars, product_link, product_id)
                laptops.append(laptop)
        else:
            logging.error(f'Falha na requisição: Status code {response.status_code}')
        laptops = [json.loads(laptop.to_json()) for laptop in laptops]
        return laptops

    def get_last_page_number(self) -> int:
        response = requests.get(self.list_base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            pagination = soup.find('ul', class_='pagination')
            if pagination:
                pages = pagination.find_all('a', class_='page-link')
                last_page = pages[-2].text.strip()
                return int(last_page)
        return 1

    def extract_laptops(self, page_number: Optional[int] = None, max_laptops: Optional[int] = None, all_brands: bool = False) -> List[Laptop]:
        last_page: int = self.get_last_page_number() if page_number is None else page_number

        all_laptops: List[Laptop] = []
        laptops_collected: int = 0

        if page_number:
            url: str = f'{self.list_base_url}?page={page_number}'
            logging.info(f'Extraindo dados da página {page_number}...')
            laptops: List[Laptop] = self.extract_laptops_from_page(url, all_brands=all_brands)
            all_laptops.extend(laptops)
            laptops_collected += len(laptops)
        else:
            for page in range(1, last_page + 1):
                url: str = f'{self.list_base_url}?page={page}'
                logging.info(f'Extraindo dados da página {page}...')
                laptops: List[Laptop] = self.extract_laptops_from_page(url, all_brands=all_brands)
                all_laptops.extend(laptops)
                laptops_collected += len(laptops)
                if max_laptops and laptops_collected >= max_laptops:
                    break

        return all_laptops