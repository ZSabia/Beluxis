from flask import url_for, current_app
from markupsafe import Markup

def generate_produtos_html(produtos, is_admin=False):
    if not produtos:
        return Markup('<div class="col-12"><p>Nenhum produto cadastrado.</p></div>')

    html = ''
    for p in produtos:
        card = f'''
        <div class="col-md-4 mb-4">
            <div class="card shadow-sm h-100">
                <img src="{url_for('static', filename='images/' + p.imagem)}" class="card-img-top" alt="{p.nome}" style="height: 200px; object-fit: cover;">
                <div class="card-body">
                    <h5 class="card-title">{p.nome}</h5>
                    <p class="card-text">{p.descricao}</p>
                    <p class="card-text"><strong>Preço: R$ {p.preco:.2f}</strong></p>
                    <p class="card-text">Estoque: {p.estoque}</p>
                </div>
            </div>
        </div>
        '''
        html += card
    return Markup(html)

def generate_servicos_html(servicos, is_authenticated=False):
    if not servicos:
        return Markup('<div class="col-12"><p>Nenhum serviço cadastrado.</p></div>')

    html = ''
    for s in servicos:
        btn = f'<a href="{url_for("novo_agendamento")}" class="btn btn-primary">Agendar</a>' if is_authenticated else f'<a href="{url_for("login")}" class="btn btn-outline-primary">Login para Agendar</a>'
        card = f'''
        <div class="col-md-4 mb-4">
            <div class="card shadow-sm h-100">
                <div class="card-body">
                    <h5 class="card-title">{s.nome}</h5>
                    <p class="card-text">{s.descricao}</p>
                    <p class="card-text"><strong>Preço: R$ {s.preco:.2f}</strong></p>
                    <p class="card-text">Duração: {s.duracao} minutos</p>
                    {btn}
                </div>
            </div>
        </div>
        '''
        html += card
    return Markup(html)

def generate_agendamentos_table_html(agendamentos):
    if not agendamentos:
        return Markup('<p>Você não tem agendamentos.</p>')

    rows = ''
    for agendamento in agendamentos:
        status_badge = {
            'pendente': '<span class="badge bg-warning">Aguardando Aprovação</span>',
            'aprovado': '<span class="badge bg-success">Aprovado</span>',
            'negado': '<span class="badge bg-danger">Negado</span>'
        }.get(agendamento.status, agendamento.status)

        actions = '<span class="text-muted">Aguardando aprovação</span>' if agendamento.status == 'pendente' else f'''
        <a href="{url_for('editar_agendamento', id=agendamento.id)}" class="btn btn-sm btn-warning">Editar</a>
        <form method="POST" action="{url_for('deletar_agendamento', id=agendamento.id)}" style="display:inline;">
            <button type="submit" class="btn btn-sm btn-danger" onclick="return confirm('Tem certeza?')">Deletar</button>
        </form>
        '''

        row = f'''
        <tr>
            <td>{agendamento.servico.nome}</td>
            <td>{agendamento.data_hora.strftime('%d/%m/%Y %H:%M')}</td>
            <td>{status_badge}</td>
            <td>{actions}</td>
        </tr>
        '''
        rows += row

    table = f'''
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Serviço</th>
                <th>Data/Hora</th>
                <th>Status</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    '''
    return Markup(table)

def generate_admin_agendamentos_table_html(agendamentos):
    if not agendamentos:
        return Markup('<tr><td colspan="5">Nenhum agendamento pendente.</td></tr>')

    rows = ''
    for ag in agendamentos:
        row = f'''
        <tr>
            <td>{ag.cliente.usuario}</td>
            <td>{ag.servico.nome}</td>
            <td>{ag.data_hora.strftime('%d/%m/%Y %H:%M')}</td>
            <td><span class="badge bg-warning">Pendente</span></td>
            <td>
                <form action="{url_for('aprovar_agendamento', id=ag.id)}" method="post" class="d-inline">
                    <button type="submit" class="btn btn-success btn-sm">Aprovar</button>
                </form>
                <form action="{url_for('negar_agendamento', id=ag.id)}" method="post" class="d-inline">
                    <button type="submit" class="btn btn-danger btn-sm" onclick="return confirm('Tem certeza que deseja negar este agendamento?')">Negar</button>
                </form>
            </td>
        </tr>
        '''
        rows += row
    return Markup(rows)

