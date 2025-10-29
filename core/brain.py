import json
import os

def generate_plan(user_input: str, config: dict, log) -> dict:
    """
    Interpreta o pedido do usuário e gera um plano de ação.
    Usa OpenAI API se a chave estiver configurada, senão usa mock.
    Retorno:
    {
      "explicacao": "Entendi que você quer X",
      "passos": ["passo 1", "passo 2", ...]
    }
    """
    log.log(f"Recebido do usuário: {user_input}")
    
    # Verifica se tem chave da OpenAI configurada
    openai_key = config.get("openai_api_key", "").strip()
    if openai_key and openai_key != "COLE_SUA_CHAVE_AQUI":
        try:
            return generate_plan_with_ai(user_input, config, log)
        except Exception as e:
            log.error(f"Erro na IA, usando fallback: {str(e)}")
            return generate_plan_mock(user_input, log)
    else:
        log.debug("Chave OpenAI não configurada, usando modo mock")
        return generate_plan_mock(user_input, log)

def generate_plan_with_ai(user_input: str, config: dict, log) -> dict:
    """
    Gera plano usando OpenAI API
    """
    try:
        from openai import OpenAI
        client = OpenAI(api_key=config["openai_api_key"])
        
        system_prompt = """Você é a Sol, assistente pessoal inteligente que converte intenções humanas em planos de execução para Windows.

🌟 SUA MISSÃO: Transformar linguagem natural em comandos estruturados executáveis.

� POLÍTICA DE SEGURANÇA:
- NUNCA execute ações diretamente
- SEMPRE gere planos que precisam de confirmação humana
- Use APENAS comandos da lista oficial
- Para ações perigosas, explique os riscos

� FORMATO OBRIGATÓRIO (JSON):
{
  "explicacao": "Explicação clara e amigável do que você entendeu",
  "passos": ["comando_exato", "comando_com_parametro:valor"]
}

⚡ COMANDOS OFICIAIS DISPONÍVEIS:

NAVEGAÇÃO WEB:
• abrir_navegador
• abrir_url:URL_COMPLETA
• pesquisar_no_youtube:TERMO
• pesquisar_google:TERMO

SISTEMA LOCAL:
• abrir_explorador_arquivos
• criar_pasta:CAMINHO_COMPLETO
• abrir_programa:NOME_PROGRAMA
• listar_arquivos:CAMINHO

INFORMAÇÕES:
• obter_data_atual
• obter_hora_atual
• mostrar_status_sistema
• executar_comando:COMANDO_SEGURO

COMUNICAÇÃO:
• falar_para_usuario:MENSAGEM

🎯 EXEMPLOS DE EXCELÊNCIA:

"abre o YouTube" 
→ {"explicacao": "Vou abrir o YouTube no seu navegador", "passos": ["abrir_navegador", "abrir_url:https://www.youtube.com"]}

"que dia é hoje?"
→ {"explicacao": "Vou verificar a data atual do sistema", "passos": ["obter_data_atual"]}

"cria uma pasta chamada Projetos"
→ {"explicacao": "Vou criar uma pasta chamada Projetos na área de trabalho", "passos": ["criar_pasta:C:\\Users\\%USERNAME%\\Desktop\\Projetos"]}

"me mostra as informações do computador"
→ {"explicacao": "Vou coletar informações básicas do seu sistema", "passos": ["mostrar_status_sistema"]}

"não sei fazer isso"
→ {"explicacao": "Ainda não tenho essa capacidade, mas posso ajudar com navegação web, arquivos básicos e informações do sistema", "passos": []}

🛡️ SEGURANÇA CRÍTICA:
- Só use comandos da lista oficial
- Sempre explique o que vai fazer
- Para dúvidas, deixe "passos" vazio
- Seja transparente sobre limitações

💡 SEJA ÚTIL, SEGURA E PRECISA!"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content.strip()
        log.debug(f"Resposta da IA: {ai_response}")
        
        # Tenta parsear a resposta como JSON
        try:
            plan = json.loads(ai_response)
            if "explicacao" in plan and "passos" in plan:
                return plan
            else:
                raise ValueError("Formato de resposta inválido")
        except:
            # Se não conseguir parsear, cria um plano baseado na resposta
            return {
                "explicacao": f"IA respondeu: {ai_response}",
                "passos": ["interpretar_resposta_ia"]
            }
            
    except ImportError:
        log.error("Biblioteca openai não instalada. Use: pip install openai")
        return generate_plan_mock(user_input, log)
    except Exception as e:
        log.error(f"Erro na chamada da IA: {str(e)}")
        return generate_plan_mock(user_input, log)

def generate_plan_mock(user_input: str, log) -> dict:
    """
    Versão mock para quando a IA não está disponível
    """
    log.debug("Usando modo mock (sem IA)")
    
    # Mock inteligente baseado em palavras-chave
    input_lower = user_input.lower()
    
    if any(word in input_lower for word in ["youtube", "video", "música"]):
        return {
            "explicacao": "Entendi que você quer abrir o YouTube e buscar algo.",
            "passos": [
                "abrir_navegador",
                "abrir_url:https://www.youtube.com",
                "pesquisar_no_youtube:lofi hip hop"
            ]
        }
    elif any(word in input_lower for word in ["google", "pesquisar", "buscar"]):
        return {
            "explicacao": "Vou fazer uma pesquisa no Google para você.",
            "passos": [
                "abrir_navegador",
                "pesquisar_google:" + user_input
            ]
        }
    elif any(word in input_lower for word in ["pasta", "arquivo", "explorador"]):
        return {
            "explicacao": "Vou abrir o explorador de arquivos e criar uma estrutura.",
            "passos": [
                "abrir_explorador_arquivos",
                "criar_pasta:C:\\Temp\\SolAgent_Exemplo"
            ]
        }
    elif any(word in input_lower for word in ["abrir", "programa", "app"]):
        return {
            "explicacao": "Vou tentar abrir um programa para você.",
            "passos": [
                "abrir_programa:notepad"
            ]
        }
    elif any(word in input_lower for word in ["hora", "horas"]):
        return {
            "explicacao": "Vou mostrar o horário atual do sistema.",
            "passos": [
                "obter_hora_atual"
            ]
        }
    elif any(word in input_lower for word in ["data", "dia", "hoje"]):
        return {
            "explicacao": "Vou mostrar a data atual do sistema.",
            "passos": [
                "obter_data_atual"
            ]
        }
    elif any(word in input_lower for word in ["sistema", "computador", "pc", "informações"]):
        return {
            "explicacao": "Vou mostrar informações do seu sistema.",
            "passos": [
                "mostrar_status_sistema"
            ]
        }
    elif any(word in input_lower for word in ["comando", "executar", "terminal"]):
        return {
            "explicacao": "Vou executar um comando básico do sistema.",
            "passos": [
                "executar_comando:date"
            ]
        }
    else:
        return {
            "explicacao": "Entendi que você quer executar uma ação no sistema. (Modo mock ativo - configure sua chave OpenAI para IA real)",
            "passos": [
                "falar_para_usuario:Olá! Sou a Sol em modo demonstração. Configure sua chave OpenAI para funcionalidade completa!"
            ]
        }