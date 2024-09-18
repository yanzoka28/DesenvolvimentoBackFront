from flask import *
import dao

app = Flask(__name__)
app.secret_key = "testedechave"

@app.route('/')
def index():
    return render_template('cadastroUsuario.html')


@app.route ("/telaLogin", methods=["POST"])
def login():
    
    loginUser = request.form.get("login")
    senha = request.form.get("senha")
    
    if dao.verificarLogin(loginUser, senha, dao.conectardb):
        session['loginUser'] = loginUser
        print("Realizado")
        return render_template('cadastroProduto.html')
        
    else:
        print("Login ou Senha incorretos")
        return render_template('login.html')
    
@app.route("/cadastroUsuario", methods=['POST'])        
def cadastrarUsuario():
    if request.method == "POST":
        loginUser = request.form['login']
        senha = request.form['senha']
        tipoUser = request.form["tipoUser"]
        
        if dao.cadastroUsuario(loginUser, senha, tipoUser):
            print("Usuario cadastrado com sucesso")
            return render_template('login.html')
        else:
            print("Este usuario ja existe")
            return render_template('cadastroUsuario.html')
        

@app.route('/cadastroProduto', methods=["GET", "POST"])
def cadastrarProduto():
    if request.method == "POST":
        nome = request.form["nome"]
        qtde = request.form["qtde"]
        preco = request.form["preco"]
        loginUser = request.form["loginUser"]
        ...
        
        
        