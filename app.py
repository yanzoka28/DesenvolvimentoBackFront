from flask import *
import dao
import dataanalise
import os
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)

app.secret_key = "testedechave"


@app.route('/')
def index():
    return render_template('cadastroUsuario.html')

@app.route("/logout")
def logout():
    session.pop("loginUser", None)
    
    return make_response(render_template('cadastroUsuario.html'))


@app.route ("/telaLogin", methods=['POST', 'GET'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        loginUser = request.form.get("login") or None
        senha = request.form.get("senha") or None
        
    if dao.verificarLogin(loginUser, senha):
        session['loginUser'] = loginUser
        print("Login realizado")
        return render_template('cadastroProduto.html')
        
    else:
        print("Login ou Senha incorretos")
        return render_template('login.html')
    
@app.route("/cadastroUsuario", methods=['POST', 'GET'])        
def cadastrarUsuario():
    if request.method == "POST":
        loginUser = request.form.get('login') or None
        senha = request.form.get('senha') or None
        tipoUser = request.form.get("tipoUser") or None
        
    if dao.verificarLogin(loginUser, senha):
        print("Este usuario ja existe")
        return render_template('cadastroUsuario.html')
        
    elif dao.cadastroUsuario(loginUser, senha, tipoUser):
        print("Usuario cadastrado com sucesso")
        session["loginUser"] = loginUser
        session["tipoUser"] = tipoUser
        return render_template('login.html')
    
    else:
        print('nao realizado')
        return render_template('cadastroUsuario.html')    

@app.route('/cadastroProduto', methods=["GET", "POST"])
def cadastrarProduto():
    try:
        if request.method == "GET":
            return render_template("cadastroProduto.html")
            
        if request.method == "POST":
            nome = request.form.get("nome") or None
            qtde = request.form.get("qtde") or None
            preco = request.form.get("preco") or None
            loginUser = session.get("loginUser") or None
            tipoUser = session.get("tipoUser") or None
            
            dao.cadastroProduto(loginUser, tipoUser, nome, qtde, preco)
            print("foi papai")
            return render_template("index.html")
            
    except Exception as e:
        print(e.with_traceback())
        render_template("cadastroProduto.html")

@app.route('/listarProdutos', methods=['GET'])
def listar_produtos():
    try:
        loginUser = session.get("loginUser") or None
        produtos = dao.lista_produtos(loginUser)

        if produtos is None:
            produtos = []

        return render_template('listarProdutos.html', produtos=produtos)
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return render_template('listarProdutos.html', produtos=[])      

@app.route('/findByID', methods=['GET', "POST"])
def findById():
    
    if request.method == "GET":
        return render_template("findByID.html")
    
    try:
        id = request.form.get("id")
        if id is None:
            return abort(400, description="Produto não fornecido")  
        
        produtosFindId = dao.findByID(id)
        print(produtosFindId)
        
        if produtosFindId is None:
            return abort(404, description="Produto não encontrado")       
        
        produtosFindIdDict = {
            "id": produtosFindId[0][0],
            "nome": produtosFindId[0][1],
            "qtde": produtosFindId[0][2],
            "preco": produtosFindId[0][3],
            "datavenda": produtosFindId[0][5]
        }    
        return jsonify(produtosFindIdDict)
    
    except Exception as e:
        print(f"Erro ao encontrar produto por ID: {e}")     
        return jsonify({"erro" : "Erro no servidor"})
    
@app.route("/findByNome", methods=["GET", "POST"])
def findByNome():
    
    if request.method == "GET":
        return render_template("findByNome.html")
    
    try:
        nome = request.form.get("nome")
        if nome is None:
            return abort(400, description="Produto não fornecido")  
        
        produtosFindNome = dao.findByName(nome)
        print(produtosFindNome)
        
        if produtosFindNome is None:
            return abort(404, description="Produto não encontrado")
        
        produtosFindNomeDict = {
            "id": produtosFindNome[0][0],
            "nome": produtosFindNome[0][1],
            "qtde": produtosFindNome[0][2],
            "preco": produtosFindNome[0][3],
            "datavenda": produtosFindNome[0][5]
        }    
        return jsonify(produtosFindNomeDict)
    except Exception as e:
        print (f"Erro ao encontrar produto por ID: {e}")
        return jsonify({"Erro" : "Erro no servidor"})
    
@app.route('/grafProduto', methods=['GET'])
def exibirgrafProds():
    try:
        nome_produto = request.args.get("nome_produto", default=None, type=str)
        fig = dataanalise.gerarGrafProdutos(nome_produto)
        #print(fig.to_html())
        
        return render_template('grafProdutos.html', plot=fig.to_html())
    except Exception as e:
    
        print(f"Erro ao mostrar grafico: {e}")
        
        return render_template_string(f"<h1>{e}</h1>")
        
@app.route('/login/externo', methods=['POST'])
def login_externo():
    login = request.json['login']
    senha = request.json['senha']
    print(login)

    if dao.verificarlogin(login, senha, dao.conectardb()):
        token = create_access_token(identity=login)
        return jsonify(access_token=token), 200
    else:
        abort(401, description="Usuário ou senha inválidos")
        
@app.route('/protegido/obter/<string:login>', methods=['GET'])
@jwt_required()
def get_usuario_protegido(login):
    usuario_logado = get_jwt_identity()
    print(usuario_logado)
    user = dao.b(login)
    if len(user) == 0:
        abort(404, description="usuário não encontrado")
    return jsonify(user), 200


@app.route('/protegido/listarusuarios/externo', methods=['GET'])
@jwt_required()
def listar_usuarios_externo():
    usuario_logado = get_jwt_identity()
    print(usuario_logado)
    return jsonify(dao.lista_produtos(1)), 200
