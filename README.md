# Laptops Scraper

Este projeto realiza scraping de laptops a partir de um [site de testes de Web Scraper](https://webscraper.io/test-sites/e-commerce/static/computers).

## Funcionamento

Por padrão, o endpoint retorna todos os laptops da marca **Lenovo** presentes no site. No entanto, você pode usar parâmetros opcionais para coletar laptops de outras marcas, especificar uma página exata ou definir um limite para a quantidade de itens retornados.

### Features capturadas:
- **Nome** do laptop
- **Preço** (separado da moeda)
- **Moeda** relacionada ao preço
- **Marca** do produto
- **Dimensões** (altura, largura, profundidade)
- **Processador**
- **Memória RAM**
- **Armazenamento** (capacidade e tipo)
- **Sistema Operacional**
- **Link da foto** do produto
- **Quantidade de reviews**
- **Classificação em estrelas**
- **Link da página de detalhes** do produto
- **ID** do produto
- **Opções de HDD** (disponíveis em 128GB, 256GB, 512GB, 1024GB, se habilitadas)
- **Data da coleta** das informações

### Principais bibliotecas e ferramentas utilizadas:
- `Requests` — para realizar as requisições HTTP
- `BeautifulSoup` — para fazer o parsing do HTML
- `Typing` — para garantir a tipagem adequada dos endpoints
- `Flask` — para a criação da API
- `Vercel` — para disponibilização da API

A API também está documentada e disponível para uso, incluindo a interface Swagger, no seguinte link: [Laptops Scraper API](https://laptops-scraper.vercel.app/).