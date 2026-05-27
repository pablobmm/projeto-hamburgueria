function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault(); 
    
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const loginBtn = document.getElementById('loginBtn');
    
    if (!email || !password) {
        showToast('Erro', 'Por favor, preencha todos os campos');
        return;
    }
    
    if (!validateEmail(email)) {
        showToast('Erro', 'Por favor, insira um email válido');
        return;
    }
    
    loginBtn.textContent = 'Entrando...';
    loginBtn.classList.add('loading');
    loginBtn.disabled = true;
    
    fetch('https://code-burger-api.onrender.com/login', { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, senha: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.usuario) { 
            localStorage.setItem('usuarioLogado', JSON.stringify(data.usuario));
            
            showToast('Login realizado!', `Bem-vindo, ${data.usuario.nome}`);
            
            setTimeout(() => { 
                window.location.href = '/'; 
            }, 1500);
        } else {
            showToast('Erro de Login', data.erro || 'Credenciais inválidas');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        showToast('Erro de Conexão', 'Não foi possível conectar ao servidor.');
    })
    .finally(() => {
        loginBtn.textContent = 'Entrar';
        loginBtn.classList.remove('loading');
        loginBtn.disabled = false;
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const emailInput = document.getElementById('email');
    const passInput = document.getElementById('password');

    if(emailInput) emailInput.focus();

    emailInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            passInput.focus();
        }
    });
});