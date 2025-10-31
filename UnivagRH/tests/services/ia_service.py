from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', api_key))

def gerar_resposta_ia(mensagem, dados_funcionario):
    """
    Função para gerar respostas da IA usando OpenAI (versão atualizada)
    """
    # Contexto específico para o assistente de RH
    contexto_rh = f"""
    Você é um assistente virtual especializado em Recursos Humanos da empresa New Center.
    Seu nome é Alex. Seja prestativo, profissional, amigável e conversacional.

    Sua função é ajudar funcionários com dúvidas sobre:
    - Férias e afastamentos
    - Benefícios (VR, VT, plano de saúde)
    - Documentação pessoal e holerites
    - Procedimentos internos
    - Dúvidas sobre folha de pagamento
    - Políticas da empresa

    Informações do funcionário atual:
    Nome: {dados_funcionario.get('NOME_COMPLETO', 'Não informado')}
    Cargo: {dados_funcionario.get('CARGO', 'Não informado')}
    Departamento: {dados_funcionario.get('DEPARTAMENTO', 'Não informado')}

    Seja direto mas simpático. Use emojis ocasionalmente para tornar a conversa mais amigável.
    Se não souber a resposta específica, oriente o funcionário a entrar em contato com o RH diretamente.
    Responda em português brasileiro de forma natural.
    """

    try:
        # Implementação com OpenAI (versão 1.0+)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": contexto_rh},
                {"role": "user", "content": mensagem}
            ],
            max_tokens=500,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Erro na API de IA: {e}")
        # Fallback para respostas locais caso a API falhe
        return gerar_resposta_fallback(mensagem, dados_funcionario)


def gerar_resposta_fallback(mensagem, dados_funcionario):
    """
    Respostas padrão caso a OpenAI não esteja disponível
    """
    mensagem = mensagem.lower()
    nome = dados_funcionario.get('NOME_COMPLETO', '').split()[0] or 'Colega'

    if any(palavra in mensagem for palavra in ['oi', 'olá', 'ola', 'hey', 'bom dia', 'boa tarde']):
        return f"Olá {nome}! 👋 Sou o Alex, seu assistente virtual do RH. Como posso ajudar você hoje?"

    elif any(palavra in mensagem for palavra in ['férias', 'ferias']):
        return f"""Para solicitar férias, {nome}:

1. Acesse **"Nova Solicitação"** no seu painel
2. Selecione o tipo **"Férias"** 
3. Informe o período desejado (mínimo 15 dias)
4. Aprovação em até 5 dias úteis

Precisa de ajuda com mais alguma coisa? 📅"""

    elif any(palavra in mensagem for palavra in ['atestado', 'médico', 'medico']):
        return f"""Sobre atestados, {nome}:

📋 Use **"Nova Solicitação"** → **"Atestado"**
⏰ Envie em até 48h após o atendimento 
📎 Anexe a imagem do documento

Alguma outra dúvida?"""

    elif any(palavra in mensagem for palavra in ['holerite', 'contracheque', 'salário']):
        return f"""Holerites, {nome}:

💳 Disponível até o 5º dia útil de cada mês
📱 Acesso pelo portal do funcionário
❓ Não encontrou? Contate: rh@newcenter.com.br"""

    elif any(palavra in mensagem for palavra in ['benefício', 'beneficios', 'vr', 'vt']):
        return f"""Seus benefícios, {nome}:

🏥 Plano de saúde (Unimed)
🍽️ VR: R$ 30/dia
🚌 VT integral 
💪 Gympass

Para detalhes específicos, consulte o RH!"""

    else:
        return f"""Obrigado pela sua mensagem, {nome}! 

Para questões específicas que não consigo resolver aqui, entre em contato com nosso RH:

📞 (65) 9999-9999
📧 rh@newcenter.com.br
🕒 Seg-Sex: 8h-18h

Posso ajudar com mais alguma coisa? 🤗"""