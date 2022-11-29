from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class FormCriarConta(FlaskForm):
    user = StringField('Nome de Usuário', validators=[DataRequired(),Length(4,16)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    conf_senha = PasswordField('Confirmação de Senha', validators=[EqualTo('senha')])
    btn_submit_cadastro = SubmitField('Cadastrar')


class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    check_lembrar = BooleanField('Lembrar dados')
    btn_submit_login = SubmitField('Fazer Login')
