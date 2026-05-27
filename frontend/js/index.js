document.addEventListener("DOMContentLoaded", () => {
  // LÓGICA DE EXIBIÇÃO DO USUÁRIO 
  const usuarioData = localStorage.getItem("usuarioLogado");
  const navContainer = document.querySelector("nav .container") || document.querySelector("nav");

  if (usuarioData) {
    const usuario = JSON.parse(usuarioData);

    const loginBtn = document.querySelector('a[href*="login.html"]');
    const cadastroBtn = document.querySelector('a[href*="cadastro.html"]');

    if (loginBtn) loginBtn.closest('.rightside').remove();
    if (cadastroBtn) cadastroBtn.closest('.rightside').remove();

    const userArea = document.createElement("div");
    const isMobile = window.innerWidth <= 820;
    userArea.className = isMobile ? "user-profile-mobile" : "rightside user-profile"; 
    
    userArea.innerHTML = `
    <span style="color: white;">
      Olá, <a href="../pages/perfil.html" style="color: white; text-decoration: underline;"><strong>${usuario.nome.split(' ')[0]}</strong></a>
    </span>
    <a href="#" id="logout-btn" title="Sair" style="color: #ef4444; font-size: 1.2rem; margin-left: 10px;">
      <i class="fa-solid fa-right-from-bracket"></i>
    </a>
    `;

    if (isMobile) {
        const navMenu = document.getElementById("nav-menu");
        if (navMenu) {
            navMenu.insertBefore(userArea, navMenu.firstChild);
        }
    } else {
        const headerContainer = document.querySelector("header .container");
        if (headerContainer) {
            headerContainer.appendChild(userArea);
        }
    }

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