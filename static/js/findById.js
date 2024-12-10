$(document).ready(function(){
    $('#findProductForm').on('submit', function(e){
        e.preventDefault(); // solicitação via AJAX(impede de que a página seja enviada)

        var productId = $('#productId').val();
        console.log("ID do Produto:", productId); 

        $.ajax({//response e request sem carregar a página 
            url: '/findByID',
            type: 'POST',
            data: { id: productId },
            success: function(response) {//requisição AJAX bem sucedida
                console.log("Resposta: ", response);  
                var productDetails = `<h2>Detalhes do Produto</h2>
                                      <p>ID: ${response.id}</p>
                                      <p>Nome: ${response.nome}</p>
                                      <p>Quantidade: ${response.qtde}</p>
                                      <p>Preço: ${response.preco}</p>
                                      <p>Data: ${response.datavenda}</p>`
                $('#productDetails').html(productDetails);
            },
            error: function(xhr) {
                var error = JSON.parse(xhr.responseText).error;
                $('#productDetails').html(`<p style="color: red;">Erro: Produto não encontrado ${error}</p>`);
            }
        });
    });
});
