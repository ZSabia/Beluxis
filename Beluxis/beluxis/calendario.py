from datetime import datetime, timedelta
from .models import Agendamento, db
from flask import current_app
from sqlalchemy.orm import joinedload

def get_agendamentos_mes(ano, mes, admin_view=False):
    """
    Retorna agendamentos para um mês específico.
    Se admin_view=True, retorna todos os agendamentos.
    Caso contrário, retorna apenas agendamentos aprovados.
    """
    start_date = datetime(ano, mes, 1)
    if mes == 12:
        end_date = datetime(ano + 1, 1, 1)
    else:
        end_date = datetime(ano, mes + 1, 1)

    query = Agendamento.query.options(joinedload(Agendamento.servico), joinedload(Agendamento.cliente)).filter(
        Agendamento.data_hora >= start_date,
        Agendamento.data_hora < end_date
    )

    if not admin_view:
        query = query.filter_by(status='aprovado')

    return query.order_by(Agendamento.data_hora).all()

def get_agendamentos_dia(data, admin_view=False):
    """
    Retorna agendamentos para uma data específica.
    """
    start_date = datetime.combine(data, datetime.min.time())
    end_date = start_date + timedelta(days=1)

    query = Agendamento.query.options(joinedload(Agendamento.servico), joinedload(Agendamento.cliente)).filter(
        Agendamento.data_hora >= start_date,
        Agendamento.data_hora < end_date
    )

    if not admin_view:
        query = query.filter_by(status='aprovado')

    return query.order_by(Agendamento.data_hora).all()

def verificar_conflito_agendamento(servico_id, data_hora, duracao_minutos, excluir_id=None):
    """
    Verifica se há conflito de horário para um novo agendamento.
    Retorna True se há conflito, False caso contrário.
    """
    start_time = data_hora
    end_time = data_hora + timedelta(minutes=duracao_minutos)

    query = Agendamento.query.filter(
        Agendamento.servico_id == servico_id,
        Agendamento.status == 'aprovado',
        Agendamento.data_hora < end_time,
        (Agendamento.data_hora + timedelta(minutes=Agendamento.servico.duracao)) > start_time
    )

    if excluir_id:
        query = query.filter(Agendamento.id != excluir_id)

    conflito = query.first()
    return conflito is not None

def get_calendario_data(ano, mes, admin_view=False):
    """
    Retorna dados do calendário para um mês específico.
    Se admin_view=True, retorna todos os agendamentos.
    Caso contrário, retorna apenas agendamentos aprovados.
    """
    agendamentos = get_agendamentos_mes(ano, mes, admin_view=admin_view)

    # Organizar por dia
    calendario = {}
    for agendamento in agendamentos:
        dia = agendamento.data_hora.day
        if dia not in calendario:
            calendario[dia] = []
        calendario[dia].append(agendamento)

    return calendario
