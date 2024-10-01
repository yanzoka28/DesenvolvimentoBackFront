import psycopg2

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
    
    cur.execute(f"SELECT count(*) FROM Produto WHERE loginUser = '{loginUser}'" )
    recset = cur.fetchall()
    
    QtdeProduto = recset[0][0]
    
    if tipoUser == "normal" and QtdeProduto >= 3:
        print("Limite de produtos atingido em usuarios Normais")
        conexao.close()
        return False 
    else:
    
        cur.execute(f"INSERT INTO Produto (nome, qtde, preco, loginuser) VALUES ('{nome}', '{qtde}', '{preco}', '{loginUser}')")
        conexao.commit()
        conexao.close()
        return True

 
 
 
    
#    cur.execute(f"SELECT tipoUser FROM Usuario WHERE loginUser = '{loginUser}'")
#   recset = cur.fetchall()
    
    
    
    