import psycopg2

def conectardb():
    connect = psycopg2.connect(
        database="postgrestestenuvem",
        host="dpg-crl0c63qf0us73cme9gg-a.oregon-postgres.render.com",
        user='postgrestestenuvem_user',
        password="Iw53PfATFfL6IgfT87azg66xEUzMbGVD"
        
        
        
       # database='AtividadeAvaliativaBackFront',
       # host='localhost',
       # user='postgres',
       # password='1234',
       # port= '5432'
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
    

    
    

    
    
    
    