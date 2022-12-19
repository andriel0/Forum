from duvidas import app, database
from models import Usuario


# Criar database e tabelas

with app.app_context():
    database.create_all()

# Excluindo tabelas
# with app.app_context():
#     database.drop_all()

# Criar Usuários

# with app.app_context():
#     usuario = Usuario(user='Andriel', email='andriel@gmail.com', senha='lol1234')
#     database.session.add(usuario)
#     database.session.commit()

# Excluir Usuários

# with app.app_context():
#     user = database.session.query(Usuario).filter_by(id=1).first()
#     database.session.delete(user)
#     database.session.commit()

# Modificar Usuários
# with app.app_context():
#     usuario = database.session.query(Usuario).filter_by(id=2).first()
#     usuario.bio = 'Sou um desenvolvedor Full Stack Júnior.'
#     database.session.commit()

# with app.app_context():
#     usu = database.session.query(Usuario).filter_by(id=2).first()
#     print(usu.user)