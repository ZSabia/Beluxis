from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import app, db
from .models import Produto, Cliente, Servico, Agendamento
from .forms import RegistroForm, LoginForm
from .calendario import get_calendario_data
from .template_helpers import generate_produtos_html, generate_servicos_html, generate_agendamentos_table_html, generate_admin_agendamentos_table_html, generate_admin_produtos_table_html, generate_admin_servicos_table_html, generate_calendar_html
from decimal import Decimal
from datetime import datetime


@app.route('/produtos')
def produtos():
    produtos = Produto.query.order_by(Produto.id.desc()).all()
    produtos_html = generate_produtos_html(produtos, current_user.is_authenticated and current_user.is_admin)
    return render_template('produtos.html', produtos_html=produtos_html)


@app.route('/produto/novo', methods=['GET', 'POST'])
@login_required
def novo_produto():
    if not current_user.is_admin:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('homepage'))
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()
        preco = request.form.get('preco', '0').strip()
        estoque = request.form.get('estoque', '0').strip()
        imagem = request.form.get('imagem', 'default.jpg').strip()

        if not nome or not preco:
            flash('Nome e preço são obrigatórios', 'danger')
            return redirect(url_for('novo_produto'))
        try:
            preco_dec = Decimal(preco.replace(',', '.'))
            estoque_int = int(estoque)
        except Exception:
            flash('Preço ou estoque inválido', 'danger')
            return redirect(url_for('novo_produto'))

        produto = Produto(nome=nome, descricao=descricao, preco=preco_dec, estoque=estoque_int, imagem=imagem)
        db.session.add(produto)
        db.session.commit()
        flash('Produto criado', 'success')
        return redirect(url_for('admin_produtos'))

    return render_template('produto_form.html')


@app.route('/produto/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_produto(id):
    if not current_user.is_admin:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('homepage'))
    produto = Produto.query.get_or_404(id)
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()
        preco = request.form.get('preco', '0').strip()
        estoque = request.form.get('estoque', '0').strip()
        imagem = request.form.get('imagem', produto.imagem).strip()

        if not nome or not preco:
            flash('Nome e preço são obrigatórios', 'danger')
            return redirect(url_for('editar_produto', id=id))
        try:
            preco_dec = Decimal(preco.replace(',', '.'))
            estoque_int = int(estoque)
        except Exception:
            flash('Preço ou estoque inválido', 'danger')
            return redirect(url_for('editar_produto', id=id))

        produto.nome = nome
        produto.descricao = descricao
        produto.preco = preco_dec
        produto.estoque = estoque_int
        produto.imagem = imagem
        db.session.commit()
        flash('Produto atualizado', 'success')
        return redirect(url_for('admin_produtos'))

    return render_template('produto_form.html', produto=produto)


@app.route('/produto/deletar/<int:id>', methods=['POST'])
@login_required
def deletar_produto(id):
    if not current_user.is_admin:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('homepage'))
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto deletado', 'success')
    return redirect(url_for('admin_produtos'))


@app.route('/admin/produtos')
@login_required
def admin_produtos():
    if not current_user.is_admin:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('homepage'))
    produtos = Produto.query.order_by(Produto.id.desc()).all()
    produtos_html = generate_admin_produtos_table_html(produtos)
    return render_template('admin_produtos.html', produtos_html=produtos_html)


@app.route('/')
def homepage():
    return render_template("home.html")


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegistroForm()
    if form.validate_on_submit():
        cliente = Cliente.query.filter_by(email=form.email.data).first()
        if cliente:
            flash('Email já cadastrado.', 'danger')
            return redirect(url_for('registro'))
        cliente = Cliente(usuario=form.usuario.data, email=form.email.data, avatar=form.avatar.data)
        cliente.set_password(form.senha.data)
        db.session.add(cliente)
        db.session.commit()
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        cliente = Cliente.query.filter_by(email=form.email.data).first()
        if cliente and cliente.check_password(form.senha.data):
            login_user(cliente)
            return redirect(url_for('homepage'))
        flash('Email ou senha inválidos.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/perfil')
@login_required
def perfil():
    agendamentos_html = generate_agendamentos_table_html(current_user.agendamentos)
    return render_template("perfil.html", cliente=current_user, agendamentos_html=agendamentos_html)


@app.route('/contato')
def contato():
    return render_template("contato.html")

@app.route('/servicos')
def servicos():
    servicos = Servico.query.order_by(Servico.id.desc()).all()
    servicos_html = generate_servicos_html(servicos, current_user.is_authenticated)
    return render_template('servicos.html', servicos_html=servicos_html)


@app.route('/admin/servicos')
@login_required
def admin_servicos():
    if not current_user.is_admin:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('homepage'))
    servicos = Servico.query.order_by(Servico.id.desc()).all()
    servicos_html = generate_admin_servicos_table_html(servicos)
    return render_template('admin_servicos.html', servicos_html=servicos_html)


@app.route('/admin/servico/novo', methods=['GET', 'POST'])
@login_required
def novo_servico():
    if not current_user.is_admin:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('homepage'))
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()
        preco = request.form.get('preco', '0').strip()
        duracao = request.form.get('duracao', '0').strip()

        if not nome or not preco or not duracao:
            flash('Nome, preço e duração são obrigatórios', 'danger')
            return redirect(url_for('novo_servico'))
        try:
            preco_dec = Decimal(preco.replace(',', '.'))
            duracao_int = int(duracao)
        except Exception:
            flash('Preço ou duração inválido', 'danger')
            return redirect(url_for('novo_servico'))

        servico = Servico(nome=nome, descricao=descricao, preco=preco_dec, duracao=duracao_int)
        db.session.add(servico)
        db.session.commit()
        flash('Serviço criado', 'success')
        return redirect(url_for('admin_servicos'))

    return render_template('servico_form.html')


