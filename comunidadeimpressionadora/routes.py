from flask import render_template, redirect, url_for, flash, request, abort
import requests
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost, FormImovel, InquilinoForm
from comunidadeimpressionadora.models import Usuario, Post, Imovel, Inquilino, Pagamentos
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image
from datetime import datetime


@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorretos', 'alert-danger')
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout Feito com Sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('Perfil atualizado com Sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Atualizado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluído com Sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)


@app.route("/cadastrar_imovel", methods=['GET', 'POST'])
def cadastrar_imovel():
    form = FormImovel()

    if form.validate_on_submit():
        # Verifique se o endCEP é igual a "03390040"
        if form.endCEP.data == "03390040":
            # Preencha automaticamente os outros campos no formulário
            form.endTipoLogradouro.data = "Rua"
            form.endNome.data = "Barcelos Leite"
            form.endBairro.data = "Vila Primavera"
            form.endCidade.data = "São Paulo"
            form.endEstado.data = "SP"
        elif form.endCEP.data == "03390050":
            # Preencha automaticamente os outros campos no formulário
            form.endTipoLogradouro.data = "Rua"
            form.endNome.data = "Inconfidência Baiana"
            form.endBairro.data = "Vila Primavera"
            form.endCidade.data = "São Paulo"
            form.endEstado.data = "SP"

        novo_imovel = Imovel(
            endTipoLogradouro=form.endTipoLogradouro.data,
            endNome=form.endNome.data,
            endNumero=form.endNumero.data,
            endComplemento=form.endComplemento.data,
            endBairro=form.endBairro.data,
            endCidade=form.endCidade.data,
            endEstado=form.endEstado.data,
            endCEP=form.endCEP.data,
            alugado=form.alugado.data,
            cpfDono=form.cpfDono.data,
            nome=form.nome.data,
            email=form.email.data,
            dddTelefone=form.dddTelefone.data,
            numeroTelefone=form.numeroTelefone.data,
            contaBancaria=form.contaBancaria.data
        )

        # Adicione o novo imóvel ao banco de dados
        database.session.add(novo_imovel)
        database.session.commit()

        flash('Imóvel cadastrado com sucesso!', 'success')
        return redirect(url_for('home'))  # Substitua 'home' pela rota desejada

    return render_template('cadastrar_imovel.html', form=form)

@app.route('/listar_imoveis')
def listar_imoveis():
    imoveis = Imovel.query.all()  # Isso assume que você tem um modelo Imovel configurado
    return render_template('listar_imoveis.html', imoveis=imoveis)


@app.route('/editar_imovel/<int:idImovel>', methods=['GET', 'POST'])
def editar_imovel(idImovel):
    imovel = Imovel.query.get_or_404(idImovel)
    form = FormImovel()

    if form.validate_on_submit():
        # Atualize os campos do imóvel com os dados do formulário
        imovel.endCEP = form.endCEP.data
        # Atualize os outros campos conforme necessário

        # Salve as mudanças no banco de dados
        database.session.commit()

        flash('Imóvel atualizado com sucesso!', 'success')
        return redirect(url_for('listar_imoveis'))  # Substitua 'listar_imoveis' pela rota desejada

    elif request.method == 'GET':
        # Preencha o formulário com os dados atuais do imóvel
        form.endCEP.data = imovel.endCEP
        # Preencha os outros campos conforme necessário

    return render_template('editar_imovel.html', form=form)

@app.route('/cadastrar_inquilino', methods=['GET', 'POST'])
def cadastrar_inquilino():
    form = InquilinoForm()

    if form.validate_on_submit():
        novo_inquilino = Inquilino(
            cpfInquilino=form.cpfInquilino.data,
            nome=form.nome.data,
            email=form.email.data,
            dddTelefone=form.dddTelefone.data,
            numeroTelefone=form.numeroTelefone.data,
            imovel_alugado=form.imovel_alugado.data
        )

        database.session.add(novo_inquilino)
        database.session.commit()

        flash('Inquilino cadastrado com sucesso!', 'success')
        return redirect(url_for('home'))  # Substitua 'home' pela rota desejada

    return render_template('cadastrar_inquilino.html', form=form)

def consultar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)

    if response.status_code == 200:
        endereco = response.json()
        return endereco
    else:
        return None

def main():
    cep_digitado = input("Digite o CEP para consulta: ")
    resultado = consultar_cep(cep_digitado)

    if resultado:
        print("Tipo Logradouro:", resultado.get("logradouro", ""))
        print("Nome da Rua:", resultado.get("logradouro", ""))
        print("Bairro:", resultado.get("bairro", ""))
        print("Cidade:", resultado.get("localidade", ""))
        print("Estado:", resultado.get("uf", ""))
    else:
        print("CEP não encontrado ou inválido.")

@app.route('/listar_pagamentos')
def listar_pagamentos():
    pagamentos = Pagamentos.query.all()
    return render_template('listar_pagamentos.html', pagamentos=pagamentos)

@app.route('/editar_pagamento/<id_pagamento>', methods=['GET', 'POST'])
def editar_pagamento(id_pagamento):
    pagamento = Pagamentos.query.get(id_pagamento)

    if request.method == 'POST':
        pagamento.pagoInquilino = request.form['pago_inquilino']

        # Converta os valores para os tipos apropriados
        pagamento.valorAluguel = float(request.form['valor_aluguel'])
        pagamento.valorPago = float(request.form['valor_pago'])

        pagamento.dataPagtoInquilino = request.form['data_pagto_inquilino']
        pagamento.pagoDono = request.form['pago_dono']
        pagamento.dataPagtoDono = request.form['data_pagto_dono']

        # Atualize outros campos conforme necessário

        database.session.commit()

        return redirect(url_for('listar_pagamentos'))

    return render_template('editar_pagamento.html', pagamento=pagamento)