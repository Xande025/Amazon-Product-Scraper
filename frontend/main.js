import './style.css'

/**
 * Amazon Product Scraper - Frontend JavaScript
 * Este arquivo contém toda a lógica de interação com o usuário e comunicação com a API
 */

// Configuração da API
const API_CONFIG = {
  // URL base da API - será ajustada automaticamente para desenvolvimento ou produção
  baseUrl: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:5001/api' 
    : '/api',
  
  // Timeout para requisições (em milissegundos)
  timeout: 30000
}

// Elementos DOM que serão utilizados
const elements = {
  searchForm: null,
  keywordInput: null,
  maxProductsSelect: null,
  searchBtn: null,
  loadingSection: null,
  resultsSection: null,
  errorSection: null,
  productsGrid: null,
  resultsCount: null,
  executionTime: null,
  errorMessage: null,
  retryBtn: null
}

/**
 * Inicializa a aplicação quando o DOM estiver carregado
 */
document.addEventListener('DOMContentLoaded', function() {
  console.log('🚀 Amazon Product Scraper iniciado')
  
  // Obter referências dos elementos DOM
  initializeElements()
  
  // Configurar event listeners
  setupEventListeners()
  
  // Verificar se a API está funcionando
  checkApiHealth()
})

/**
 * Obtém referências para todos os elementos DOM necessários
 */
function initializeElements() {
  elements.searchForm = document.getElementById('searchForm')
  elements.keywordInput = document.getElementById('keyword')
  elements.maxProductsSelect = document.getElementById('maxProducts')
  elements.searchBtn = document.getElementById('searchBtn')
  elements.loadingSection = document.getElementById('loadingSection')
  elements.resultsSection = document.getElementById('resultsSection')
  elements.errorSection = document.getElementById('errorSection')
  elements.productsGrid = document.getElementById('productsGrid')
  elements.resultsCount = document.getElementById('resultsCount')
  elements.executionTime = document.getElementById('executionTime')
  elements.errorMessage = document.getElementById('errorMessage')
  elements.retryBtn = document.getElementById('retryBtn')
  
  // Verificar se todos os elementos foram encontrados
  const missingElements = Object.entries(elements)
    .filter(([key, element]) => !element)
    .map(([key]) => key)
  
  if (missingElements.length > 0) {
    console.error('❌ Elementos DOM não encontrados:', missingElements)
  } else {
    console.log('✅ Todos os elementos DOM foram encontrados')
  }
}

/**
 * Configura todos os event listeners da aplicação
 */
function setupEventListeners() {
  // Event listener para o formulário de pesquisa
  if (elements.searchForm) {
    elements.searchForm.addEventListener('submit', handleSearchSubmit)
  }
  
  // Event listener para o botão de tentar novamente
  if (elements.retryBtn) {
    elements.retryBtn.addEventListener('click', handleRetryClick)
  }
  
  // Event listener para tecla Enter no campo de pesquisa
  if (elements.keywordInput) {
    elements.keywordInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault()
        handleSearchSubmit(e)
      }
    })
  }
  
  console.log('✅ Event listeners configurados')
}

/**
 * Verifica se a API está funcionando
 */
async function checkApiHealth() {
  try {
    console.log('🔍 Verificando saúde da API...')
    
    const response = await fetch(`${API_CONFIG.baseUrl}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      signal: AbortSignal.timeout(5000) // Timeout de 5 segundos para health check
    })
    
    if (response.ok) {
      const data = await response.json()
      console.log('✅ API está funcionando:', data)
    } else {
      console.warn('⚠️ API respondeu com status:', response.status)
    }
  } catch (error) {
    console.warn('⚠️ Não foi possível verificar a API:', error.message)
  }
}

/**
 * Manipula o envio do formulário de pesquisa
 */
async function handleSearchSubmit(event) {
  event.preventDefault()
  
  // Obter valores do formulário
  const keyword = elements.keywordInput.value.trim()
  const maxProducts = parseInt(elements.maxProductsSelect.value)
  
  // Validar entrada
  if (!keyword) {
    showError('Por favor, digite uma palavra-chave para pesquisar.')
    elements.keywordInput.focus()
    return
  }
  
  // Iniciar pesquisa
  await performSearch(keyword, maxProducts)
}

/**
 * Manipula o clique no botão de tentar novamente
 */
function handleRetryClick() {
  const keyword = elements.keywordInput.value.trim()
  const maxProducts = parseInt(elements.maxProductsSelect.value)
  
  if (keyword) {
    performSearch(keyword, maxProducts)
  }
}

/**
 * Executa a pesquisa de produtos
 */
async function performSearch(keyword, maxProducts) {
  try {
    console.log(`🔍 Iniciando pesquisa: "${keyword}" (max: ${maxProducts})`)
    
    // Mostrar estado de carregamento
    showLoading()
    
    // Fazer requisição para a API
    const response = await fetch(
      `${API_CONFIG.baseUrl}/scrape?keyword=${encodeURIComponent(keyword)}&max_products=${maxProducts}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        signal: AbortSignal.timeout(API_CONFIG.timeout)
      }
    )
    
    // Verificar se a resposta foi bem-sucedida
    if (!response.ok) {
      throw new Error(`Erro HTTP: ${response.status} - ${response.statusText}`)
    }
    
    // Processar resposta JSON
    const data = await response.json()
    
    // Verificar se o scraping foi bem-sucedido
    if (data.success) {
      console.log('✅ Pesquisa concluída com sucesso:', data)
      showResults(data)
    } else {
      throw new Error(data.error || 'Erro desconhecido no scraping')
    }
    
  } catch (error) {
    console.error('❌ Erro na pesquisa:', error)
    
    // Determinar mensagem de erro apropriada
    let errorMessage = 'Ocorreu um erro durante a pesquisa. '
    
    if (error.name === 'AbortError') {
      errorMessage += 'A pesquisa demorou muito para responder. Tente novamente.'
    } else if (error.message.includes('Failed to fetch')) {
      errorMessage += 'Não foi possível conectar com o servidor. Verifique sua conexão.'
    } else {
      errorMessage += error.message
    }
    
    showError(errorMessage)
  }
}

