document.addEventListener("ContentLoaded", function() {
    fetch('/listarProdutos')
        .then(response => response.json())
        .then(produtos => {
            const tabela = document.getElementById('tabelaProdutos');
            produtos.forEach(produto => {
                const linha = tabela.insertRow();
                const celId = linha.insertCell(0);
                const celNome = linha.insertCell(1);
                const celQtde = linha.insertCell(2);
                const celPreco = linha.insertCell(3);
                celId.textContent = produto.id;
                celNome.textContent = produto.nome;
                celQtde.textContent = produto.qtde;
                celPreco.textContent = produto.preco;
            });
        })
        .catch(error => console.error('Erro ao carregar os produtos:', error));
});
