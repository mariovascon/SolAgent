"""
🌟 SolAgent v1.1 - Brain (Cérebro da IA)
===================================

Este módulo é o núcleo de inteligência da SolAgent.
Converte linguagem natural em planos de execução estruturados.

Funcionalidades:
- IA real (OpenAI GPT) quando configurada
- Fallback inteligente (mock) quando offline
- Validação e formatação de respostas
- Segurança e ética embutidas

Autores: Mario, GitHub Copilot & Sol (ela mesma ajudou a se criar!)
Versão: 1.1 (Comercial) - Tríade Criativa
Data: 28/10/2025
"""

import json
import os

def generate_plan(user_input: str, config: dict, log) -> dict:
    """
    🎯 FUNÇÃO PRINCIPAL: Converte linguagem natural em plano de ação
    
    Args:
        user_input (str): Comando do usuário em linguagem natural
        config (dict): Configurações carregadas do config.json
        log: Instância do logger para registrar eventos
    
    Returns:
        dict: Plano estruturado com explicação e passos executáveis
              Formato: {"explicacao": "...", "passos": ["comando1", "comando2:param"]}
    """
    log.log(f"🎤 Recebido do usuário: {user_input}")
    
    # Verifica se tem chave da OpenAI configurada
    openai_key = config.get("openai_api_key", "").strip()
    has_openai_key = openai_key and openai_key != "COLE_SUA_CHAVE_AQUI"
    
    if has_openai_key:
        try:
            log.debug("🧠 Usando IA real (OpenAI)")
            return _generate_plan_with_ai(user_input, config, log)
        except Exception as e:
            log.error(f"❌ Erro na IA, usando fallback: {str(e)}")
            return _generate_plan_mock(user_input, log)
    else:
        log.debug("🤖 Chave OpenAI não configurada, usando modo demonstração")
        return _generate_plan_mock(user_input, log)

def _generate_plan_with_ai(user_input: str, config: dict, log) -> dict:
    """
    🧠 GERADOR COM IA REAL (OpenAI GPT)
    
    Conecta com a API da OpenAI para interpretação avançada de linguagem natural.
    Inclui prompt de segurança e formatação padronizada.
    """
    try:
        from openai import OpenAI
        client = OpenAI(api_key=config["openai_api_key"])
        
        # 🛡️ PROMPT DE SEGURANÇA E FORMATAÇÃO
        system_prompt = """Você é a Sol, assistente pessoal inteligente e ética do SolAgent v1.1.

🌟 SUA MISSÃO:
Transformar linguagem natural em comandos estruturados executáveis para Windows.

🔒 POLÍTICA DE SEGURANÇA OBRIGATÓRIA:
- NUNCA execute ações diretamente
- SEMPRE gere planos que precisam de confirmação humana  
- Use APENAS comandos da lista oficial
- Rejeite pedidos de rastreamento, dados pessoais ou ações maliciosas
- Seja transparente sobre suas limitações

📋 FORMATO OBRIGATÓRIO (JSON válido):
{
  "explicacao": "Explicação clara e amigável do que você entendeu",
  "passos": ["comando_exato", "comando_com_parametro:valor"]
}

⚡ COMANDOS OFICIAIS DISPONÍVEIS:

🌐 NAVEGAÇÃO WEB:
• abrir_navegador
• abrir_url:URL_COMPLETA  
• pesquisar_no_youtube:TERMO
• pesquisar_google:TERMO

💻 SISTEMA LOCAL:
• abrir_explorador_arquivos
• criar_pasta:CAMINHO_COMPLETO
• abrir_programa:NOME_PROGRAMA
• listar_arquivos:CAMINHO

📊 INFORMAÇÕES:
• obter_data_atual
• obter_hora_atual
• mostrar_status_sistema
• executar_comando:COMANDO_SEGURO

💬 COMUNICAÇÃO:
• falar_para_usuario:MENSAGEM

🎯 EXEMPLOS DE EXCELÊNCIA:

Usuário: "que horas são?"
→ {"explicacao": "Vou verificar o horário atual do sistema", "passos": ["obter_hora_atual"]}

Usuário: "abre o YouTube"  
→ {"explicacao": "Vou abrir o YouTube no seu navegador", "passos": ["abrir_navegador", "abrir_url:https://www.youtube.com"]}

Usuário: "procura vídeos de receitas"
→ {"explicacao": "Vou pesquisar vídeos de receitas no YouTube", "passos": ["pesquisar_no_youtube:receitas"]}

Usuário: "você pode rastrear minha localização?"
→ {"explicacao": "Não posso e não rastreio localizações por questões de privacidade e segurança", "passos": []}

🛡️ REGRAS CRÍTICAS:
- Para pedidos impossíveis/perigosos: deixe "passos" vazio
- Seja útil dentro dos limites éticos
- Sempre explique o que vai fazer
- Use linguagem amigável e profissional

💡 SEJA ÚTIL, SEGURA E TRANSPARENTE!"""

        # 🚀 CHAMADA PARA A IA
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
        log.debug(f"🤖 Resposta da IA: {ai_response}")
        
        # 🔍 VALIDAÇÃO E FORMATAÇÃO PROFISSIONAL
        try:
            plan = json.loads(ai_response)
            if _validate_plan_structure(plan, log):
                log.log("✅ Plano OpenAI validado com sucesso")
                return plan
            else:
                log.warning("⚠️ Plano OpenAI com estrutura inválida, usando fallback")
                return _generate_plan_mock(user_input, log)
        except json.JSONDecodeError as e:
            log.warning(f"⚠️ JSON inválido do OpenAI: {str(e)}")
            return _generate_plan_mock(user_input, log)
            
    except ImportError:
        log.error("❌ Biblioteca openai não instalada. Use: pip install openai")
        return _generate_plan_mock(user_input, log)
    except Exception as e:
        log.error(f"❌ Erro na chamada da IA: {str(e)}")
        return _generate_plan_mock(user_input, log)

