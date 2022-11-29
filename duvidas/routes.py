from flask import render_template
from duvidas import app
from duvidas.forms import FormLogin, FormCriarConta


@app.route("/")
def homepage():
    return render_template('homepage.html')


@app.route("/cadastrar")
def cadastrar():
    form_criar_conta = FormCriarConta()
    return render_template('cadastrar.html', form_criar_conta=form_criar_conta)


@app.route("/logar")
def logar():
    form_login = FormLogin()
    render_template('logar.html', form_login=form_login)
