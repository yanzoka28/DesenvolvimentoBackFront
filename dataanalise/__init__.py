import os

import pandas as pd
import plotly.express as px

import dao


def gerarGrafProdutos(nome_produto):

    df = dao.listar_vendas(nome_produto)    


    print(f"ERRO: {df.columns}")
    
    df['dataVenda'] = pd.to_datetime(df["dataVenda"])
    df['mes'] = df['dataVenda'].dt.to_period('M').astype(str)
    
    df_agrupado = df.groupby(['mes', 'nome_produto'])['quantidade'].sum().reset_index()
    dados = df_agrupado.sort_values(by='mes', ascending=False)
    

    fig = px.bar(
        dados,
        x = 'quantidade',
        y = 'mes',
        text='mes',
        color = 'nome_produto',
        barmode="stack",
        title = 'Estoque de Produtos',
        labels = {'mes': 'Mês', 'quantidade': 'Quantidade De Estoque'}
    )
    fig.update_traces(textposition='outside') # Formatando os dados e colocando rótulos
    fig.update_layout(xaxis_tickangle= -45) # Rotacionando o x em -45
   # fig.update_layout(plot_bgcolor='lightgray', paper_bgcolor='pink') # Definindo a cor de fundo do gráfico
    fig.update_layout(bargap=0.2)
    
    fig.add_layout_image(
        
        source="image/rene_na_macha_funebre.png",
        xref="paper", 
        yref="paper",
        x=0.5, 
        y=0.5,  # Posição da imagem (0 a 1, onde 0 é a borda esquerda/baixo e 1 é a borda direita/cima)
        sizex=0.5, 
        sizey=0.5,  # Tamanho da imagem (em proporção ao gráfico)
        xanchor="center", 
        yanchor="middle",
        opacity=1.0,  # Opacidade da imagem
        layer="above"
    
    )
    fig.show()

    return fig.show()
    

    
    





  