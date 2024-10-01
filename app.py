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
        loginUser = request.form.get("login")
        senha = request.form.get("senha")
        
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
        loginUser = request.form['login']
        senha = request.form['senha']
        tipoUser = request.form["tipoUser"]
        
    if dao.verificarLogin(loginUser, senha):
        print("Este usuario ja existe")
        return render_template('cadastroUsuario.html')
        
    elif dao.cadastroUsuario(loginUser, senha, tipoUser):
        print("Usuario cadastrado com sucesso")
        return render_template('login.html')
    
    else:
        print('nao realizado')
        return render_template('cadastroUsuario.html')    

@app.route('/cadastroProduto', methods=["GET", "POST"])
def cadastrarProduto():
    if request.method == "GET":
        return render_template("cadastroProduto.html")
    
    if request.method == "POST":
        nome = request.form["nome"]
        qtde = request.form["qtde"]
        preco = request.form["preco"]
        loginUser = request.form["loginUser"]
        
        dao.cadastroProduto(nome, qtde, preco, loginUser)
        return redirect(url_for("home.html"))
        
    render_template("cadastroProduto.html")
        
    
        
        
        