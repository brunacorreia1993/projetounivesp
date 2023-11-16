from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    curso_excel = BooleanField('Excel Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_ppt = BooleanField('Apresentações Impressionadoras')
    curso_sql = BooleanField('SQL Impressionador')
    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse e-mail. Cadastre outro e-mail')


class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post Aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')


class FormImovel(FlaskForm):
    endCEP = StringField('CEP', validators=[DataRequired(), Length(max=8)])
    endTipoLogradouro = StringField('Tipo de Logradouro', validators=[DataRequired(), Length(max=45)])
    endNome = StringField('Nome do Logradouro', validators=[DataRequired(), Length(max=45)])
    endNumero = IntegerField('Número do Endereço', validators=[DataRequired()])
    endComplemento = StringField('Complemento', validators=[Length(max=45)])
    endBairro = StringField('Bairro', validators=[DataRequired(), Length(max=45)])
    endCidade = StringField('Cidade', validators=[DataRequired(), Length(max=45)])
    endEstado = StringField('Estado', validators=[DataRequired(), Length(max=45)])
    alugado = SelectField('Alugado', choices=[('Sim', 'Sim'), ('Não', 'Não')], validators=[DataRequired()], default='Não')
    cpfDono = StringField('CPF do Dono', validators=[DataRequired(), Length(max=11)])
    nome = StringField('Nome do Dono', validators=[DataRequired(), Length(max=45)])
    email = StringField('E-mail do Dono', validators=[DataRequired(), Length(max=45)])
    dddTelefone = IntegerField('DDD do Telefone do Dono', validators=[DataRequired()])
    numeroTelefone = IntegerField('Número do Telefone do Dono', validators=[DataRequired()])
    contaBancaria = StringField('Conta Bancária do Dono', validators=[Length(max=45)])

    botao_submit_imovel = SubmitField('Cadastrar Imóvel')


class InquilinoForm(FlaskForm):
    cpfInquilino = StringField('CPF do Inquilino', validators=[DataRequired(), Length(min=11, max=11)])
    nome = StringField('Nome do Inquilino', validators=[DataRequired(), Length(max=45)])
    email = StringField('E-mail do Inquilino', validators=[DataRequired(), Email(), Length(max=45)])
    dddTelefone = IntegerField('DDD do Telefone', validators=[DataRequired()])
    numeroTelefone = IntegerField('Número do Telefone', validators=[DataRequired()])
    imovel_alugado = SelectField('Casa/Apartamento', choices=[('', 'Selecione um imóvel'), (
    'Rua Barcelos Leite, 85 , Vila Primavera', 'Rua Barcelos Leite, 85 , Vila Primavera'), (
                                                            'Rua Inconfidência Baiana, 211 , Vila Primavera',
                                                            'Rua Inconfidência Baiana, 211 , Vila Primavera')],validators=[DataRequired()])


