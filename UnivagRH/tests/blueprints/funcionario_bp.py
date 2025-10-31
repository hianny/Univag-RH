from flask import Blueprint, flash
from flask import render_template, request, redirect, url_for, session, jsonify
from datetime import datetime

from flask_login import login_required, current_user, logout_user

from tests.services.ia_service import gerar_resposta_ia
from tests.models import Usuario
from tests.services.solicitacao_service import SolicitacaoService
from tests.utils.cache_helpers import TipoSolicitacaoCache

funcionario_bp = Blueprint('funcionario', __name__)


def _get_funcionario_dict():
    if current_user.detalhes:
        return {
            'ID': current_user.detalhes.id_usuario_detalhe,
            'NOME_COMPLETO': current_user.detalhes.nome,
            'CARGO': current_user.detalhes.cargo,
            'EMAIL': current_user.detalhes.email,
            'ENDERECO': current_user.detalhes.endereco,
            'SALARIO': current_user.detalhes.salario,
            'CPF': current_user.detalhes.cpf
        }
    return None


def _get_solicitacoes_dict():
    if current_user.solicitacoes:
        solicitacoes = current_user.solicitacoes
        solicitacoes.sort(key=lambda solicitacao: solicitacao.id_solicitacao, reverse=True)
        return [
            {'status': solicitacao.fluxos_aprovacao[0].status_solicitacao,
             'tipo': solicitacao.tipo_solicitacao.descricao_tipo_solicitacao,
             'data': solicitacao.data_solicitacao} for solicitacao in solicitacoes]
    return None


@funcionario_bp.route('/funcionario')
@login_required
def painel():
    if not current_user.is_authenticated or current_user.rh:
        return redirect(url_for('auth.index'))

    # Pega os dados do funcionário e suas solicitações da sessão
    funcionario = _get_funcionario_dict()

    if not funcionario:
        logout_user()
        session.pop('_flashes', None)
        flash("Dados do funcionário não encontrados. Por favor, faça login novamente.")
        return redirect(url_for('auth.login'))

    solicitacoes_funcionario = _get_solicitacoes_dict()

    # Renderiza o template do dashboard do funcionário
    return render_template('funcionario/main_page.html',
                           funcionario=funcionario,
                           solicitacoes_funcionario=solicitacoes_funcionario)


@funcionario_bp.route('/funcionarios/solicitacoes', methods=['GET', 'POST'])
@login_required
def criar_solicitacao():
    if current_user.rh:
        return redirect(url_for('auth.index'))

    funcionario = _get_funcionario_dict()
    if not funcionario:
        logout_user()
        session.pop('_flashes', None)
        flash("Dados do funcionário não encontrados. Por favor, faça login novamente.")
        return redirect(url_for('auth.login'))

    tipos_solicitacao = TipoSolicitacaoCache.get_all()

    if request.method == 'GET':

        solicitacoes_funcionario = _get_solicitacoes_dict()

        # Renderiza o formulário para criar uma nova solicitação
        return render_template('funcionario/solicitar.html',
                               funcionario=funcionario, tipos_solicitacao=tipos_solicitacao,
                               solicitacoes_funcionario=solicitacoes_funcionario)

    elif request.method == 'POST':
        tipo_solicitacao = request.form.get('requestType')
        data_solicitacao = request.form.get('requestDate')
        detalhes_solicitacao = request.form.get('requestDetails')

        # TODO:
        # Validação básica dos campos
        if not all([tipo_solicitacao, data_solicitacao, detalhes_solicitacao]) or not TipoSolicitacaoCache.get_by_id(tipo_solicitacao):
            flash("Por favor, preencha todos os campos da solicitação.")
            return redirect(url_for('funcionario.criar_solicitacao'))

        # Adiciona a nova solicitação à lista na sessão
        # Em um app real, esta solicitação seria salva em um banco de dados
        success = SolicitacaoService.solicitar(id_user=current_user.id_user, id_func=current_user.funcionario.id_func,
                                               id_tipo=int(tipo_solicitacao), data=data_solicitacao,
                                               mensagem=detalhes_solicitacao)

        if success:
            return redirect(url_for('funcionario.painel'))
        else:
            return redirect(url_for('funcionario.criar_solicitacao'))


@funcionario_bp.route('/funcionarios/chat-ia', methods=['GET', 'POST'])
@login_required
def chat_ia():
    if current_user.rh:
        return redirect(url_for('auth.index'))

    funcionario = _get_funcionario_dict()
    if not funcionario:
        logout_user()
        session.pop('_flashes', None)
        flash("Dados do funcionário não encontrados. Por favor, faça login novamente.")
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        # Renderiza a página do chat
        return render_template('funcionario/chat_ia.html',
                               funcionario=funcionario,
                               now=datetime.now())

    elif request.method == 'POST':
        # Processa as mensagens do chat
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'Mensagem vazia'}), 400

        try:
            # Resposta da IA com OpenAI atualizada
            ai_response = gerar_resposta_ia(user_message, funcionario)

            return jsonify({
                'response': ai_response,
                'timestamp': datetime.now().strftime('%H:%M')
            })

        except Exception as e:
            print(f"Erro no chat com IA: {e}")
            return jsonify({
                'response': 'Desculpe, estou com problemas técnicos no momento. Por favor, tente novamente mais tarde.',
                'timestamp': datetime.now().strftime('%H:%M')
            })
