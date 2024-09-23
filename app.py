from flask import Flask, jsonify
from flask_restx import Api, Resource, reqparse
from scraper import LaptopScraper

app = Flask(__name__)
api = Api(app, version='1.0', title='Scraper Laptops API', description='Scrape laptops from Web Scraper Test Sites\n\nDeveloped by Victor Martins')

# Definindo os parâmetros opcionais
laptop_parser = reqparse.RequestParser()
laptop_parser.add_argument('page', type=int, help='Número da página')
laptop_parser.add_argument('limit', type=int, help='Quantidade máxima de laptops')
laptop_parser.add_argument('all_brands', type=bool, help='Incluir todas as marcas ou não')

laptop_ns = api.namespace('laptops', description='Operações relacionadas a laptops')

@laptop_ns.route('/')
class LaptopsResource(Resource):
    """
    Classe para gerenciar laptops.

    Métodos:
        get: Retorna uma lista de laptops.
    """

    @laptop_ns.doc('get_laptops')
    @laptop_ns.expect(laptop_parser)
    def get(self):
        """
        Recupera uma lista de laptops.

        Returns:
            Response: JSON contendo a lista de laptops.
        """
        try:
            # Obtém parâmetros da query string
            args = laptop_parser.parse_args()
            page_number = args.get('page')  # Será None se não for fornecido
            max_laptops = args.get('limit')  # Será None se não for fornecido
            all_brands = args.get('all_brands')  # Não deve ter valor padrão, será None se não for fornecido
            
            # Chama a função de scraping com os parâmetros opcionais
            scraper = LaptopScraper()
            laptops_data = scraper.extract_laptops(page_number=page_number, max_laptops=max_laptops, all_brands=all_brands)

            if not laptops_data:
                return jsonify({'message': 'Nenhum laptop encontrado'}), 404

            return jsonify(laptops_data)

        except ValueError as e:
            return jsonify({'error': 'Erro ao processar dados', 'details': str(e)}), 400
        
        except Exception as e:
            return jsonify({'error': 'Erro interno do servidor', 'details': str(e)}), 500

@laptop_ns.route('/ping')
class PingResource(Resource):
    def get(self):
        return jsonify({"message": "API Flask rodando na Vercel"})

# Definindo manipuladores de erro diretamente na API
@api.errorhandler
def handle_error(error):
    """Manipulador de erro genérico"""
    return jsonify({'error': 'Erro interno do servidor', 'details': str(error)}), 500

if __name__ == '__main__':
    app.run(debug=True)