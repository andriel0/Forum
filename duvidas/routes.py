import os
import secrets
from flask import render_template, url_for, request, flash, redirect
from duvidas import app, database, bcrypt
from duvidas.forms import FormLogin, FormCriarConta, FormCriarPost, FormEditarPerfil
from duvidas.models import Usuario, Post, Comentario, Projeto
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf.file import FileField, FileAllowed
from PIL import Image



@app.route("/", methods=['GET', 'POST'])
def homepage():
    form_criar_post = FormCriarPost()
    if form_criar_post.validate_on_submit():
        with app.app_context():
            post = Post(titulo=form_criar_post.titulo.data, corpo=form_criar_post.corpo.data, id_usuario=current_user.id)
            database.session.add(post)
            database.session.commit()
            return redirect(url_for('homepage'))
    return render_template('homepage.html', form_criar_post=form_criar_post)


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


@app.route("/sair")
@login_required
def sair():
    logout_user()
    return redirect(url_for('homepage'))


def salvar_imagem(imagem):
    # criptografando e colocando na pasta
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)

    # reduzindo tamanho da foto
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    # salvando a foto reduzida
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


@app.route("/meuperfil", methods=['GET', 'POST'])
@login_required
def meuperfil():
    form_editar_perfil = FormEditarPerfil()
    if form_editar_perfil.foto_perfil.data:
        with app.app_context():
            imagem = salvar_imagem(form_editar_perfil.foto_perfil.data)
            current_user.foto_perfil = imagem
            database.session.commit()
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('meuperfil.html', foto_perfil=foto_perfil, form_editar_perfil=form_editar_perfil)


@app.route("/editarperfil", methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form_editar_perfil = FormEditarPerfil()
    if form_editar_perfil.validate_on_submit():
        with app.app_context():
            current_user.user = form_editar_perfil.user.data
            current_user.email = form_editar_perfil.email.data
            if form_editar_perfil.foto_perfil.data:
                imagem = salvar_imagem(form_editar_perfil.foto_perfil.data)
                current_user.foto_perfil = imagem
            database.session.commit()
            return redirect(url_for('meuperfil'))
            # senha_cripto = bcrypt.generate_password_hash(form_editar_perfil.senha.data).decode('utf8')
            # usuario = Usuario(id=current_user.id, user=form_editar_perfil.user.data, email=form_editar_perfil.email.data,
            #               senha=senha_cripto)
            # return redirect(url_for('meuperfil'))
    elif request.method == 'GET':
        form_editar_perfil.user.data = current_user.user
        form_editar_perfil.email.data = current_user.email
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form_editar_perfil=form_editar_perfil)


@app.route("/projetos")
@login_required
def projetos():
    return render_template('projetos.html')
