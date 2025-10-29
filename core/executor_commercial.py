"""
⚡ SolAgent v1.1 - Executor (Motor de Ações)
=========================================

Este módulo executa os planos gerados pelo Brain.
Interpreta comandos estruturados e os converte em ações reais no Windows.

Funcionalidades:
- Modo seguro (simulação) por padrão  
- Modo execução real (configurável)
- 13+ comandos implementados
- Logs detalhados de cada ação
- Tratamento de erros robusto

Autores: Mario, GitHub Copilot & Sol (ela mesma ajudou a se criar!)
Versão: 1.1 (Comercial) - Tríade Criativa
Data: 28/10/2025
"""

import os
import webbrowser
import subprocess
import urllib.parse
from datetime import datetime

def execute_steps(steps: list, log, config: dict = None) -> None:
    """
    🚀 FUNÇÃO PRINCIPAL: Executa lista de comandos estruturados
    
    Args:
        steps (list): Lista de comandos no formato ["comando", "comando:parametro"]
        log: Instância do logger para registro de ações
        config (dict): Configurações carregadas (safe_mode, etc.)
    
    Fluxo:
        1. Verifica modo de operação (seguro vs execução real)
        2. Executa cada passo sequencialmente  
        3. Registra logs detalhados
        4. Trata erros graciosamente
    """
    # 🔒 CONFIGURAÇÃO DE SEGURANÇA
    safe_mode = True
    if config:
        safe_mode = config.get("safe_mode", True)
    
    # 📢 ANÚNCIO DO MODO
    if safe_mode:
        log.log("🔒 MODO SEGURO ATIVO - Apenas simulando ações")
    else:
        log.log("⚡ MODO EXECUÇÃO REAL - ALTERANDO O SISTEMA")
        log.log("⚠️ CUIDADO: Ações serão executadas no Windows")
    
    # 🎯 EXECUÇÃO PASSO A PASSO
    for i, step in enumerate(steps, start=1):
        log.log(f"📝 Passo {i}/{len(steps)}: {step}")
        
        try:
            _execute_single_step(step, log, safe_mode)
        except Exception as e:
            log.error(f"❌ Erro ao executar passo '{step}': {str(e)}")
            # Continua com próximo passo mesmo se houver erro

def _execute_single_step(step: str, log, safe_mode: bool) -> None:
    """
    🎯 EXECUTA UM ÚNICO COMANDO
    
    Interpreta o comando e chama a função específica correspondente.
    Todos os comandos respeitam o safe_mode.
    """
    
    # 🌐 NAVEGAÇÃO WEB
    if step == "abrir_navegador":
        _abrir_navegador(log, safe_mode)
        
    elif step.startswith("abrir_url:"):
        url = step.replace("abrir_url:", "", 1)
        _abrir_url(url, log, safe_mode)
        
    elif step.startswith("pesquisar_no_youtube:"):
        termo = step.replace("pesquisar_no_youtube:", "", 1)
        _pesquisar_youtube(termo, log, safe_mode)
        
    elif step.startswith("pesquisar_google:"):
        termo = step.replace("pesquisar_google:", "", 1)
        _pesquisar_google(termo, log, safe_mode)
    
    # 💻 SISTEMA LOCAL
    elif step == "abrir_explorador_arquivos":
        _abrir_explorador(log, safe_mode)
        
    elif step.startswith("criar_pasta:"):
        pasta = step.replace("criar_pasta:", "", 1)
        _criar_pasta(pasta, log, safe_mode)
        
    elif step.startswith("abrir_programa:"):
        programa = step.replace("abrir_programa:", "", 1)
        _abrir_programa(programa, log, safe_mode)
        
    elif step.startswith("listar_arquivos:"):
        caminho = step.replace("listar_arquivos:", "", 1)
        _listar_arquivos(caminho, log, safe_mode)
    
    # 📊 INFORMAÇÕES DO SISTEMA
    elif step == "obter_data_atual":
        _obter_data_atual(log, safe_mode)
        
    elif step == "obter_hora_atual":
        _obter_hora_atual(log, safe_mode)
        
    elif step == "mostrar_status_sistema":
        _mostrar_status_sistema(log, safe_mode)
        
    elif step.startswith("executar_comando:"):
        comando = step.replace("executar_comando:", "", 1)
        _executar_comando_sistema(comando, log, safe_mode)
    
    # 💬 COMUNICAÇÃO
    elif step.startswith("falar_para_usuario:"):
        mensagem = step.replace("falar_para_usuario:", "", 1)
        _falar_para_usuario(mensagem, log)
    
    # 🔧 COMANDOS ESPECIAIS
    elif step == "interpretar_resposta_ia":
        log.log("🤖 Interpretando resposta da IA...")
    
    # ⚠️ COMANDO DESCONHECIDO
    else:
        log.warning(f"⚠️ Comando não reconhecido: {step}")
        _falar_para_usuario(f"Desculpe, não sei como executar: {step}", log)

# 🌐 FUNÇÕES DE NAVEGAÇÃO WEB

