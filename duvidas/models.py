from duvidas import database, login_manager
from datetime import datetime
from flask_login import UserMixin
import secrets


@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.get(id_usuario)


class Usuario(database.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = database.Column(database.Integer, primary_key=True)
    user = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg', nullable=False)
    code = database.Column(database.String, default='')
    bio = database.Column(database.Text, default='', nullable=False)
    posts_user = database.relationship('Post', backref='autor', lazy=True)
    comentarios_user = database.relationship('duvidas.models.Comentario', lazy=True, overlaps="comentarios_user")
    projetos_user = database.relationship('duvidas.models.Projeto', lazy=True, overlaps="projetos_user")


    def get_code(self):
        self.code = secrets.token_hex(3)



class Post(database.Model):
    __table_args__ = {'extend_existing': True}
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    comentarios_post = database.relationship('duvidas.models.Comentario', lazy=True, overlaps="comentarios_post")


class Comentario(database.Model):
    __table_args__ = {'extend_existing': True}
    id = database.Column(database.Integer, primary_key=True)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    id_post = database.Column(database.Integer, database.ForeignKey('post.id'), nullable=False)


class Projeto(database.Model):
    __table_args__ = {'extend_existing': True}
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    explicacao = database.Column(database.Text, nullable=False)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
