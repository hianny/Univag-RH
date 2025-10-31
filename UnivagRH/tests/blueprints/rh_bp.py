from flask import Blueprint
from flask import render_template, redirect, url_for, session
from datetime import datetime
import pandas as pd
from flask_login import login_required, current_user

from tests.services.solicitacao_service import SolicitacaoService

rh_bp = Blueprint('rh', __name__)

@rh_bp.route('/rh')
@login_required
def painel():
    if not current_user.rh:
        return redirect(url_for('auth.index'))

    try:
        # Carrega dados do CSV (mantido como no seu código original)
        # df = pd.read_csv(r'./UnivagRH/tests/static/csv/FuncionarioBase.csv', sep=';')
        #
        # # Processa solicitações (simulação - substitua por dados reais)
        # solicitacoes = [
        #     {'funcionario': 'João Silva', 'tipo': 'Férias', 'data': '2023-06-15', 'status': 'Pendente'},
        #     {'funcionario': 'Maria Oliveira', 'tipo': 'Rescisão', 'data': '2023-05-20', 'status': 'Aprovado'},
        #     {'funcionario': 'Carlos Pereira', 'tipo': 'Banco de Horas', 'data': '2023-06-01', 'status': 'Rejeitado'}
        # ]
        solicitacoes = SolicitacaoService.get_all()
        # Processa férias (calcula dias restantes)
        # hoje = datetime.now().date()
        funcionarios_ferias = []

        # for _, row in df.iterrows():
        #     try:
        #         data_ferias = datetime.strptime(str(row['ProximasFerias']), '%Y-%m-%d').date()
        #         dias_restantes = (data_ferias - hoje).days
        #         funcionario_data_rh = row.to_dict()
        #         funcionario_data_rh['dias_restantes'] = dias_restantes
        #         funcionarios_ferias.append(funcionario_data_rh)
        #     except Exception:
        #         continue  # Ignora linhas com erro na data de férias

        # Ordena por proximidade das férias
        funcionarios_ferias.sort(key=lambda x: x['dias_restantes'])

        return render_template('rh.html',
                               solicitacoes=solicitacoes,
                               funcionarios_ferias=funcionarios_ferias)

    except Exception as e:
        return f"Erro ao processar dados do RH: {str(e)}", 500
