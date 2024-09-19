import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from typing import List, Dict, Optional, Union

import logging

logging.basicConfig(level=logging.DEBUG)

# VARIÁVEIS GLOBAIS
collection_date: str = datetime.now().strftime('%Y-%m-%d')
list_base_url: str = 'https://webscraper.io/test-sites/e-commerce/static/computers/laptops'
product_base_url: str = 'https://webscraper.io/test-sites/e-commerce/static/product'
all_labels: List[str] = []

# Função para extrair características usando expressões regulares
def extract_features(description: str) -> Dict[str, Optional[str]]:
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
        'Sistema Operacional': os if os else None
    }

# Função para extrair detalhes adicionais dos produtos
def extract_product_details(product_url: str) -> Dict[str, Dict[str, str]]:
    response = requests.get(product_url)
    details: Dict[str, Dict[str, str]] = {}

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        labels = soup.find_all('label')
        for label in labels:
            label_text = label.text.strip().replace(':', '')
            all_labels.append(label_text)

            buttons = label.find_next_sibling('div', class_='swatches').find_all('button') if label.find_next_sibling('div', class_='swatches') else []
            
            button_values = {}
            for button in buttons:
                value = button['value']
                is_disabled = 'disabled' in button.attrs
                button_values[value] = 'disabled' if is_disabled else 'enabled'
            
            details[label_text] = button_values

    return details

# Função para extrair dados dos laptops de uma página
def extract_laptops_from_page(url: str, all_brands: bool = False) -> List[Dict[str, Union[str, int]]]:
    response = requests.get(url)
    laptops: List[Dict[str, Union[str, int]]] = []

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

            # Verifica se a marca contém "Lenovo" ou se o parâmetro all_brands é True
            if not all_brands and 'Lenovo' not in description:
                continue

            product_details = extract_product_details(product_link)

            features = extract_features(description)
            features.update({
                'Nome': name,
                'Preço': price,
                'Imagem URL': image_url,
                'Reviews': review_count,
                'Estrelas': rating_stars,
                'Link Produto': product_link,
                'ID Produto': product_id,
                'HDD': product_details.get('HDD', {}),
                'Data Coleta': collection_date
            })

            laptops.append(features)
    else:
        logging.error(f'Falha na requisição: Status code {response.status_code}')
    return laptops

# Função para obter o número da última página
def get_last_page_number(base_url: str) -> int:
    response = requests.get(base_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        pagination = soup.find('ul', class_='pagination')
        if pagination:
            pages = pagination.find_all('a', class_='page-link')
            last_page = pages[-2].text.strip()
            return int(last_page)
    return 1

# Função para extrair laptops com parâmetros opcionais
def extract_laptops(page_number: Optional[int] = None, max_laptops: Optional[int] = None, all_brands: bool = False) -> List[Dict[str, Union[str, int]]]:
    # URL base da primeira página
    base_url: str = 'https://webscraper.io/test-sites/e-commerce/static/computers/laptops'

    # Obtém o número da última página se não for especificada uma página específica
    last_page: int = get_last_page_number(base_url) if page_number is None else page_number

    # Lista para armazenar todos os dados dos laptops
    all_laptops: List[Dict[str, Union[str, int]]] = []
    laptops_collected: int = 0

    # Se uma página específica for fornecida, coleta dados apenas dessa página
    if page_number:
        url: str = f'{base_url}?page={page_number}'
        logging.info(f'Extraindo dados da página {page_number}...')
        laptops: List[Dict[str, Union[str, int]]] = extract_laptops_from_page(url, all_brands=all_brands)
        all_laptops.extend(laptops)
        laptops_collected += len(laptops)
    else:
        # Itera sobre cada página
        for page in range(1, last_page + 1):
            url: str = f'{base_url}?page={page}'
            logging.info(f'Extraindo dados da página {page}...')
            laptops: List[Dict[str, Union[str, int]]] = extract_laptops_from_page(url, all_brands=all_brands)
            all_laptops.extend(laptops)
            laptops_collected += len(laptops)
            if max_laptops and laptops_collected >= max_laptops:
                break

    return all_laptops