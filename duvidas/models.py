from duvidas import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.get(id_usuario)


class Usuario(database.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = database.Column(database.Integer, primary_key=True)
    user = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    bio = database.Column(database.Text, default='')
    posts = database.relationship('duvidas.models.Post', backref='autor', lazy=True)
    projetos = database.relationship('duvidas.models.Projeto', backref='dono', lazy=True)
    comentarios = database.relationship('duvidas.models.Comentario', backref='autor', lazy=True)


class Post(database.Model):
    __table_args__ = {'extend_existing': True}
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.String, database.ForeignKey('usuario.id'), nullable=False)
    comentarios = database.relationship('duvidas.models.Comentario', backref='autor', lazy=True)


class Comentario(database.Model):
    __table_args__ = {'extend_existing': True}
    id = database.Column(database.Integer, primary_key=True)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.String, database.ForeignKey('usuario.id'), nullable=False)
    id_post = database.Column(database.String, database.ForeignKey('post.id'), nullable=False)


class Projeto(database.Model):
    __table_args__ = {'extend_existing': True}
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    explicacao = database.Column(database.Text, nullable=False)
    id_usuario = database.Column(database.String, database.ForeignKey('usuario.id'), nullable=False)
