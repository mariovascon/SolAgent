import os
import webbrowser
import subprocess
import urllib.parse

def execute_steps(steps: list, log, config: dict = None) -> None:
    """
    Executa os passos do plano de ação.
    Se safe_mode estiver ativo, apenas simula as ações.
    """
    safe_mode = True
    if config:
        safe_mode = config.get("safe_mode", True)
    
    if safe_mode:
        log.log("🔒 MODO SEGURO ATIVO - Apenas simulando ações")
    else:
        log.log("⚡ MODO EXECUÇÃO REAL - Executando ações no sistema")
    
    for i, step in enumerate(steps, 1):
        log.log(f"Passo {i}/{len(steps)}: {step}")
        
        try:
            if step == "abrir_navegador":
                _abrir_navegador(log, safe_mode)
                
            elif step.startswith("abrir_url:"):
                url = step.replace("abrir_url:", "")
                _abrir_url(url, log, safe_mode)
                
            elif step.startswith("pesquisar_no_youtube:"):
                termo = step.replace("pesquisar_no_youtube:", "")
                _pesquisar_youtube(termo, log, safe_mode)
                
            elif step.startswith("pesquisar_google:"):
                termo = step.replace("pesquisar_google:", "")
                _pesquisar_google(termo, log, safe_mode)
                
            elif step == "abrir_explorador_arquivos":
                _abrir_explorador(log, safe_mode)
                
            elif step.startswith("criar_pasta:"):
                pasta = step.replace("criar_pasta:", "")
                _criar_pasta(pasta, log, safe_mode)
                
            elif step.startswith("abrir_programa:"):
                programa = step.replace("abrir_programa:", "")
                _abrir_programa(programa, log, safe_mode)
                
            elif step == "interpretar_resposta_ia":
                log.log("Interpretando resposta da IA...")
                
            elif step == "obter_data_atual":
                _obter_data_atual(log, safe_mode)
                
            elif step == "obter_hora_atual":
                _obter_hora_atual(log, safe_mode)
                
            elif step.startswith("falar_para_usuario:"):
                mensagem = step.replace("falar_para_usuario:", "")
                _falar_para_usuario(mensagem, log)
                
            elif step.startswith("listar_arquivos:"):
                caminho = step.replace("listar_arquivos:", "")
                _listar_arquivos(caminho, log, safe_mode)
                
            elif step == "mostrar_status_sistema":
                _mostrar_status_sistema(log, safe_mode)
                
            elif step.startswith("executar_comando:"):
                comando = step.replace("executar_comando:", "")
                _executar_comando_sistema(comando, log, safe_mode)
                
            else:
                log.warning(f"Passo desconhecido: {step}")
                
        except Exception as e:
            log.error(f"Erro ao executar passo '{step}': {str(e)}")

def _abrir_navegador(log, safe_mode):
    log.log("Abrindo navegador padrão...")
    if not safe_mode:
        webbrowser.open("about:blank")

def _abrir_url(url, log, safe_mode):
    log.log(f"Abrindo URL: {url}")
    if not safe_mode:
        webbrowser.open(url)

def _pesquisar_youtube(termo, log, safe_mode):
    termo_encoded = urllib.parse.quote(termo)
    search_url = f"https://www.youtube.com/results?search_query={termo_encoded}"
    log.log(f"Pesquisando no YouTube: {termo}")
    if not safe_mode:
        webbrowser.open(search_url)

def _pesquisar_google(termo, log, safe_mode):
    termo_encoded = urllib.parse.quote(termo)
    search_url = f"https://www.google.com/search?q={termo_encoded}"
    log.log(f"Pesquisando no Google: {termo}")
    if not safe_mode:
        webbrowser.open(search_url)

def _abrir_explorador(log, safe_mode):
    log.log("Abrindo explorador de arquivos...")
    if not safe_mode:
        os.system("start explorer")

def _criar_pasta(pasta, log, safe_mode):
    log.log(f"Criando pasta em: {pasta}")
    if not safe_mode:
        try:
            os.makedirs(pasta, exist_ok=True)
            log.log(f"✅ Pasta criada com sucesso: {pasta}")
        except Exception as e:
            log.error(f"Erro ao criar pasta: {str(e)}")

