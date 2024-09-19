from flask import Flask, jsonify, request
from flask_restx import Api, Resource
from scraper import extract_laptops

app = Flask(__name__)
api = Api(app, version='1.0', title='IN8 Laptops API', description='Scrape laptops from Web Scraper Test Sites')

@api.route('/laptops')
class LaptopsResource(Resource):
    def get(self):
        try:
            # Obtém parâmetros da query string
            page_number = request.args.get('page', type=int)
            max_laptops = request.args.get('max', type=int)
            
            # Chama a função de scraping com parâmetros opcionais
            all_laptops = extract_laptops(page_number=page_number, max_laptops=max_laptops)

            if not all_laptops:
                return jsonify({'message': 'Nenhum laptop encontrado'})
            print(all_laptops)

            return jsonify(all_laptops)
        
        except ValueError as e:
            # Exemplo de erro de valor, como erros ao processar dados
            return jsonify({'error': 'Erro ao processar dados', 'details': str(e)}), 400
        
        except Exception as e:
            # Captura qualquer outro erro
            return jsonify({'error': 'Erro interno do servidor', 'details': str(e)}), 500

@app.route('/')
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