@app.route('/admin/servico/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_servico(id):
    if not current_user.is_admin:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('homepage'))
    servico = Servico.query.get_or_404(id)
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()
        preco = request.form.get('preco', '0').strip()
        duracao = request.form.get('duracao', '0').strip()

        if not nome or not preco or not duracao:
            flash('Nome, preço e duração são obrigatórios', 'danger')
            return redirect(url_for('editar_servico', id=id))
        try:
            preco_dec = Decimal(preco.replace(',', '.'))
            duracao_int = int(duracao)
        except Exception:
            flash('Preço ou duração inválido', 'danger')
            return redirect(url_for('editar_servico', id=id))

        servico.nome = nome
        servico.descricao = descricao
        servico.preco = preco_dec
        servico.duracao = duracao_int
        db.session.commit()
        flash('Serviço atualizado', 'success')
        return redirect(url_for('admin_servicos'))

    return render_template('servico_form.html', servico=servico)


@app.route('/admin/servico/deletar/<int:id>', methods=['POST'])
@login_required
def deletar_servico(id):
    if not current_user.is_admin:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('homepage'))
    servico = Servico.query.get_or_404(id)
    db.session.delete(servico)
    db.session.commit()
    flash('Serviço deletado', 'success')
    return redirect(url_for('admin_servicos'))

@app.route('/agendamento/novo', methods=['GET', 'POST'])
@login_required
def novo_agendamento():
    if request.method == 'POST':
        servico_id = request.form.get('servico_id', '').strip()
        data_hora_str = request.form.get('data_hora', '').strip()

        if not servico_id or not data_hora_str:
            flash('Serviço e data/hora são obrigatórios', 'danger')
            return redirect(url_for('novo_agendamento'))

        try:
            from datetime import datetime
            data_hora = datetime.strptime(data_hora_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Formato de data/hora inválido', 'danger')
            return redirect(url_for('novo_agendamento'))

        agendamento = Agendamento(cliente_id=current_user.id, servico_id=int(servico_id), data_hora=data_hora, status='pendente')
        db.session.add(agendamento)
        db.session.commit()
        flash('Agendamento solicitado! Aguarde a aprovação do administrador.', 'info')
        return redirect(url_for('perfil'))

    servicos = Servico.query.all()
    return render_template('agendamento_form.html', servicos=servicos)

@app.route('/agendamento/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    if agendamento.cliente_id != current_user.id:
        flash('Acesso negado', 'danger')
        return redirect(url_for('perfil'))

    if request.method == 'POST':
        servico_id = request.form.get('servico_id', '').strip()
        data_hora_str = request.form.get('data_hora', '').strip()

        if not servico_id or not data_hora_str:
            flash('Serviço e data/hora são obrigatórios', 'danger')
            return redirect(url_for('editar_agendamento', id=id))

        try:
            from datetime import datetime
            data_hora = datetime.strptime(data_hora_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Formato de data/hora inválido', 'danger')
            return redirect(url_for('editar_agendamento', id=id))

        agendamento.servico_id = int(servico_id)
        agendamento.data_hora = data_hora
        db.session.commit()
        flash('Agendamento atualizado com sucesso!', 'success')
        return redirect(url_for('perfil'))

    servicos = Servico.query.all()
    return render_template('agendamento_form.html', agendamento=agendamento, servicos=servicos)

@app.route('/agendamento/deletar/<int:id>', methods=['POST'])
@login_required
def deletar_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    if agendamento.cliente_id != current_user.id:
        flash('Acesso negado', 'danger')
        return redirect(url_for('perfil'))

    db.session.delete(agendamento)
    db.session.commit()
    flash('Agendamento deletado com sucesso!', 'success')
    return redirect(url_for('perfil'))


@app.route('/admin/agendamentos')
@login_required
def admin_agendamentos():
    if not current_user.is_admin:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('homepage'))
    agendamentos = Agendamento.query.filter_by(status='pendente').all()
    agendamentos_html = generate_admin_agendamentos_table_html(agendamentos)
    return render_template('admin_agendamentos.html', agendamentos_html=agendamentos_html)


@app.route('/admin/agendamento/aprovar/<int:id>', methods=['POST'])
@login_required
def aprovar_agendamento(id):
    if not current_user.is_admin:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('homepage'))
    agendamento = Agendamento.query.get_or_404(id)
    agendamento.status = 'aprovado'
    db.session.commit()
    flash('Agendamento aprovado!', 'success')
    return redirect(url_for('admin_agendamentos'))


@app.route('/admin/agendamento/negar/<int:id>', methods=['POST'])
@login_required
def negar_agendamento(id):
    if not current_user.is_admin:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('homepage'))
    agendamento = Agendamento.query.get_or_404(id)
    agendamento.status = 'negado'
    db.session.commit()
    flash('Agendamento negado.', 'warning')
    return redirect(url_for('admin_agendamentos'))


@app.route('/calendario')
@login_required
def calendario():
    ano = int(request.args.get('ano', datetime.now().year))
    mes = int(request.args.get('mes', datetime.now().month))

    calendario_data = get_calendario_data(ano, mes, admin_view=current_user.is_admin)
    admin_view = current_user.is_admin

    calendario_html = generate_calendar_html(calendario_data, ano, mes, admin_view)

    return render_template('calendario.html', calendario_html=calendario_html)

