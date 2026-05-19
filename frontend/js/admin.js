const API_URL = "http://localhost:5002/admin/stats";
const API_PRODUTOS = "http://localhost:5002/admin/produtos";

const modal = document.getElementById("modalLanche");
const formLanche = document.getElementById("formLanche");

async function carregarDadosDashboard() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error("Erro ao buscar dados do servidor");

        const dados = await response.json();
        const cards = document.querySelectorAll('.card p');

        cards[0].innerText = `R$ ${dados.faturamento.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;
        cards[1].innerText = dados.colaboradores;
        cards[2].innerText = dados.top_lanches[0]?.nome || "Nenhum";

    } catch (error) {
        console.error("Erro no Dashboard:", error);
    }
}

async function carregarProdutos() {
    try {
        const response = await fetch(API_PRODUTOS);
        const produtos = await response.json();

        const tabela = document.getElementById("lista-produtos");
        tabela.innerHTML = "";

        const pastasCategorias = {
            '1': 'burgers',
            '2': 'pizza',
            '3': 'vegetariano',
            '4': 'kids'
        };

        produtos.forEach(p => {
            let imageUrl = '';
            const idCategoria = String(p.categoria);
            const nomePasta = pastasCategorias[idCategoria] || 'burgers';

            if (p.imagem && p.imagem.startsWith('http')) {
                imageUrl = p.imagem;
            } else if (p.imagem && p.imagem.startsWith('static/')) {
                imageUrl = `http://localhost:5002/${p.imagem}`;
            } else if (p.imagem) {
                const imagensPadraoNativas = [
                    'burger1.png', 'burger2.png', 'burger3.png', 'burger4.png', 'burger5.png', 'burger6.png',
                    'pizza10.png', 'pizza11.png', 'vegetariano20.png', 'kids30.png', 'default_burger.png'
                ];

                if (!imagensPadraoNativas.includes(p.imagem)) {
                    imageUrl = `../assets/burgers/${p.imagem}`;
                } else {
                    imageUrl = `../assets/${nomePasta}/${p.imagem}`;
                }
            } else {
                imageUrl = '../assets/burgers/burger1.png';
            }

            tabela.innerHTML += `
            <tr>
                <td>#${p.id}</td>
                <td>
                    <img src="${imageUrl}" width="40" height="40" 
                        style="border-radius: 5px; object-fit: cover;" 
                        onerror="this.onerror=null; this.src='../assets/burgers/burger1.png'">
                </td>
                <td>${p.nome}</td>
                <td>R$ ${Number(p.preco).toFixed(2)}</td>
                <td>
                    <button class="btn-edit" onclick="editar(${p.id})">
                        <i class="fa-solid fa-pen"></i>
                    </button>
                    <button class="btn-delete" onclick="excluir(${p.id})">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
        });
    } catch (erro) {
        console.error("Erro ao carregar produtos:", erro);
    }
}

function abrirModal(lanche = null) {
    modal.style.display = "block";
    formLanche.reset();
    document.getElementById("lancheId").value = "";

    if (lanche) {
        document.getElementById("modalTitle").innerText = "Editar Lanche";
        document.getElementById("lancheId").value = lanche.id;
        document.getElementById("lancheNome").value = lanche.nome;
        document.getElementById("lancheDescricao").value = lanche.descricao;
        document.getElementById("lanchePreco").value = lanche.preco;

        const idCategoria = lanche.categoria ? String(lanche.categoria) : "1";
        document.getElementById("lancheCategoria").value = idCategoria;

    } else {
        document.getElementById("modalTitle").innerText = "Novo Produto";
        document.getElementById("lancheCategoria").value = "1";
    }
}

function fecharModal() {
    modal.style.display = "none";
}

async function editar(id) {
    try {
        const response = await fetch(`${API_PRODUTOS}/${id}`);
        if (!response.ok) throw new Error();
        const lanche = await response.json();
        abrirModal(lanche);
    } catch (error) {
        alert("Erro ao buscar dados do lanche. Verifique se a rota GET está correta no Flask.");
    }
}

formLanche.onsubmit = async (e) => {
    e.preventDefault();

    const id = document.getElementById("lancheId").value;
    const formData = new FormData();

    formData.append("nome", document.getElementById("lancheNome").value);
    formData.append("descricao", document.getElementById("lancheDescricao").value);
    formData.append("preco", document.getElementById("lanchePreco").value);
    formData.append("categoria", document.getElementById("lancheCategoria").value);

    const inputImagem = document.getElementById("lancheImagem");
    if (inputImagem.files[0]) {
        formData.append("imagem", inputImagem.files[0]);
    }

    const url = id ? `${API_PRODUTOS}/${id}` : API_PRODUTOS;
    const metodo = id ? "PUT" : "POST";

    try {
        const response = await fetch(url, {
            method: metodo,
            body: formData
        });

        if (response.ok) {
            alert(id ? "Lanche atualizado!" : "Lanche criado!");
            fecharModal();
            carregarProdutos();
            carregarDadosDashboard();
        } else {
            const erroData = await response.json();
            alert(`Erro: ${erroData.erro || erroData.Erro || "Erro ao salvar"}`);
        }
    } catch (error) {
        alert("Falha na comunicação com o servidor.");
    }
};

async function excluir(id) {
    if (!confirm(`Deseja excluir o lanche #${id}?`)) return;

    try {
        const response = await fetch(`${API_PRODUTOS}/${id}`, { method: 'DELETE' });
        if (response.ok) {
            alert("Lanche removido!");
            carregarProdutos();
        }
    } catch (error) {
        console.error("Erro na deleção:", error);
    }
}

window.onclick = (event) => { if (event.target == modal) fecharModal(); };

window.onload = () => {
    carregarDadosDashboard();
    carregarProdutos();
};