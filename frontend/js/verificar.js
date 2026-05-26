document.addEventListener('DOMContentLoaded', () => {
    const verifyBtn = document.getElementById('verifyBtn');
    const otpInput = document.getElementById('otp-input');

    const urlParams = new URLSearchParams(window.location.search);
    const emailRaw = urlParams.get('email');
    
    // Traduz e remove qualquer espaço acidental
    const email = emailRaw ? decodeURIComponent(emailRaw).trim().toLowerCase() : null;

    console.log("Tentando validar o e-mail:", email);

    if (!email) {
        showToast('Erro', 'Email não identificado na URL.');
        return;
    }

    verifyBtn.addEventListener('click', async () => {
        // Pega o valor, remove espaços e garante que é string
        const codigoDigitado = otpInput.value.replace(/\s+/g, '').trim();

        console.log("Código que está sendo enviado:", codigoDigitado);

        verifyBtn.textContent = 'Verificando...';
        verifyBtn.disabled = true;

        try {
            const response = await fetch('https://code-burger-api.onrender.com/usuario/verificar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    email: email, 
                    codigo: codigoDigitado 
                })
            });

            const data = await response.json();
            console.log("Resposta do Servidor:", data);

            if (response.ok) {
                showToast('Sucesso!', 'Conta ativada!');
                setTimeout(() => window.location.href = 'login.html', 2000);
            } else {
                showToast('Erro', data.erro || 'Código inválido.');
                verifyBtn.textContent = 'Verificar Conta';
                verifyBtn.disabled = false;
            }
        } catch (error) {
            console.error("Erro Crítico no Fetch:", error);
            showToast('Erro', 'Falha na conexão com o servidor.');
            verifyBtn.disabled = false;
        }
    });


    async function reenviarToken() { 
        const urlParams = new URLSearchParams(window.location.search);
        const email = urlParams.get('email');

        try {
            const res = await fetch('https://code-burger-api.onrender.com/usuario/reenviar-codigo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email })
            });
            const data = await res.json();
            alert(data.mensagem || data.erro);
        } catch (err) {
            console.error("Erro ao reenviar:", err);
        }
    }

    window.reenviarToken = reenviarToken;

});