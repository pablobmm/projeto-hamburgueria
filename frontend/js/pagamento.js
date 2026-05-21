document.addEventListener('DOMContentLoaded', () => {
    const cardNumberInput = document.getElementById('card-number');
    const cardNameInput = document.getElementById('card-name');
    const cardExpiryInput = document.getElementById('card-expiry');
    const cardCvcInput = document.getElementById('card-cvc');
    const submitButton = document.getElementById('submit-payment-btn');

    const total = localStorage.getItem('totalPedido');
    if (total) {
        document.getElementById('summary-subtotal').textContent = Number(total).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
        document.getElementById('summary-total').textContent = Number(total).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    }

    cardNumberInput.addEventListener('input', (e) => { e.target.value = e.target.value.replace(/\D/g, '').replace(/(\d{4})(?=\d)/g, '$1 ').trim(); });
    cardNameInput.addEventListener('input', (e) => { e.target.value = e.target.value.replace(/[^a-zA-Z\sÀ-ÖØ-öø-ÿ']/g, ''); });
    cardExpiryInput.addEventListener('input', (e) => {
        let digits = e.target.value.replace(/\D/g, '');
        let mes = digits.substring(0, 2); let ano = digits.substring(2, 4);
        if (mes.length === 1 && mes[0] > '1') mes = '0' + mes;
        e.target.value = mes + (ano.length > 0 ? '/' + ano : '');
    });
    cardCvcInput.addEventListener('input', (e) => { e.target.value = e.target.value.replace(/\D/g, ''); });


    submitButton.addEventListener('click', async (e) => {
        e.preventDefault();

        const carrinhoRaw = localStorage.getItem('carrinho');
        if (!carrinhoRaw) { alert('Seu carrinho está vazio!'); return; }
        const itensCarrinho = JSON.parse(carrinhoRaw);

        const itensFormatadosBackend = itensCarrinho.map(item => {
            let precoRaw = item.preco || item.preco_unitario || item.valor || "0";
            
            let precoLimpo = typeof precoRaw === 'number' ? precoRaw : 
                String(precoRaw)
                    .replace('R$', '')
                    .replace(/\s/g, '')
                    .replace('.', '')
                    .replace(',', '.');

            return {
                lanche_id: Number(item.id),
                preco: parseFloat(precoLimpo) || 0.0,
                qtd: Number(item.quantidade || item.qtd || 1)
            };
        });

        const totalValidacao = itensFormatadosBackend.reduce((acc, i) => acc + (i.preco * i.qtd), 0);
        if (totalValidacao <= 0) {
            alert('Erro interno: O valor total do carrinho não pôde ser calculado como positivo. Verifique os itens.');
            return;
        }

        submitButton.textContent = 'Processando com Mercado Pago...';
        submitButton.disabled = true;

        try {
            const response = await fetch('http://localhost:5002/pedido/checkout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    usuario_id: 1, 
                    itens: itensFormatadosBackend
                })
            });

            const resultado = await response.json();

            if (response.ok) {
                localStorage.removeItem('carrinho');
                localStorage.removeItem('totalPedido');
                localStorage.removeItem('subtotalPedido');

                alert('Pedido realizado com sucesso via Mercado Pago!');
                window.location.href = resultado.link_pagamento; 
            } else {
                alert(`Erro no Checkout: ${resultado.erro || 'Falha ao processar'}`);
                submitButton.textContent = 'Finalizar Pagamento';
                submitButton.disabled = false;
            }
        } catch (error) {
            console.error("Erro no checkout:", error);
            alert('Não foi possível conectar ao servidor.');
            submitButton.textContent = 'Finalizar Pagamento';
            submitButton.disabled = false;
        }
    });
});