from duvidas import app, database
from models import Usuario


# Criar database e tabelas

# with app.app_context():
    # database.create_all()


# Criar Usuários

# with app.app_context():
#     usuario = Usuario(user='Andriel', email='andriel@gmail.com', senha='lol1234')
#     database.session.add(usuario)
#     database.session.commit()