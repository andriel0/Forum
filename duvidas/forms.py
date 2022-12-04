from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from duvidas.models import Usuario


class FormCriarConta(FlaskForm):
    user = StringField('Nome de Usuário', validators=[DataRequired(), Length(4, 16)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    conf_senha = PasswordField('Confirmação de Senha', validators=[EqualTo('senha')])
    btn_submit_cadastro = SubmitField('Cadastrar')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.')

    def validate_user(self, user):
        usuario = Usuario.query.filter_by(user=user.data).first()
        if usuario:
            raise ValidationError('Nome de usuário já cadastrado. Cadastre-se com outro nome de usuário ou faça login para continuar.')


class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    check_lembrar = BooleanField('Lembrar dados')
    btn_submit_login = SubmitField('Fazer Login')
