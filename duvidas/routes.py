import os
import secrets
from flask import render_template, url_for, request, flash, redirect
from duvidas import app, database, bcrypt
from duvidas.forms import FormLoginEmail, FormLoginSenha, FormCriarConta, FormCriarPost, FormEditarPerfil, FormVerificar
from duvidas.models import Usuario, Post, Comentario, Projeto
from flask_login import login_user, logout_user, login_required, current_user
from PIL import Image


@app.route("/", methods=['GET', 'POST'])
def homepage():
    form_criar_post = FormCriarPost()
    posts = Post.query.order_by(Post.id.desc())
    if form_criar_post.validate_on_submit():
        with app.app_context():
            post = Post(titulo=form_criar_post.titulo.data, corpo=form_criar_post.corpo.data, id_usuario=current_user.id)
            database.session.add(post)
            database.session.commit()
            return redirect(url_for('homepage'))
    return render_template('homepage.html', form_criar_post=form_criar_post, posts=posts)


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
            return redirect(url_for('logar'))
    return render_template('cadastrar.html', form_criar_conta=form_criar_conta)


@app.route("/login_email", methods=['GET', 'POST'])
def logar_email():
    form = FormLoginEmail()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario:
            return redirect(url_for('logar_senha', usuario=usuario))
    return render_template('login_email.html', form=form)


def gerar_codigo():
    codigo = secrets.token_hex(3).upper()
    print(codigo)
    return codigo


@app.route("/login_senha/<usuario>", methods=['GET', 'POST'])
def logar_senha(usuario):
    form = FormLoginSenha()
    print(usuario)
    if form.validate_on_submit() and bcrypt.check_password_hash(usuario.senha, form.senha.data):
        codigo = gerar_codigo()
        print(codigo)
        return verificar_login(codigo, usuario, form.check_lembrar.data)
    return render_template('login_senha.html', form=form)


@app.route("/logar/verificar", methods=['GET', 'POST'])
def verificar_login(codigo, usuario, lembrar):
    form_verificar = FormVerificar()
    if form_verificar.validate_on_submit() and form_verificar.codigo.data == codigo:
        login_user(usuario, lembrar)
        return redirect(url_for('homepage'))
    return render_template('logar.html', form_verificar=form_verificar, usuario=usuario)


# @app.route("/logar", methods=['GET', 'POST'])
# def logar():
#     form_login = FormLogin()
#     if form_login.validate_on_submit():
#         usuario = Usuario.query.filter_by(email=form_login.email.data).first()
#         if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
#             codigo = gerar_codigo()
#             form_verificar = FormVerificar()
#             flash(f'Login feito com sucesso no e-mail {form_login.email.data}', 'alert-success')
#             return render_template('logar.html', form_login=form_login, form_verificar=form_verificar, codigo=codigo,
#                                    lembrar=form_login.check_lembrar.data, usuario=usuario)
#             # return redirect(url_for('verificar_login'))
#             # query_next = request.args.get('next')
#             # if query_next:
#             #     return redirect(query_next)
#             # else:
#             #     return redirect(url_for('verificar_login'))
#
#         else:
#             raise ValueError('Email ou senha incorretos')
#
#     return render_template('logar.html', form_login=form_login)


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


@app.route("/perfil/<usuario>", methods=['GET', 'POST'])
@login_required
def perfil(usuario):
    usuario_perfil = database.session.query(Usuario).filter_by(user=usuario).first()
    form_editar_perfil = FormEditarPerfil()
    if form_editar_perfil.foto_perfil.data:
        with app.app_context():
            imagem = salvar_imagem(form_editar_perfil.foto_perfil.data)
            usuario_perfil.foto_perfil = imagem
            database.session.commit()
            return redirect(url_for('perfil', usuario=usuario))
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(usuario_perfil.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil, form_editar_perfil=form_editar_perfil,
                           usuario=usuario_perfil)


@app.route("/perfil/<usuario>/editar", methods=['GET', 'POST'])
@login_required
def editar_perfil(usuario):
    form_editar_perfil = FormEditarPerfil()
    if form_editar_perfil.senha.data and not 5 < len(form_editar_perfil.senha.data) < 21:
        form_editar_perfil.senha.errors = list(form_editar_perfil.senha.errors)
        form_editar_perfil.senha.errors.append(ValueError("A senha deve ter entre 6-20 caracteres."))
    elif form_editar_perfil.validate_on_submit():
        current_user.email = form_editar_perfil.email.data
        current_user.user = form_editar_perfil.user.data
        current_user.bio = form_editar_perfil.bio.data
        if form_editar_perfil.senha.data and not(bcrypt.check_password_hash(current_user.senha, form_editar_perfil.senha.data)):
            senha_cripto = bcrypt.generate_password_hash(form_editar_perfil.senha.data).decode('utf8')
            current_user.senha = senha_cripto
        database.session.commit()
    elif request.method == 'GET':
        form_editar_perfil.email.data = current_user.email
        form_editar_perfil.user.data = current_user.user
        form_editar_perfil.bio.data = current_user.bio
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form_editar_perfil=form_editar_perfil)


@app.route("/projetos")
@login_required
def projetos():
    return render_template('projetos.html')