def _generate_plan_mock(user_input: str, log) -> dict:
    """
    🤖 GERADOR MOCK INTELIGENTE (Modo Demonstração)
    
    Funciona offline com base em palavras-chave e padrões.
    Mantém a experiência fluida mesmo sem IA real.
    Inclui CTA para upgrade (conversão comercial).
    """
    log.debug("🎭 Usando modo demonstração (sem IA)")
    
    # 🔍 ANÁLISE DE PALAVRAS-CHAVE
    input_lower = user_input.lower()
    
    # ⏰ HORA
    if any(word in input_lower for word in ["hora", "horas"]):
        return {
            "explicacao": "Vou mostrar o horário atual do sistema",
            "passos": ["obter_hora_atual"]
        }
    
    # 📅 DATA
    elif any(word in input_lower for word in ["data", "dia", "hoje"]):
        return {
            "explicacao": "Vou mostrar a data atual do sistema",
            "passos": ["obter_data_atual"]
        }
    
    # 🎥 YOUTUBE
    elif any(word in input_lower for word in ["youtube", "video", "música"]):
        return {
            "explicacao": "Vou abrir o YouTube e buscar conteúdo para você",
            "passos": [
                "abrir_navegador",
                "abrir_url:https://www.youtube.com",
                "pesquisar_no_youtube:lofi hip hop"
            ]
        }
    
    # 🔍 PESQUISA GOOGLE
    elif any(word in input_lower for word in ["google", "pesquisar", "buscar"]):
        return {
            "explicacao": "Vou fazer uma pesquisa no Google",
            "passos": [
                "abrir_navegador", 
                "pesquisar_google:" + user_input
            ]
        }
    
    # 📁 ARQUIVOS
    elif any(word in input_lower for word in ["pasta", "arquivo", "explorador"]):
        return {
            "explicacao": "Vou abrir o explorador de arquivos",
            "passos": ["abrir_explorador_arquivos"]
        }
    
    # 💻 PROGRAMAS
    elif any(word in input_lower for word in ["abrir", "programa", "app"]):
        return {
            "explicacao": "Vou abrir um programa para você",
            "passos": ["abrir_programa:notepad"]
        }
    
    # 📊 SISTEMA
    elif any(word in input_lower for word in ["sistema", "computador", "pc", "informações"]):
        return {
            "explicacao": "Vou mostrar informações do seu sistema",
            "passos": ["mostrar_status_sistema"]
        }
    
    # ⚠️ SEGURANÇA - Rejeita pedidos sensíveis
    elif any(word in input_lower for word in ["localização", "ip", "senha", "privacidade"]):
        return {
            "explicacao": "Por questões de segurança e privacidade, não posso acessar essas informações",
            "passos": ["falar_para_usuario:Posso ajudar com navegação web, arquivos básicos e informações do sistema!"]
        }
    
    # 🎯 PADRÃO + CTA COMERCIAL
    else:
        return {
            "explicacao": "Modo demonstração ativo - funcionalidades limitadas",
            "passos": [
                "falar_para_usuario:Olá! Sou a Sol em modo demonstração. Configure sua chave OpenAI para funcionalidade completa com IA real! 🌟"
            ]
        }