def _abrir_programa(programa, log, safe_mode):
    log.log(f"Abrindo programa: {programa}")
    if not safe_mode:
        try:
            # Tenta abrir programas comuns
            programas_comuns = {
                "notepad": "notepad.exe",
                "calculadora": "calc.exe",
                "paint": "mspaint.exe",
                "cmd": "cmd.exe",
                "powershell": "powershell.exe"
            }
            
            comando = programas_comuns.get(programa.lower(), programa)
            subprocess.Popen(comando, shell=True)
            log.log(f"✅ Programa {programa} aberto com sucesso")
        except Exception as e:
            log.error(f"Erro ao abrir programa {programa}: {str(e)}")

def _obter_data_atual(log, safe_mode):
    """Obtém e exibe a data atual do sistema"""
    from datetime import datetime
    hoje = datetime.now().strftime("%d/%m/%Y")
    log.log(f"Data atual detectada: {hoje}")
    print(f"🌟 Sol: Hoje é {hoje}")

def _obter_hora_atual(log, safe_mode):
    """Obtém e exibe a hora atual do sistema"""
    from datetime import datetime
    agora = datetime.now().strftime("%H:%M:%S")
    log.log(f"Hora atual detectada: {agora}")
    print(f"🌟 Sol: Agora são {agora}")

def _falar_para_usuario(mensagem, log):
    """Fala diretamente com o usuário"""
    log.log(f"Respondendo ao usuário: {mensagem}")
    print(f"🌟 Sol: {mensagem}")

def _listar_arquivos(caminho, log, safe_mode):
    """Lista arquivos em um diretório"""
    log.log(f"Listando arquivos em: {caminho}")
    if not safe_mode:
        try:
            import os
            if os.path.exists(caminho):
                arquivos = os.listdir(caminho)
                print(f"🌟 Sol: Encontrei {len(arquivos)} itens em {caminho}:")
                for arquivo in arquivos[:10]:  # Mostra só os primeiros 10
                    print(f"  📁 {arquivo}")
                if len(arquivos) > 10:
                    print(f"  ... e mais {len(arquivos) - 10} itens")
            else:
                print(f"🌟 Sol: O caminho {caminho} não existe")
        except Exception as e:
            log.error(f"Erro ao listar arquivos: {str(e)}")
    else:
        print(f"🌟 Sol: (Modo seguro) Simulando listagem de arquivos em {caminho}")

def _mostrar_status_sistema(log, safe_mode):
    """Mostra informações básicas do sistema"""
    log.log("Coletando informações do sistema...")
    try:
        import platform
        import psutil
        from datetime import datetime
        
        sistema = platform.system()
        versao = platform.version()
        processador = platform.processor()
        memoria = psutil.virtual_memory()
        disco = psutil.disk_usage('/')
        
        print("🌟 Sol: Aqui estão as informações do seu sistema:")
        print(f"  💻 Sistema: {sistema}")
        print(f"  🔧 Processador: {processador}")
        print(f"  🧠 Memória: {round(memoria.total / (1024**3), 1)}GB total, {round(memoria.available / (1024**3), 1)}GB disponível")
        print(f"  💾 Disco: {round(disco.total / (1024**3), 1)}GB total, {round(disco.free / (1024**3), 1)}GB livre")
        print(f"  📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
    except Exception as e:
        log.error(f"Erro ao obter status do sistema: {str(e)}")
        print("🌟 Sol: Não consegui obter todas as informações do sistema")

def _executar_comando_sistema(comando, log, safe_mode):
    """Executa comandos seguros do sistema"""
    log.log(f"Comando solicitado: {comando}")
    
    # Lista de comandos seguros permitidos
    comandos_seguros = {
        "ipconfig": "ipconfig",
        "dir": "dir",
        "date": "date /t",
        "time": "time /t",
        "systeminfo": "systeminfo | findstr /C:\"OS Name\" /C:\"Total Physical Memory\"",
        "tasklist": "tasklist | findstr /V \"Image Name\""
    }
    
    if comando.lower() in comandos_seguros:
        if not safe_mode:
            try:
                import subprocess
                resultado = subprocess.run(comandos_seguros[comando.lower()], 
                                        shell=True, capture_output=True, text=True, timeout=10)
                print(f"🌟 Sol: Resultado do comando '{comando}':")
                print(resultado.stdout)
            except Exception as e:
                log.error(f"Erro ao executar comando: {str(e)}")
                print("🌟 Sol: Houve um erro ao executar o comando")
        else:
            print(f"🌟 Sol: (Modo seguro) Simulando execução do comando '{comando}'")
    else:
        log.warning(f"Comando não permitido ou desconhecido: {comando}")
        print(f"🌟 Sol: Desculpe, o comando '{comando}' não é permitido por segurança")