def generate_admin_produtos_table_html(produtos):
    if not produtos:
        return Markup('<tr><td colspan="5">Nenhum produto cadastrado.</td></tr>')

    rows = ''
    for p in produtos:
        preco = f"R$ {p.preco:.2f}" if p.preco is not None else "R$ 0.00"
        row = f'''
        <tr>
            <th scope="row">{p.id}</th>
            <td>{p.nome}</td>
            <td>{preco}</td>
            <td>{p.estoque}</td>
            <td>
                <a href="{url_for('editar_produto', id=p.id)}" class="btn btn-warning btn-sm">Editar</a>
                <form action="{url_for('deletar_produto', id=p.id)}" method="post" class="d-inline">
                    <button type="submit" class="btn btn-danger btn-sm" onclick="return confirm('Tem certeza que deseja deletar este produto?')">Deletar</button>
                </form>
            </td>
        </tr>
        '''
        rows += row
    return Markup(rows)

def generate_admin_servicos_table_html(servicos):
    if not servicos:
        return Markup('<tr><td colspan="5">Nenhum serviço cadastrado.</td></tr>')

    rows = ''
    for s in servicos:
        preco = f"R$ {s.preco:.2f}" if s.preco is not None else "R$ 0.00"
        row = f'''
        <tr>
            <th scope="row">{s.id}</th>
            <td>{s.nome}</td>
            <td>{preco}</td>
            <td>{s.duracao}</td>
            <td>
                <a href="{url_for('editar_servico', id=s.id)}" class="btn btn-warning btn-sm">Editar</a>
                <form action="{url_for('deletar_servico', id=s.id)}" method="post" class="d-inline">
                    <button type="submit" class="btn btn-danger btn-sm" onclick="return confirm('Tem certeza que deseja deletar este serviço?')">Deletar</button>
                </form>
            </td>
        </tr>
        '''
        rows += row
    return Markup(rows)

def generate_calendar_html(calendario, ano, mes, admin_view=False):
    import calendar
    first_day, days_in_month = calendar.monthrange(ano, mes)
    month_names = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    month_name = month_names[mes - 1]

    nav_prev = url_for('calendario', ano=ano-1 if mes == 1 else ano, mes=mes-1 if mes > 1 else 12)
    nav_next = url_for('calendario', ano=ano+1 if mes == 12 else ano, mes=mes+1 if mes < 12 else 1)

    nav_html = f'''
    <div class="d-flex justify-content-between align-items-center mb-4">
        <a href="{nav_prev}" class="btn btn-outline-primary">&larr; Anterior</a>
        <h2>{month_name} {ano}</h2>
        <a href="{nav_next}" class="btn btn-outline-primary">Próximo &rarr;</a>
    </div>
    '''

    table_rows = ''
    current_day = 1
    for week in range(6):
        row = '<tr>'
        for weekday in range(7):
            if week == 0 and weekday < first_day:
                row += '<td></td>'
            elif current_day <= days_in_month:
                day_class = 'calendar-day has-events' if calendario.get(current_day) else 'calendar-day'
                events_html = ''
                if calendario.get(current_day):
                    for agendamento in calendario[current_day]:
                        status_class = {
                            'aprovado': 'bg-success',
                            'pendente': 'bg-warning',
                            'negado': 'bg-danger'
                        }.get(agendamento.status, 'bg-secondary')
                        event = f'''
                        <div class="event {status_class} text-white p-1 mb-1 rounded small">
                            <strong>{agendamento.data_hora.strftime('%H:%M')}</strong><br>
                            {agendamento.servico.nome}<br>
                        '''
                        if admin_view:
                            event += f'Cliente: {agendamento.cliente.usuario}<br>Status: {agendamento.status}'
                        event += '</div>'
                        events_html += event
                cell = f'''
                <td class="{day_class}">
                    <div class="day-number">{current_day}</div>
                    <div class="events">{events_html}</div>
                </td>
                '''
                row += cell
                current_day += 1
            else:
                row += '<td></td>'
        row += '</tr>'
        table_rows += row

    table_html = f'''
    <div class="card">
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-bordered">
                    <thead class="table-dark">
                        <tr>
                            <th>Dom</th>
                            <th>Seg</th>
                            <th>Ter</th>
                            <th>Qua</th>
                            <th>Qui</th>
                            <th>Sex</th>
                            <th>Sáb</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    '''

    legend_html = '''
    <div class="mt-3">
        <h5>Legenda:</h5>
        <div class="d-flex gap-3">
            <div><span class="badge bg-success">Aprovado</span></div>
    '''
    if admin_view:
        legend_html += '''
            <div><span class="badge bg-warning">Pendente</span></div>
            <div><span class="badge bg-danger">Negado</span></div>
        '''
    legend_html += '</div></div>'

    return Markup(nav_html + table_html + legend_html)
