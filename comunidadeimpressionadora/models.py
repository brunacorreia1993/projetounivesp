from comunidadeimpressionadora import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)
    cursos = database.Column(database.String, nullable=False, default='Não Informado')

    def contar_posts(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

##############################################################

class Imovel(database.Model):
    idImovel = database.Column(database.Integer, primary_key=True)
    endTipoLogradouro = database.Column(database.String(45))
    endNome = database.Column(database.String(45))
    endNumero = database.Column(database.Integer)
    endComplemento = database.Column(database.String(45))
    endBairro = database.Column(database.String(45))
    endCidade = database.Column(database.String(45))
    endEstado = database.Column(database.String(45))
    endCEP = database.Column(database.String(8))
    alugado = database.Column(database.Enum('Sim', 'Não'))
    cpfDono = database.Column(database.String(11))
    nome = database.Column(database.String(45))
    email = database.Column(database.String(45))
    dddTelefone = database.Column(database.Integer)
    numeroTelefone = database.Column(database.BigInteger)
    contaBancaria = database.Column(database.String(45))

class Inquilino(database.Model):
    cpfInquilino = database.Column(database.String(11), primary_key=True)
    nome = database.Column(database.String(45))
    email = database.Column(database.String(45))
    dddTelefone = database.Column(database.Integer)
    numeroTelefone = database.Column(database.BigInteger)
    imovel_alugado = database.Column(database.Enum('Rua Barcelos Leite, 85 , Vila Primavera', 'Rua Inconfidência Baiana, 211 , Vila Primavera'))

class Pagamentos(database.Model):
    idPagto = database.Column(database.String(45), primary_key=True)
    dono = database.Column(database.String(45))
    inquilino = database.Column(database.String(45))
    contrato = database.Column(database.String(45))
    dataVencimento = database.Column(database.String(45))
    pagoInquilino = database.Column(database.Enum('Sim', 'Não'))
    valorAluguel = database.Column(database.Float)
    valorPago = database.Column(database.Float)
    dataPagtoInquilino = database.Column(database.String(45))
    pagoDono = database.Column(database.Enum('Sim', 'Não'))
    dataPagtoDono = database.Column(database.String(45))