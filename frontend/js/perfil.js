document.addEventListener("DOMContentLoaded", () => {
    const usuarioData = localStorage.getItem("usuarioLogado");
    if (!usuarioData) {
        window.location.href = "../pages/login.html";
        return;
    }

    const usuario = JSON.parse(usuarioData);
    const form = document.getElementById("editProfileForm");

    document.getElementById("editNome").value = usuario.nome;
    document.getElementById("editEmail").value = usuario.email;
    document.getElementById("editTelefone").value = usuario.telefone;
    document.getElementById("editEndereco").value = usuario.endereco;


    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const dadosAtualizados = {
            id: usuario.id,
            nome: document.getElementById("editNome").value,
            email: document.getElementById("editEmail").value,
            telefone: document.getElementById("editTelefone").value,
            endereco: document.getElementById("editEndereco").value
        };

        fetch(`https://code-burger-api.onrender.com/usuario/atualizar/${usuario.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dadosAtualizados)
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (data.usuario) {
                    localStorage.setItem('usuarioLogado', JSON.stringify(data.usuario));

                    showToast('Sucesso', data.mensagem);

                    setTimeout(() => {
                        window.location.href = "../index.html";
                    }, 2000);
                } else {
                    showToast('Erro', data.erro);
                }
            });
    });
});