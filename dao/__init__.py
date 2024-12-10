import psycopg2
import pandas as pd
from psycopg2.extras import DictCursor

def conectardb():
    connect = psycopg2.connect(
        
       # database="postgrestestenuvem",
       # host="dpg-crl0c63qf0us73cme9gg-a.oregon-postgres.render.com",
       # user='postgrestestenuvem_user',
       # password="Iw53PfATFfL6IgfT87azg66xEUzMbGVD"
        
        database='AtividadeAvaliativaBackFront',
        host='localhost',
        user='postgres',
        password='1234',
        port= '5432'
        
    ) 
    return connect


def verificarLogin(loginUser, senha):
    conexao = conectardb()
    cur = conexao.cursor()
    
    cur.execute(f"SELECT count(*) FROM Usuario WHERE loginUser = '{loginUser}' AND senha = '{senha}'")
    recset = cur.fetchall()
    conexao.close()
    
    if recset[0][0] == 1:
        return True
    else:
        return False
    
    
def cadastroUsuario(loginUser, senha, tipoUser):
    conexao = conectardb()
    cur = conexao.cursor()
    
    cur.execute(f"SELECT count(*) FROM Usuario WHERE loginUser = '{loginUser}'")
    recset = cur.fetchall()
    
    if recset[0][0] == 0:
        cur.execute(f"INSERT INTO Usuario VALUES('{loginUser}', '{senha}', '{tipoUser}')")
        conexao.commit()
        conexao.close()
        return True
    else:
        conexao.close()
        return False
    
def cadastroProduto(loginUser, tipoUser, nome, qtde, preco):
    conexao = conectardb()
    cur = conexao.cursor()
    
    cur.execute(f"SELECT count(*) FROM Produtos WHERE loginUser = '{loginUser}'" )
    recset = cur.fetchall()
  
    
    QtdeProduto = recset[0][0]
    print("ate aqui okay")
    if tipoUser == "normal" and QtdeProduto >= 3:
        print("Limite de produtos atingido em usuarios Normais")
        conexao.close()
        print("2")
        return False 
    
    else:
        cur.execute(f"INSERT INTO Produtos (nome, qtde, preco, loginuser, datavenda) VALUES ('{nome}', '{qtde}', '{preco}', '{loginUser}', NOW())") 
        conexao.commit()
        conexao.close()
        print("entrou")
        return True

 
def lista_produtos(loginUser):
    conexao = conectardb()

    cur = conexao.cursor(cursor_factory=DictCursor)
    
    try:
        cur.execute(f"SELECT nome, qtde, preco FROM Produtos WHERE loginuser = ('{loginUser}')")
        produtos = cur.fetchall()

        if not produtos:
            return []

        return [dict(produto) for produto in produtos]
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return []
    finally:
        conexao.close()
        
def listar_vendas(nome_produto): 
    
    try:
        conexao = conectardb() 
        cur = conexao.cursor() 
        if nome_produto: 
            cur.execute(f"SELECT dataVenda, nome, qtde, preco FROM Produtos WHERE nome = ('{nome_produto}')") 
        else: 
            cur.execute("SELECT dataVenda, nome, qtde, preco FROM Produtos") 
            
        vendas = cur.fetchall() 
        conexao.close() 
        
        df = pd.DataFrame(vendas, columns=['dataVenda', 'nome_produto', 'quantidade', 'preco']) 
        return df
    except Exception as e:
        print(e)
        return None
    
def findByID(id):
    try:
        conexao = conectardb()
        cur = conexao.cursor()
        cur.execute(f"SELECT * FROM Produtos WHERE id = '{id}'")
        recset = cur.fetchall()
        conexao.close()
        
        return recset   
    except Exception as e:
        print(e)
        return None
    
def findByName(nome):
    try:
        conexao = conectardb()
        cur = conexao.cursor()
        cur.execute(f"SELECT * FROM Produtos WHERE nome = '{nome}'")
        recset = cur.fetchall()
        conexao.close()
        
        return recset
    except Exception as e:
        print (e)
        return None

def buscar_pessoa(login):
    conexao = conectardb()
    cur = conexao.cursor()
    cur.execute(f"SELECT * FROM usuario where login= '{login}' ")
    recset = cur.fetchall()
    conexao.close()

    return recset