import pytest
from unittest.mock import patch
from scraper import extract_features, extract_laptops_from_page, extract_product_details

# Mock de dados para os testes
mock_product_details = {
    'title': 'Dell Latitude 5580',
    'price': '$1337.28',
    'description': 'Dell Latitude 5580, 15.6" FHD, Core i7-7600U, 8GB, 256GB SSD, GeForce GT930MX, Windows 10 Pro',
    'reviews': '6 reviews'
}

mock_laptops_page = [
    {
        'title': 'Dell Latitude 5580',
        'price': '$1337.28',
        'description': 'Dell Latitude 5580, 15.6" FHD, Core i7-7600U, 8GB, 256GB SSD, GeForce GT930MX, Windows 10 Pro',
        'url': '/test-sites/e-commerce/static/product/139'
    },
    {
        'title': 'Dell Latitude 5480',
        'price': '$1338.37',
        'description': 'Dell Latitude 5480, 14" FHD, Core i7-7600U, 8GB, 256GB SSD, Linux + Windows 10 Home',
        'url': '/test-sites/e-commerce/static/product/140'
    }
]

def test_extract_features():
    description = "Brand X Core i7-8550U 16GB RAM 512GB SSD Windows 10"
    features = extract_features(description)
    assert features['Marca'] == 'Brand'
    assert features['Processador'] == 'Core i7-8550U'
    assert features['RAM'] == '16GB'
    assert features['Armazenamento'] == '512GB SSD'
    assert features['Sistema Operacional'] == 'Windows 10'

@patch('scraper.requests.get')
def test_extract_product_details(mock_get):
    mock_get.return_value.json.return_value = mock_product_details
    url = 'https://webscraper.io/test-sites/e-commerce/static/product/1'
    details = extract_product_details(url)
    assert details == mock_product_details
    assert isinstance(details, dict)

@patch('scraper.requests.get')
def test_extract_laptops_from_page(mock_get):
    # Testa com todos os laptops (marca Lenovo por padrão)
    mock_get.return_value.json.return_value = mock_laptops_page
    url = 'https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page=1'
    laptops = extract_laptops_from_page(url)
    assert len(laptops) > 0
    assert isinstance(laptops[0], dict)
    
    # Testa com todos os parâmetros opcionais
    url = 'https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page=1'
    laptops_all = extract_laptops_from_page(url, all=True)
    assert len(laptops_all) > 0
    assert isinstance(laptops_all[0], dict)
    
    # Testa a marca específica (e.g., Lenovo)
    url = 'https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page=1'
    laptops_lenovo = extract_laptops_from_page(url, all=False)
    assert len(laptops_lenovo) > 0
    assert isinstance(laptops_lenovo[0], dict)