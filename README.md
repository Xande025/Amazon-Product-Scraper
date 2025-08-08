# Amazon Product Scraper

Um sistema completo de web scraping para extrair dados de produtos da Amazon, desenvolvido com Flask (backend) e HTML/CSS/JavaScript (frontend).

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Características](#características)
- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Limitações e Considerações](#limitações-e-considerações)
- [Contribuição](#contribuição)
- [Licença](#licença)

## 🎯 Visão Geral

O Amazon Product Scraper é uma aplicação web que permite extrair informações de produtos da Amazon de forma automatizada. O sistema consiste em um backend Flask que realiza o web scraping e uma interface web moderna que permite aos usuários pesquisar produtos e visualizar os resultados de forma organizada.

### Funcionalidades Principais

- **Interface Web Intuitiva**: Interface moderna e responsiva para pesquisa de produtos
- **API RESTful**: Endpoints bem documentados para integração com outras aplicações
- **Extração de Dados**: Coleta título, classificação, número de avaliações, imagens e preços
- **Tratamento de Erros**: Sistema robusto de tratamento de erros e validação
- **Design Responsivo**: Interface adaptável para desktop e dispositivos móveis

## ✨ Características

### Backend (Flask)
- ✅ API RESTful com endpoints documentados
- ✅ Web scraping com BeautifulSoup e requests
- ✅ Tratamento robusto de erros
- ✅ Configuração CORS para integração frontend
- ✅ Validação de parâmetros de entrada
- ✅ Headers personalizados para evitar detecção de bot

### Frontend (HTML/CSS/JavaScript)
- ✅ Interface moderna com design profissional
- ✅ Formulário de pesquisa com validação
- ✅ Exibição de resultados em grid responsivo
- ✅ Estados de carregamento e erro
- ✅ Integração AJAX com o backend
- ✅ Animações e transições suaves

## 🏗️ Arquitetura

```
┌─────────────────┐    HTTP/AJAX    ┌─────────────────┐
│                 │ ──────────────► │                 │
│   Frontend      │                 │   Backend       │
│   (Vite)        │ ◄────────────── │   (Flask)       │
│   Port: 5173    │    JSON API     │   Port: 5001    │
└─────────────────┘                 └─────────────────┘
                                             │
                                             │ HTTP Requests
                                             ▼
                                    ┌─────────────────┐
                                    │                 │
                                    │   Amazon.com    │
                                    │   (Web Scraping)│
                                    └─────────────────┘
```

### Fluxo de Dados

1. **Usuário** insere palavra-chave na interface web
2. **Frontend** envia requisição AJAX para o backend
3. **Backend** processa a requisição e faz scraping da Amazon
4. **Backend** retorna dados estruturados em JSON
5. **Frontend** exibe os resultados de forma organizada

## 📋 Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado:

- **Python 3.8+** - Para o backend Flask
- **Node.js 16+** - Para o frontend Vite
- **pip** - Gerenciador de pacotes Python
- **npm** - Gerenciador de pacotes Node.js

### Verificar Instalações

```bash
# Verificar Python
python3 --version

# Verificar Node.js
node --version

# Verificar npm
npm --version
```

## 🚀 Instalação

### 1. Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd amazon-scraper
```

### 2. Configurar Backend

```bash
# Navegar para o diretório do backend
cd backend

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
# No Linux/Mac:
source venv/bin/activate
# No Windows:
# venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configurar Frontend

```bash
# Navegar para o diretório do frontend
cd ../frontend

# Instalar dependências
npm install
```

## 🎮 Uso

### Executar o Backend

```bash
# No diretório backend/
source venv/bin/activate
python src/main.py
```

O backend estará disponível em: `http://localhost:5001`

### Executar o Frontend

```bash
# No diretório frontend/
npm run dev
```

O frontend estará disponível em: `http://localhost:5173`

### Usar a Aplicação

1. Abra o navegador e acesse `http://localhost:5173`
2. Digite uma palavra-chave no campo de pesquisa (ex: "notebook")
3. Selecione o número máximo de produtos desejado
4. Clique em "Buscar Produtos"
5. Aguarde os resultados serem exibidos

## 🔌 API Endpoints

### Base URL
```
http://localhost:5001/api
```

### Endpoints Disponíveis

#### 1. Health Check
```http
GET /health
```

**Resposta:**
```json
{
  "status": "healthy",
  "service": "Amazon Scraper API",
  "timestamp": 1754662666.9606373
}
```

#### 2. Scraping de Produtos
```http
GET /scrape?keyword={palavra-chave}&max_products={numero}
```

**Parâmetros:**
- `keyword` (obrigatório): Palavra-chave para pesquisar
- `max_products` (opcional): Número máximo de produtos (1-50, padrão: 20)

**Exemplo:**
```http
GET /scrape?keyword=notebook&max_products=10
```

**Resposta de Sucesso:**
```json
{
  "success": true,
  "keyword": "notebook",
  "total_products": 10,
  "execution_time": 2.34,
  "search_url": "https://www.amazon.com.br/s?k=notebook",
  "products": [
    {
      "title": "Notebook Dell Inspiron 15",
      "rating": "4.5",
      "reviews_count": "1234",
      "image_url": "https://...",
      "price": "2499.99"
    }
  ]
}
```

**Resposta de Erro:**
```json
{
  "success": false,
  "error": "Parâmetro 'keyword' é obrigatório",
  "message": "Por favor, forneça uma palavra-chave para pesquisar"
}
```

#### 3. Informações da API
```http
GET /info
```

**Resposta:**
```json
{
  "name": "Amazon Scraper API",
  "version": "1.0.0",
  "description": "API para fazer scraping de produtos da Amazon",
  "endpoints": {
    "/api/scrape": {
      "method": "GET",
      "description": "Faz scraping de produtos da Amazon",
      "parameters": {
        "keyword": "string (obrigatório) - palavra-chave para pesquisar",
        "max_products": "integer (opcional) - número máximo de produtos (1-50, padrão: 20)"
      },
      "example": "/api/scrape?keyword=notebook&max_products=10"
    }
  }
}
```

## 📁 Estrutura do Projeto

```
amazon-scraper/
├── backend/                    # Backend Flask
│   ├── src/
│   │   ├── routes/            # Blueprints da API
│   │   │   ├── scraper.py     # Endpoints de scraping
│   │   │   └── user.py        # Endpoints de usuário (template)
│   │   ├── models/            # Modelos de dados
│   │   ├── static/            # Arquivos estáticos
│   │   ├── database/          # Banco de dados SQLite
│   │   ├── main.py            # Arquivo principal do Flask
│   │   └── scraper.py         # Lógica de web scraping
│   ├── venv/                  # Ambiente virtual Python
│   └── requirements.txt       # Dependências Python
├── frontend/                  # Frontend Vite
│   ├── src/                   # Código fonte (se usando framework)
│   ├── index.html             # Página principal
│   ├── main.js                # JavaScript principal
│   ├── style.css              # Estilos CSS
│   ├── package.json           # Dependências Node.js
│   └── vite.config.js         # Configuração Vite
├── README.md                  # Este arquivo
└── todo.md                    # Lista de tarefas do projeto
```

### Arquivos Principais

#### Backend
- **`src/main.py`**: Ponto de entrada da aplicação Flask
- **`src/scraper.py`**: Classe principal para web scraping da Amazon
- **`src/routes/scraper.py`**: Endpoints da API de scraping
- **`requirements.txt`**: Lista de dependências Python

#### Frontend
- **`index.html`**: Estrutura HTML da aplicação
- **`main.js`**: Lógica JavaScript e integração com API
- **`style.css`**: Estilos CSS responsivos
- **`package.json`**: Configuração e dependências Node.js

## 🛠️ Tecnologias Utilizadas

### Backend
- **[Flask](https://flask.palletsprojects.com/)** - Framework web Python
- **[Flask-CORS](https://flask-cors.readthedocs.io/)** - Suporte a CORS
- **[Requests](https://requests.readthedocs.io/)** - Cliente HTTP
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)** - Parser HTML/XML
- **[lxml](https://lxml.de/)** - Parser XML/HTML rápido

### Frontend
- **[Vite](https://vitejs.dev/)** - Build tool e dev server
- **HTML5** - Estrutura da página
- **CSS3** - Estilos e layout responsivo
- **JavaScript (ES6+)** - Lógica da aplicação
- **[Font Awesome](https://fontawesome.com/)** - Ícones
- **[Google Fonts](https://fonts.google.com/)** - Tipografia

### Ferramentas de Desenvolvimento
- **Python 3.11** - Linguagem do backend
- **Node.js 20** - Runtime JavaScript
- **npm** - Gerenciador de pacotes
- **Git** - Controle de versão

## ⚠️ Limitações e Considerações

### Limitações Técnicas

1. **Proteções Anti-Bot da Amazon**
   - A Amazon implementa várias proteções contra web scraping
   - CAPTCHAs podem ser exibidos para requisições automatizadas
   - Rate limiting pode bloquear muitas requisições consecutivas

2. **Estrutura HTML Dinâmica**
   - A Amazon frequentemente altera a estrutura HTML das páginas
   - Seletores CSS podem precisar de atualizações periódicas
   - Conteúdo carregado via JavaScript pode não ser capturado

3. **Geolocalização**
   - Resultados podem variar baseado na localização do servidor
   - Preços e disponibilidade são específicos por região

### Considerações Legais

1. **Termos de Serviço**
   - Verifique os termos de serviço da Amazon antes do uso
   - Web scraping pode violar os termos de uso de alguns sites

2. **Uso Responsável**
   - Implemente delays entre requisições
   - Respeite o arquivo robots.txt
   - Não sobrecarregue os servidores

3. **Dados Pessoais**
   - Não colete informações pessoais de usuários
   - Respeite a privacidade e proteção de dados

### Melhorias Futuras

1. **Proxy e Rotação de IP**
   - Implementar rotação de proxies
   - Usar serviços de proxy residencial

2. **Cache e Persistência**
   - Implementar cache de resultados
   - Salvar dados em banco de dados

3. **Monitoramento**
   - Logs detalhados de requisições
   - Métricas de performance

4. **Testes Automatizados**
   - Testes unitários para funções de scraping
   - Testes de integração da API

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes de Contribuição

- Mantenha o código limpo e bem documentado
- Adicione testes para novas funcionalidades
- Siga as convenções de código existentes
- Atualize a documentação quando necessário

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique a seção de [Limitações](#limitações-e-considerações)
2. Consulte os logs do backend para erros detalhados
3. Abra uma issue no repositório do projeto

---

**Desenvolvido com ❤️ por [Manus AI](https://manus.ai)**

