from flask import Flask, jsonify, request
from flask_restx import Api, Resource, reqparse
from scraper import extract_laptops

app = Flask(__name__)
api = Api(app, version='1.0', title='IN8 Laptops API', description='Scrape laptops from Web Scraper Test Sites')

# Definindo os parâmetros opcionais, sem valores padrão
laptop_parser = reqparse.RequestParser()
laptop_parser.add_argument('page', type=int, required=False, help='Número da página')
laptop_parser.add_argument('limit', type=int, required=False, help='Quantidade máxima de laptops')
laptop_parser.add_argument('all_brands', type=bool, required=False, help='Incluir todas as marcas ou não')

@api.route('/laptops')
class LaptopsResource(Resource):
    @api.expect(laptop_parser)  # Isso garante que os parâmetros apareçam no Swagger
    def get(self):
        try:
            # Obtém parâmetros da query string
            args = laptop_parser.parse_args()
            page_number = args.get('page')  # Será None se não for fornecido
            max_laptops = args.get('limit')  # Será None se não for fornecido
            all_brands = args.get('all_brands')  # Será None se não for fornecido
            
            # Chama a função de scraping com os parâmetros opcionais
            all_laptops = extract_laptops(page_number=page_number, max_laptops=max_laptops, all_brands=all_brands)

            if not all_laptops:
                return jsonify({'message': 'Nenhum laptop encontrado'})

            return jsonify(all_laptops)

        except ValueError as e:
            # Exemplo de erro de valor, como erros ao processar dados
            return jsonify({'error': 'Erro ao processar dados', 'details': str(e)}), 400
        
        except Exception as e:
            # Captura qualquer outro erro
            return jsonify({'error': 'Erro interno do servidor', 'details': str(e)}), 500

@app.route('/ping')
def home():
    return jsonify({"message": "API Flask rodando na Vercel"})

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Requisição mal formada', 'details': str(error)}), 400

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Recurso não encontrado', 'details': str(error)}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Erro interno do servidor', 'details': str(error)}), 500

if __name__ == '__main__':
    app.run(debug=True)