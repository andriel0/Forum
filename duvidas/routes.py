from flask import render_template, url_for, request, flash, redirect
from duvidas import app, database, bcrypt
from duvidas.forms import FormLogin, FormCriarConta
from duvidas.models import Usuario
from flask_login import login_user, logout_user, login_required


@app.route("/")
def homepage():
    return render_template('homepage.html')


@app.route("/cadastrar", methods=['GET', 'POST'])
def cadastrar():
    form_criar_conta = FormCriarConta()
    if form_criar_conta.validate_on_submit():
        with app.app_context():
            senha_cripto = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode('utf8')
            usuario = Usuario(user=form_criar_conta.user.data, email=form_criar_conta.email.data, senha=senha_cripto)
            database.session.add(usuario)
            database.session.commit()
            flash(f'Conta criada com sucesso no e-mail {form_criar_conta.email.data}', 'alert-success')
            return redirect(url_for('homepage'))
    return render_template('cadastrar.html', form_criar_conta=form_criar_conta)


@app.route("/logar", methods=['GET', 'POST'])
def logar():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, form_login.check_lembrar.data)
            flash(f'Login feito com sucesso no e-mail {form_login.email.data}', 'alert-success')
            query_next = request.args.get('next')
            if query_next:
                return redirect(query_next)
            else:
                return redirect(url_for('homepage'))
        else:
            flash(f'Email ou senha incorretos', 'alert-danger')
    return render_template('logar.html', form_login=form_login)


@login_required
@app.route("/sair")
def sair():
    logout_user()
    return redirect(url_for('homepage'))


@login_required
@app.route("/projetos")
def projetos():
    return render_template('projetos.html')