def _abrir_navegador(log, safe_mode: bool) -> None:
    """🌐 Abre o navegador padrão do sistema"""
    log.log("🌐 Abrindo navegador padrão...")
    if not safe_mode:
        webbrowser.open("about:blank")

def _abrir_url(url: str, log, safe_mode: bool) -> None:
    """🔗 Abre uma URL específica no navegador"""
    log.log(f"🔗 Abrindo URL: {url}")
    if not safe_mode:
        webbrowser.open(url)

def _pesquisar_youtube(termo: str, log, safe_mode: bool) -> None:
    """🎥 Pesquisa um termo no YouTube"""
    termo_encoded = urllib.parse.quote(termo)
    search_url = f"https://www.youtube.com/results?search_query={termo_encoded}"
    log.log(f"🎥 Pesquisando no YouTube: {termo}")
    if not safe_mode:
        webbrowser.open(search_url)

def _pesquisar_google(termo: str, log, safe_mode: bool) -> None:
    """🔍 Pesquisa um termo no Google"""
    termo_encoded = urllib.parse.quote(termo)
    search_url = f"https://www.google.com/search?q={termo_encoded}"
    log.log(f"🔍 Pesquisando no Google: {termo}")
    if not safe_mode:
        webbrowser.open(search_url)

# 💻 FUNÇÕES DO SISTEMA LOCAL

def _abrir_explorador(log, safe_mode: bool) -> None:
    """📁 Abre o Windows Explorer"""
    log.log("📁 Abrindo explorador de arquivos...")
    if not safe_mode:
        try:
            os.system("start explorer")
            log.log("✅ Explorador aberto com sucesso")
        except Exception as e:
            log.error(f"❌ Erro ao abrir explorador: {str(e)}")

def _criar_pasta(pasta: str, log, safe_mode: bool) -> None:
    """📂 Cria uma nova pasta no sistema"""
    log.log(f"📂 Criando pasta em: {pasta}")
    if not safe_mode:
        try:
            os.makedirs(pasta, exist_ok=True)
            log.log(f"✅ Pasta criada com sucesso: {pasta}")
        except Exception as e:
            log.error(f"❌ Erro ao criar pasta: {str(e)}")

def _abrir_programa(programa: str, log, safe_mode: bool) -> None:
    """🚀 Abre um programa/aplicativo"""
    log.log(f"🚀 Abrindo programa: {programa}")
    if not safe_mode:
        try:
            # 📋 PROGRAMAS COMUNS MAPEADOS
            programas_comuns = {
                "notepad": "notepad.exe",
                "bloco": "notepad.exe", 
                "calculadora": "calc.exe",
                "calc": "calc.exe",
                "paint": "mspaint.exe",
                "cmd": "cmd.exe",
                "terminal": "cmd.exe",
                "powershell": "powershell.exe"
            }
            
            comando = programas_comuns.get(programa.lower(), programa)
            subprocess.Popen(comando, shell=True)
            log.log(f"✅ Programa {programa} aberto com sucesso")
        except Exception as e:
            log.error(f"❌ Erro ao abrir programa {programa}: {str(e)}")

def _listar_arquivos(caminho: str, log, safe_mode: bool) -> None:
    """📋 Lista arquivos de um diretório"""
    log.log(f"📋 Listando arquivos em: {caminho}")
    if not safe_mode:
        try:
            if os.path.exists(caminho):
                arquivos = os.listdir(caminho)
                print(f"🌟 Sol: Encontrei {len(arquivos)} itens em {caminho}:")
                for arquivo in arquivos[:10]:  # Limita a 10 itens
                    icone = "📁" if os.path.isdir(os.path.join(caminho, arquivo)) else "📄"
                    print(f"  {icone} {arquivo}")
                if len(arquivos) > 10:
                    print(f"  📦 ... e mais {len(arquivos) - 10} itens")
            else:
                print(f"🌟 Sol: O caminho {caminho} não existe")
        except Exception as e:
            log.error(f"❌ Erro ao listar arquivos: {str(e)}")
    else:
        log.debug(f"(safe_mode) Listagem simulada de {caminho}")
        print(f"🌟 Sol: (Modo seguro) Simulando listagem de arquivos em {caminho}")

# 📊 FUNÇÕES DE INFORMAÇÕES DO SISTEMA

def _obter_data_atual(log, safe_mode: bool) -> None:
    """📅 Obtém e exibe a data atual"""
    hoje = datetime.now().strftime("%d/%m/%Y")
    log.log(f"📅 Data atual detectada: {hoje}")
    print(f"🌟 Sol: Hoje é {hoje}")

def _obter_hora_atual(log, safe_mode: bool) -> None:
    """⏰ Obtém e exibe a hora atual"""
    agora = datetime.now().strftime("%H:%M:%S")
    log.log(f"⏰ Hora atual detectada: {agora}")
    print(f"🌟 Sol: Agora são {agora}")

