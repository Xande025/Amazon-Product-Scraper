"""
Blueprint para endpoints de scraping da Amazon
"""

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.scraper import scrape_amazon_products
import time

# Criar blueprint para scraping
scraper_bp = Blueprint('scraper', __name__)


@scraper_bp.route('/scrape', methods=['GET'])
@cross_origin()  # Permitir CORS para este endpoint
def scrape_products():
    """
    Endpoint para fazer scraping de produtos da Amazon
    
    Parâmetros de query:
    - keyword: palavra-chave para pesquisar (obrigatório)
    - max_products: número máximo de produtos para retornar (opcional, padrão: 20)
    
    Retorna:
    - JSON com dados dos produtos encontrados
    """
    try:
        # Obter parâmetros da query string
        keyword = request.args.get('keyword')
        max_products = request.args.get('max_products', 20, type=int)
        
        # Validar parâmetros obrigatórios
        if not keyword:
            return jsonify({
                'success': False,
                'error': 'Parâmetro "keyword" é obrigatório',
                'message': 'Por favor, forneça uma palavra-chave para pesquisar'
            }), 400
        
        # Validar número máximo de produtos
        if max_products < 1 or max_products > 50:
            return jsonify({
                'success': False,
                'error': 'Parâmetro "max_products" deve estar entre 1 e 50',
                'message': 'Número de produtos deve ser entre 1 e 50'
            }), 400
        
        # Registrar início do scraping
        start_time = time.time()
        print(f"Iniciando scraping para keyword: {keyword}, max_products: {max_products}")
        
        # Fazer scraping dos produtos
        result = scrape_amazon_products(keyword, max_products)
        
        # Calcular tempo de execução
        execution_time = round(time.time() - start_time, 2)
        result['execution_time'] = execution_time
        
        # Verificar se o scraping foi bem-sucedido
        if result['success']:
            print(f"Scraping concluído com sucesso em {execution_time}s. Produtos encontrados: {result['total_products']}")
            return jsonify(result), 200
        else:
            print(f"Erro no scraping: {result.get('error', 'Erro desconhecido')}")
            return jsonify(result), 500
            
    except ValueError as e:
        # Erro de validação de parâmetros
        return jsonify({
            'success': False,
            'error': 'Erro de validação',
            'message': str(e)
        }), 400
        
    except Exception as e:
        # Erro interno do servidor
        print(f"Erro interno no endpoint de scraping: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor',
            'message': 'Ocorreu um erro inesperado durante o scraping'
        }), 500


@scraper_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """
    Endpoint para verificar se o serviço está funcionando
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Amazon Scraper API',
        'timestamp': time.time()
    }), 200


@scraper_bp.route('/info', methods=['GET'])
@cross_origin()
def api_info():
    """
    Endpoint com informações sobre a API
    """
    return jsonify({
        'name': 'Amazon Scraper API',
        'version': '1.0.0',
        'description': 'API para fazer scraping de produtos da Amazon',
        'endpoints': {
            '/api/scrape': {
                'method': 'GET',
                'description': 'Faz scraping de produtos da Amazon',
                'parameters': {
                    'keyword': 'string (obrigatório) - palavra-chave para pesquisar',
                    'max_products': 'integer (opcional) - número máximo de produtos (1-50, padrão: 20)'
                },
                'example': '/api/scrape?keyword=notebook&max_products=10'
            },
            '/api/health': {
                'method': 'GET',
                'description': 'Verifica se o serviço está funcionando'
            },
            '/api/info': {
                'method': 'GET',
                'description': 'Informações sobre a API'
            }
        }
    }), 200

