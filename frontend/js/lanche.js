let todosOsLanches = [];

document.addEventListener('DOMContentLoaded', () => {
    buscarLanches();
});

async function buscarLanches() {
    const urlAPI = 'http://localhost:5002/api/lanche';
    try {
        const response = await fetch(urlAPI);

        if (!response.ok) {
            throw new Error(`Erro na rede: ${response.statusText}`);
        }
        todosOsLanches = await response.json();
        console.log('Dados recebidos da API:', todosOsLanches);
        
        filtrarPorCategoria(1);

    } catch (error) {
        console.error('Ocorreu um erro ao buscar os lanches:', error);
        const container = document.getElementById('lista-lanches');
        if (container) {
            container.innerHTML = "<p>Desculpe, não foi possível carregar o cardápio. Tente novamente mais tarde.</p>";
        }
    }
}

function filtrarPorCategoria(categoriaDesejada) {
    const deParaCategorias = {
        '1': 'burgers',
        '2': 'pizza',
        '3': 'vegetariano',
        '4': 'kids',
        'burgers': '1',
        'pizza': '2',
        'vegetariano': '3',
        'kids': '4'
    };

    const lanchesFiltrados = todosOsLanches.filter(lanche => {
        if (!lanche.categoria) return false;

        const categoriaLancheStr = String(lanche.categoria).toLowerCase();
        const buscaStr = String(categoriaDesejada).toLowerCase();

        return categoriaLancheStr === buscaStr || deParaCategorias[categoriaLancheStr] === buscaStr;
    });

    exibirLanchesNaPagina(lanchesFiltrados, categoriaDesejada);
}

function exibirLanchesNaPagina(lanches, categoriaAtual) {
    const container = document.getElementById('lista-lanches');
    if (!container) return;
    container.innerHTML = '';

    if (lanches.length === 0) {
        container.innerHTML = '<p style="color:white; text-align:center;">Nenhum item encontrado.</p>';
        return;
    }

    const nomesFormatados = {
        '1': 'Burgers',
        '2': 'Pizza',
        '3': 'Vegetariano',
        '4': 'Kids'
    };

    lanches.forEach(lanche => {
        let imageUrl = '';
        const idCategoria = lanche.categoria;
        const nomePasta = nomesFormatados[idCategoria] ? nomesFormatados[idCategoria].toLowerCase() : 'burgers';

        if (lanche.imagem && lanche.imagem.startsWith('http')) {
            imageUrl = lanche.imagem;
        } else if (lanche.imagem && lanche.imagem.startsWith('static/')) {
            imageUrl = `http://localhost:5002/${lanche.imagem}`;
        } else if (lanche.imagem) {
            const imagensPadraoNativas = [
                'burger1.png', 'burger2.png', 'burger3.png', 'burger4.png', 'burger5.png', 'burger6.png',
                'pizza10.png', 'pizza11.png', 'vegetariano20.png', 'kids30.png', 'default_burger.png'
            ];

            if (!imagensPadraoNativas.includes(lanche.imagem)) {
                imageUrl = `../assets/burgers/${lanche.imagem}`;
            } else {
                imageUrl = `../assets/${nomePasta}/${lanche.imagem}`;
            }
        } else {
            imageUrl = '../assets/burgers/burger1.png'; 
        }

        const descReal = lanche.descricao || "";
        const descParaOnclick = descReal.replace(/\r?\n|\r/g, ' ').replace(/'/g, "\\'");
        const nomeCategoriaExibição = nomesFormatados[idCategoria] || 'Burgers';

        const cardHTML = `
            <a href="#" class="product-item" 
                onclick="selecionarLanche('${lanche.nome}', '${imageUrl}', '${lanche.preco}', '${descParaOnclick}')"> 
                <div class="photo">
                    <img src="${imageUrl}" alt="${lanche.nome}" onerror="this.onerror=null; this.src='../assets/burgers/burger1.png'"/>
                </div>
                <div class="info">
                    <div class="product-category">${nomeCategoriaExibição}</div>
                    <div class="product-name">${lanche.nome}</div>
                    <div class="product-description">${descReal}</div> 
                    <div class="product-price">${Number(lanche.preco).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</div>
                </div>
            </a>
        `;
        container.insertAdjacentHTML('beforeend', cardHTML);
    });
}

function selecionarLanche(nome, imagemUrl, preco, descricao) {
    const lancheSelecionado = {
        nome: nome,
        imagem: imagemUrl,
        preco: preco,
        descricao: descricao
    };

    localStorage.setItem('lancheParaPersonalizar', JSON.stringify(lancheSelecionado));
    window.location.href = '/frontend/pages/personalizacao.html';
}