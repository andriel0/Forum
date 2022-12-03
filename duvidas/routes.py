from flask import render_template, url_for, request, flash, redirect
from duvidas import app
from duvidas.forms import FormLogin, FormCriarConta


@app.route("/")
def homepage():
    return render_template('homepage.html')


@app.route("/cadastrar", methods=['GET', 'POST'])
def cadastrar():
    form_criar_conta = FormCriarConta()
    if form_criar_conta.validate_on_submit():
        flash('Conta criada com sucesso.', 'alert-success')
        redirect(url_for('homepage'))
    return render_template('cadastrar.html', form_criar_conta=form_criar_conta)


@app.route("/logar")
def logar():
    form_login = FormLogin()
    render_template('logar.html', form_login=form_login)
