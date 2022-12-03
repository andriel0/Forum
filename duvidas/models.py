from duvidas import database
from sqlalchemy import Column, String, INTEGER


class Usuario(database.Model):
    id = database.Column(INTEGER, primary_key=True)
    user = database.Column(String, nullable=False, unique=True)
    email = database.Column(String, nullable=False, unique=True)
    senha = database.Column(String, nullable=False)
    foto_perfil = database.Column(String, default='default.jpg')