from flask import Blueprint, render_template, url_for, flash, redirect, request
from extensions import db
from models.models import Usuario

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index(): 
    return render_template('index.html') 

@main_bp.route('/recursos')
def recursos():
    return render_template('working.html')

@main_bp.route('/sobre')
def sobre():
    return render_template('working.html')

@main_bp.route('/contato')
def contato():
    return render_template('working.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        from werkzeug.security import check_password_hash
        if usuario and check_password_hash(usuario.senha, senha):
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login falhou. Verifique seu email e senha.', 'danger')
    
    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])  
def register():  
    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('Este email já está registrado!', 'danger')
            return redirect(url_for('main.register'))
        
        from werkzeug.security import generate_password_hash
        senha_hash = generate_password_hash(senha, method='pbkdf2:sha256')
        
        novo_usuario = Usuario(nome=nome, sobrenome=sobrenome, email=email, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

@main_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main_bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500