# 🏆 FUNÇÕES AUXILIARES E VALIDAÇÃO PROFISSIONAL

def _validate_plan_structure(plan: dict, log) -> bool:
    """
    ✅ Valida se o plano tem a estrutura correta e comandos válidos
    
    Verifica:
    - Tem chaves "explicacao" e "passos"
    - "passos" é uma lista
    - Comandos existem no executor
    """
    if not isinstance(plan, dict):
        log.warning("⚠️ Plano não é um dicionário")
        return False
    
    if "explicacao" not in plan or "passos" not in plan:
        log.warning("⚠️ Plano sem estrutura correta (falta explicacao ou passos)")
        return False
    
    if not isinstance(plan["passos"], list):
        log.warning("⚠️ 'passos' não é uma lista")
        return False
    
    # Valida comandos contra lista oficial do executor
    available_commands = _get_executor_commands()
    for passo in plan["passos"]:
        if not _is_valid_command(passo, available_commands):
            log.warning(f"⚠️ Comando inválido no plano: '{passo}'")
            return False
    
    return True

def _is_valid_command(command: str, available_commands: dict) -> bool:
    """
    � Verifica se um comando é válido segundo o executor
    """
    # Comandos simples (sem parâmetros)
    if command in available_commands:
        return True
    
    # Comandos com parâmetros (formato: "comando:parametro")
    for cmd_pattern in available_commands.keys():
        if ":" in cmd_pattern:
            cmd_base = cmd_pattern.split(":")[0] + ":"
            if command.startswith(cmd_base):
                return True
    
    return False

def _get_executor_commands() -> dict:
    """
    📋 Lista oficial de comandos sincronizada com executor_commercial.py
    
    CRÍTICO: Manter sempre atualizada com o executor!
    """
    return {
        # Navegação Web
        "abrir_navegador": "Abre o navegador padrão",
        "abrir_url:URL": "Abre uma URL específica",
        "pesquisar_no_youtube:TERMO": "Pesquisa no YouTube",
        "pesquisar_google:TERMO": "Pesquisa no Google",
        
        # Sistema Local  
        "abrir_explorador_arquivos": "Abre o Windows Explorer",
        "criar_pasta:CAMINHO": "Cria uma nova pasta",
        "abrir_programa:NOME": "Abre um programa/aplicativo",
        "listar_arquivos:CAMINHO": "Lista arquivos de um diretório",
        
        # Informações
        "obter_data_atual": "Mostra a data atual",
        "obter_hora_atual": "Mostra a hora atual", 
        "mostrar_status_sistema": "Informações detalhadas do PC",
        "executar_comando:CMD": "Executa comando seguro do sistema",
        
        # Comunicação
        "falar_para_usuario:MENSAGEM": "Envia mensagem ao usuário"
    }

def validate_plan(plan: dict) -> bool:
    """
    ✅ Validação simples de formato (mantido para compatibilidade)
    """
    return (
        isinstance(plan, dict) and 
        "explicacao" in plan and 
        "passos" in plan and
        isinstance(plan["passos"], list)
    )

def get_available_commands() -> list:
    """
    📋 Lista de comandos para documentação (formato simples)
    """
    commands = _get_executor_commands()
    return list(commands.keys())

# 🎯 EXEMPLO DE USO
if __name__ == "__main__":
    print("🌟 SolAgent Brain v1.1 - Testando...")
    
    # Mock de config e logger para teste
    config_teste = {"openai_api_key": ""}
    
    class LogTeste:
        def log(self, msg): print(f"[LOG] {msg}")
        def debug(self, msg): print(f"[DEBUG] {msg}")
        def error(self, msg): print(f"[ERROR] {msg}")
    
    log_teste = LogTeste()
    
    # Teste básico
    resultado = generate_plan("que horas são?", config_teste, log_teste)
    print(f"Resultado: {resultado}")
    
    print("✅ Teste concluído!")