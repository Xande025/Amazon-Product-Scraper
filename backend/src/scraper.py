"""
Amazon Web Scraper Module
Este módulo contém funções para extrair dados de produtos da Amazon
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urlencode


class AmazonScraper:
    """
    Classe principal para fazer scraping de produtos da Amazon
    """
    
    def __init__(self):
        # Lista de User-Agents para rotação
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        ]
        self.headers_base = {
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        # Configurar sessão para reutilizar conexões
        self.session = requests.Session()
    
    def build_search_url(self, keyword):
        """
        Constrói a URL de pesquisa da Amazon para uma palavra-chave específica
        
        Args:
            keyword (str): Palavra-chave para pesquisar
            
        Returns:
            str: URL completa de pesquisa da Amazon
        """
        # URL base da Amazon Brasil
        base_url = "https://www.amazon.com.br/s?"
        
        # Parâmetros de pesquisa
        params = {
            'k': keyword,
            'ref': 'sr_pg_1'
        }
        
        # Construir URL completa
        search_url = base_url + urlencode(params)
        return search_url
    
    def fetch_page_content(self, url):
        """
        Faz requisição HTTP para obter o conteúdo da página
        
        Args:
            url (str): URL da página para fazer scraping
            
        Returns:
            str: Conteúdo HTML da página ou None se houver erro
        """
        try:
            # Adicionar delay aleatório para evitar detecção de bot
            time.sleep(random.uniform(1, 3))
            # Rotacionar User-Agent
            user_agent = random.choice(self.user_agents)
            headers = self.headers_base.copy()
            headers['User-Agent'] = user_agent
            # Fazer requisição HTTP
            response = self.session.get(url, headers=headers, timeout=10)
            # Verificar se a requisição foi bem-sucedida
            if response.status_code == 200:
                return response.text
            else:
                print(f"Erro na requisição: Status code {response.status_code}")
                print(f"User-Agent usado: {user_agent}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Erro ao fazer requisição: {str(e)}")
            return None
    
    def extract_product_data(self, html_content):
        """
        Extrai dados dos produtos do HTML da página de resultados
        
        Args:
            html_content (str): Conteúdo HTML da página
            
        Returns:
            list: Lista de dicionários com dados dos produtos
        """
        if not html_content:
            return []
        
        # Criar objeto BeautifulSoup para parsing do HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Lista para armazenar dados dos produtos
        products = []
        
        # Encontrar todos os containers de produtos
        # A Amazon usa diferentes seletores, vamos tentar vários
        product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        if not product_containers:
            # Tentar seletor alternativo
            product_containers = soup.find_all('div', class_=re.compile(r's-result-item'))
        
        print(f"Encontrados {len(product_containers)} produtos")
        
        for container in product_containers:
            try:
                product_data = self.extract_single_product(container)
                if product_data:
                    products.append(product_data)
            except Exception as e:
                print(f"Erro ao extrair produto: {str(e)}")
                continue
        
        return products
    
    def extract_single_product(self, container):
        """
        Extrai dados de um único produto do container HTML
        
        Args:
            container: Elemento BeautifulSoup do container do produto
            
        Returns:
            dict: Dados do produto ou None se não conseguir extrair
        """
        product_data = {}
        
        # Extrair título do produto
        title_element = container.find('h2', class_=re.compile(r's-size-mini'))
        if not title_element:
            title_element = container.find('span', class_=re.compile(r'a-size-.*-text'))
        
        if title_element:
            # Pegar o texto do link dentro do h2
            title_link = title_element.find('a')
            if title_link:
                product_data['title'] = title_link.get_text(strip=True)
            else:
                product_data['title'] = title_element.get_text(strip=True)
        else:
            return None  # Se não tem título, não é um produto válido
        
        # Extrair classificação (estrelas)
        rating_element = container.find('span', class_=re.compile(r'a-icon-alt'))
        if rating_element:
            rating_text = rating_element.get_text()
            # Extrair número de estrelas usando regex
            rating_match = re.search(r'(\d+(?:,\d+)?)', rating_text)
            if rating_match:
                product_data['rating'] = rating_match.group(1).replace(',', '.')
            else:
                product_data['rating'] = 'N/A'
        else:
            product_data['rating'] = 'N/A'
        
        # Extrair número de avaliações
        reviews_element = container.find('a', class_=re.compile(r'a-link-normal'))
        if reviews_element:
            reviews_text = reviews_element.get_text()
            # Extrair número de avaliações
            reviews_match = re.search(r'(\d+(?:\.\d+)*)', reviews_text)
            if reviews_match:
                product_data['reviews_count'] = reviews_match.group(1)
            else:
                product_data['reviews_count'] = '0'
        else:
            product_data['reviews_count'] = '0'
        
        # Extrair URL da imagem
        img_element = container.find('img', class_=re.compile(r's-image'))
        if img_element:
            # Tentar pegar src primeiro, depois data-src
            img_url = img_element.get('src') or img_element.get('data-src')
            if img_url:
                product_data['image_url'] = img_url
            else:
                product_data['image_url'] = 'N/A'
        else:
            product_data['image_url'] = 'N/A'
        
        # Extrair preço (opcional)
        price_element = container.find('span', class_=re.compile(r'a-price-whole'))
        if price_element:
            product_data['price'] = price_element.get_text(strip=True)
        else:
            product_data['price'] = 'N/A'
        
        return product_data
    
    def scrape_products(self, keyword, max_products=20):
        """
        Função principal para fazer scraping de produtos da Amazon
        
        Args:
            keyword (str): Palavra-chave para pesquisar
            max_products (int): Número máximo de produtos para retornar
            
        Returns:
            dict: Resultado do scraping com produtos e metadados
        """
        try:
            print(f"Iniciando scraping para palavra-chave: {keyword}")
            
            # Construir URL de pesquisa
            search_url = self.build_search_url(keyword)
            print(f"URL de pesquisa: {search_url}")
            
            # Obter conteúdo da página
            html_content = self.fetch_page_content(search_url)
            
            if not html_content:
                return {
                    'success': False,
                    'error': 'Não foi possível obter o conteúdo da página',
                    'products': []
                }
            
            # Extrair dados dos produtos
            products = self.extract_product_data(html_content)
            
            # Limitar número de produtos se necessário
            if len(products) > max_products:
                products = products[:max_products]
            
            return {
                'success': True,
                'keyword': keyword,
                'total_products': len(products),
                'products': products,
                'search_url': search_url
            }
            
        except Exception as e:
            print(f"Erro geral no scraping: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'products': []
            }


# Função de conveniência para uso direto
def scrape_amazon_products(keyword, max_products=20):
    """
    Função de conveniência para fazer scraping de produtos da Amazon
    
    Args:
        keyword (str): Palavra-chave para pesquisar
        max_products (int): Número máximo de produtos para retornar
        
    Returns:
        dict: Resultado do scraping
    """
    scraper = AmazonScraper()
    return scraper.scrape_products(keyword, max_products)


# Teste da funcionalidade (apenas para desenvolvimento)
if __name__ == "__main__":
    # Teste básico
    result = scrape_amazon_products("notebook", 5)
    print(f"Resultado: {result}")