/**
 * Mostra o estado de carregamento
 */
function showLoading() {
  // Esconder outras seções
  hideAllSections()
  
  // Mostrar seção de carregamento
  elements.loadingSection.classList.remove('hidden')
  
  // Desabilitar botão de pesquisa
  elements.searchBtn.disabled = true
  elements.searchBtn.classList.add('loading')
  
  console.log('⏳ Mostrando estado de carregamento')
}

/**
 * Mostra os resultados da pesquisa
 */
function showResults(data) {
  // Esconder outras seções
  hideAllSections()
  
  // Atualizar informações dos resultados
  elements.resultsCount.textContent = `${data.total_products} produtos encontrados`
  elements.executionTime.textContent = `Tempo: ${data.execution_time}s`
  
  // Limpar grid de produtos
  elements.productsGrid.innerHTML = ''
  
  // Adicionar produtos ao grid
  if (data.products && data.products.length > 0) {
    data.products.forEach((product, index) => {
      const productCard = createProductCard(product, index)
      elements.productsGrid.appendChild(productCard)
    })
  } else {
    // Mostrar mensagem quando não há produtos
    elements.productsGrid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 2rem;">
        <i class="fas fa-search" style="font-size: 3rem; color: #6c757d; margin-bottom: 1rem;"></i>
        <h3>Nenhum produto encontrado</h3>
        <p>Tente usar uma palavra-chave diferente.</p>
      </div>
    `
  }
  
  // Mostrar seção de resultados
  elements.resultsSection.classList.remove('hidden')
  
  // Reabilitar botão de pesquisa
  elements.searchBtn.disabled = false
  elements.searchBtn.classList.remove('loading')
  
  console.log(`✅ Mostrando ${data.total_products} produtos`)
}

/**
 * Cria um card de produto
 */
function createProductCard(product, index) {
  const card = document.createElement('div')
  card.className = 'product-card'
  card.style.animationDelay = `${index * 0.1}s`
  
  // Processar dados do produto
  const title = product.title || 'Título não disponível'
  const rating = product.rating !== 'N/A' ? parseFloat(product.rating) : null
  const reviewsCount = product.reviews_count || '0'
  const imageUrl = product.image_url !== 'N/A' ? product.image_url : '/placeholder-image.png'
  const price = product.price !== 'N/A' ? `R$ ${product.price}` : 'Preço não disponível'
  
  // Gerar estrelas para avaliação
  const starsHtml = rating ? generateStarsHtml(rating) : '<span class="rating-text">Sem avaliação</span>'
  
  card.innerHTML = `
    <img 
      src="${imageUrl}" 
      alt="${title}" 
      class="product-image"
      onerror="this.src='/placeholder-image.png'"
    />
    <h3 class="product-title">${title}</h3>
    <div class="product-info">
      <div class="product-rating">
        ${starsHtml}
        ${rating ? `<span class="rating-text">(${rating})</span>` : ''}
      </div>
      <div class="product-reviews">
        <i class="fas fa-comment"></i>
        ${formatNumber(reviewsCount)} avaliações
      </div>
      <div class="product-price">${price}</div>
    </div>
  `
  
  return card
}

/**
 * Gera HTML das estrelas para avaliação
 */
function generateStarsHtml(rating) {
  const fullStars = Math.floor(rating)
  const hasHalfStar = rating % 1 >= 0.5
  const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0)
  
  let starsHtml = '<div class="stars">'
  
  // Estrelas cheias
  for (let i = 0; i < fullStars; i++) {
    starsHtml += '<i class="fas fa-star"></i>'
  }
  
  // Meia estrela
  if (hasHalfStar) {
    starsHtml += '<i class="fas fa-star-half-alt"></i>'
  }
  
  // Estrelas vazias
  for (let i = 0; i < emptyStars; i++) {
    starsHtml += '<i class="far fa-star"></i>'
  }
  
  starsHtml += '</div>'
  return starsHtml
}

/**
 * Formata números para exibição
 */
function formatNumber(num) {
  const number = parseInt(num.toString().replace(/\D/g, ''))
  
  if (number >= 1000000) {
    return (number / 1000000).toFixed(1) + 'M'
  } else if (number >= 1000) {
    return (number / 1000).toFixed(1) + 'K'
  } else {
    return number.toString()
  }
}

/**
 * Mostra mensagem de erro
 */
function showError(message) {
  // Esconder outras seções
  hideAllSections()
  
  // Atualizar mensagem de erro
  elements.errorMessage.textContent = message
  
  // Mostrar seção de erro
  elements.errorSection.classList.remove('hidden')
  
  // Reabilitar botão de pesquisa
  elements.searchBtn.disabled = false
  elements.searchBtn.classList.remove('loading')
  
  console.error('❌ Mostrando erro:', message)
}

/**
 * Esconde todas as seções de conteúdo
 */
function hideAllSections() {
  elements.loadingSection.classList.add('hidden')
  elements.resultsSection.classList.add('hidden')
  elements.errorSection.classList.add('hidden')
}

// Exportar funções para uso em testes (se necessário)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    performSearch,
    createProductCard,
    generateStarsHtml,
    formatNumber
  }
}

