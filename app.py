from flask import *
import dao

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
        
def listarProdutos():
    try:
        produtos = dao.listarProdutos()

        if produtos is None:
            produtos = []

        return render_template('listarProdutos.html', produtos=produtos)
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return render_template('listarProdutos.html', produtos=[])

    
        
        
        