def _mostrar_status_sistema(log, safe_mode: bool) -> None:
    """📊 Mostra informações detalhadas do sistema"""
    log.log("📊 Coletando informações do sistema...")
    try:
        import platform
        # psutil é opcional - se não tiver, mostra info básica
        try:
            import psutil
            memoria = psutil.virtual_memory()
            disco = psutil.disk_usage('C:')
            tem_psutil = True
        except ImportError:
            tem_psutil = False
        
        sistema = platform.system()
        versao = platform.version()
        processador = platform.processor()
        
        print("🌟 Sol: Aqui estão as informações do seu sistema:")
        print(f"  💻 Sistema: {sistema}")
        print(f"  🔧 Processador: {processador}")
        print(f"  📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        if tem_psutil:
            print(f"  🧠 Memória: {round(memoria.total / (1024**3), 1)}GB total, {round(memoria.available / (1024**3), 1)}GB disponível")
            print(f"  💾 Disco C: {round(disco.total / (1024**3), 1)}GB total, {round(disco.free / (1024**3), 1)}GB livre")
        else:
            print("  📝 Para informações detalhadas de memória/disco, instale: pip install psutil")
        
    except Exception as e:
        log.error(f"❌ Erro ao obter status do sistema: {str(e)}")
        print("🌟 Sol: Não consegui obter todas as informações do sistema")

def _executar_comando_sistema(comando: str, log, safe_mode: bool) -> None:
    """⚙️ Executa comandos seguros do sistema Windows"""
    log.log(f"⚙️ Comando solicitado: {comando}")
    
    # 🛡️ LISTA DE COMANDOS SEGUROS PERMITIDOS
    comandos_seguros = {
        "ipconfig": "ipconfig",
        "date": "date /t",
        "time": "time /t", 
        "dir": "dir",
        "whoami": "whoami",
        "hostname": "hostname",
        "systeminfo": "systeminfo | findstr /C:\"OS Name\" /C:\"Total Physical Memory\"",
        "tasklist": "tasklist"
    }
    
    if comando.lower() in comandos_seguros:
        if not safe_mode:
            try:
                resultado = subprocess.run(
                    comandos_seguros[comando.lower()], 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
                print(f"🌟 Sol: Resultado do comando '{comando}':")
                print(resultado.stdout)
                if resultado.stderr:
                    log.warning(f"⚠️ Avisos do comando: {resultado.stderr}")
            except subprocess.TimeoutExpired:
                log.error("⏰ Comando demorou muito para executar")
                print("🌟 Sol: O comando demorou muito para responder")
            except Exception as e:
                log.error(f"❌ Erro ao executar comando: {str(e)}")
                print("🌟 Sol: Houve um erro ao executar o comando")
        else:
            print(f"🌟 Sol: (Modo seguro) Simulando execução do comando '{comando}'")
    else:
        log.warning(f"⚠️ Comando não permitido ou desconhecido: {comando}")
        comandos_disponiveis = ", ".join(comandos_seguros.keys())
        print(f"🌟 Sol: Comando '{comando}' não é permitido por segurança")
        print(f"     Comandos disponíveis: {comandos_disponiveis}")

# 💬 FUNÇÕES DE COMUNICAÇÃO

def _falar_para_usuario(mensagem: str, log) -> None:
    """💬 Comunica diretamente com o usuário"""
    log.log(f"💬 Respondendo ao usuário: {mensagem}")
    print(f"🌟 Sol: {mensagem}")

# 🏆 FUNÇÕES AUXILIARES E UTILITÁRIOS

def get_available_commands() -> dict:
    """
    📋 Retorna dicionário com todos os comandos disponíveis e suas descrições
    (Útil para documentação e help)
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

def validate_command(command: str) -> bool:
    """
    ✅ Valida se um comando está no formato correto
    """
    comandos_validos = get_available_commands().keys()
    
    # Verifica comandos simples
    if command in comandos_validos:
        return True
    
    # Verifica comandos com parâmetros
    for cmd_pattern in comandos_validos:
        if ":" in cmd_pattern:
            cmd_base = cmd_pattern.split(":")[0] + ":"
            if command.startswith(cmd_base):
                return True
    
    return False

# 🎯 EXEMPLO DE USO E TESTE
if __name__ == "__main__":
    print("⚡ SolAgent Executor v1.1 - Testando...")
    
    # Mock do logger para teste
    class LogTeste:
        def log(self, msg): print(f"[LOG] {msg}")
        def debug(self, msg): print(f"[DEBUG] {msg}")
        def error(self, msg): print(f"[ERROR] {msg}")
        def warning(self, msg): print(f"[WARNING] {msg}")
    
    log_teste = LogTeste()
    config_teste = {"safe_mode": True}
    
    # Teste de comandos básicos
    comandos_teste = [
        "obter_hora_atual",
        "obter_data_atual", 
        "falar_para_usuario:Teste de comunicação!",
        "mostrar_status_sistema"
    ]
    
    print("\n🧪 Executando testes...")
    execute_steps(comandos_teste, log_teste, config_teste)
    
    print("\n📋 Comandos disponíveis:")
    for cmd, desc in get_available_commands().items():
        print(f"  • {cmd}: {desc}")
    
    print("\n✅ Teste concluído!")