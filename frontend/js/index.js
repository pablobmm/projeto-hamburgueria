document.addEventListener("DOMContentLoaded", () => {
  // LÓGICA DE EXIBIÇÃO DO USUÁRIO 
  const usuarioData = localStorage.getItem("usuarioLogado");
  const navContainer = document.querySelector("nav .container") || document.querySelector("nav");

  if (usuarioData) {
    const usuario = JSON.parse(usuarioData);

    // Localiza os botões de Login e Cadastro para remover
    const loginBtn = document.querySelector('a[href="login.html"]');
    const cadastroBtn = document.querySelector('a[href="cadastro.html"]');

    if (loginBtn) loginBtn.parentElement.remove();
    if (cadastroBtn) cadastroBtn.parentElement.remove();

    // Cria a área do perfil do usuário
    const userArea = document.createElement("div");
    userArea.className = "rightside user-profile";
    userArea.innerHTML = `
    <span style="color: white; margin-right: 15px;">
      Olá, <a href="perfil.html" style="color: white; text-decoration: underline;"><strong>${usuario.nome.split(' ')[0]}</strong></a>
    </span>
    <a href="#" id="logout-btn" title="Sair" style="color: #ef4444; font-size: 1.2rem;">
      <i class="fa-solid fa-right-from-bracket"></i>
    </a>
    `;

    navContainer.appendChild(userArea);

    // Lógica de Logout
    document.getElementById("logout-btn").addEventListener("click", (e) => {
      e.preventDefault();
      localStorage.removeItem("usuarioLogado");
      window.location.reload();
    });
  }

  // LÓGICA DE BUSCA(FILTRO)
  const inputSearch = document.getElementById("search");

  if (inputSearch) {
    inputSearch.addEventListener("input", function () {
      const valorBusca = inputSearch.value.toLowerCase().trim();
      const produtos = document.querySelectorAll(".product-item");

      produtos.forEach((produto) => {
        const nomeEl = produto.querySelector(".product-name");
        const nome = nomeEl ? nomeEl.textContent.toLowerCase() : "";

        // Se o nome incluir o que foi digitado, mostra, senão esconde
        if (valorBusca === "" || nome.includes(valorBusca)) {
          produto.style.display = "block";
        } else {
          produto.style.display = "none";
        }
      });
    });
  }

  const btnMenu = document.getElementById('btn-menu');
    const navMenu = document.getElementById('nav-menu');

    if (btnMenu && navMenu) {
        btnMenu.addEventListener('click', () => {
            // Liga/Desliga a classe 'active' que mostra o menu no CSS
            navMenu.classList.toggle('active');
            
            // Opcional: Animação simples transformando os três riscos em um 'X'
            btnMenu.classList.toggle('toggle-icon');
        });
    }
});