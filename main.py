"""
⚡ SolAgent v1.2 - Loop Principal com Suporte a Voz
==================================================

Interface principal: texto + voz integrados
Compatibilidade total com versões anteriores

Novidades v1.2:
- Entrada por voz (push-to-talk)
- Saída por voz (TTS)
- Modo híbrido texto/voz
- Fallback automático

Autores: Mario, GitHub Copilot & Sol (ela mesma ajudou a se criar!)
Versão: 1.2 (Audio Revolution) - Tríade Criativa
Data: 28/10/2025
"""

import json
from core import brain_commercial as brain, executor_commercial as executor, confirm, logger

# Sistema de áudio + histórico - com fallback gracioso
try:
    from core.audio_input import AudioInput
    from core.audio_output import AudioOutput
    AUDIO_SYSTEM_AVAILABLE = True
except ImportError:
    AUDIO_SYSTEM_AVAILABLE = False

try:
    from core.command_history import CommandHistory
    HISTORY_SYSTEM_AVAILABLE = True
except ImportError:
    HISTORY_SYSTEM_AVAILABLE = False

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    config = load_config()
    log = logger.Logger(debug_mode=config.get("debug_mode", False))
    
    # 🎤 Inicializa sistemas de áudio
    audio_input = None
    audio_output = None
    
    if AUDIO_SYSTEM_AVAILABLE:
        try:
            audio_input = AudioInput(config, log)
            audio_output = AudioOutput(config, log)
            log.log("🎵 Sistemas de áudio inicializados")
        except Exception as e:
            log.warning(f"⚠️ Erro ao inicializar áudio: {str(e)}")
    
    # 📊 Inicializa sistema de histórico
    command_history = None
    
    if HISTORY_SYSTEM_AVAILABLE:
        try:
            command_history = CommandHistory(config, log)
            log.log("📊 Sistema de histórico inicializado")
        except Exception as e:
            log.warning(f"⚠️ Erro ao inicializar histórico: {str(e)}")
    
    # 🌟 Banner de inicialização
    print("🌟 ═══════════════════════════════════════════════════════════")
    print("🌟   SolAgent v1.2 - Assistente Inteligente com Voz")
    print("🌟 ═══════════════════════════════════════════════════════════")
    
    # 📊 Status de sistemas
    safe_mode = config.get("safe_mode", True)
    openai_configured = config.get("openai_api_key", "").strip() not in ["", "COLE_SUA_CHAVE_AQUI"]
    voice_input_available = audio_input and audio_input.is_available()
    voice_output_available = audio_output and audio_output.is_available()
    
    print("\n� Status dos Sistemas:")
    print(f"  🔒 Modo: {'SEGURO (simulação)' if safe_mode else 'EXECUÇÃO REAL'}")
    print(f"  🧠 IA: {'OpenAI configurada' if openai_configured else 'Modo demonstração'}")
    print(f"  🎤 Entrada de voz: {'✅ Disponível' if voice_input_available else '❌ Indisponível'}")  
    print(f"  🔊 Saída de voz: {'✅ Disponível' if voice_output_available else '❌ Indisponível'}")
    
    # 💡 Instruções
    if voice_input_available:
        push_key = config.get("push_to_talk_key", "space").upper()
        print(f"\n💡 Como usar:")
        print(f"  🎤 Pressione e segure '{push_key}' para falar")
        print(f"  ✍️ Ou digite normalmente")
        print(f"  📝 Comandos especiais: 'sair', 'config', 'modo', 'teste_audio', 'historico'")
    else:
        print(f"\n💡 Digite comandos em linguagem natural.")
        print(f"    Exemplo: 'abre o YouTube e procura lo-fi'")
        print(f"  📝 Comandos: 'sair', 'config', 'modo', 'historico'")
        
        if AUDIO_SYSTEM_AVAILABLE:
            print(f"  🎵 Para ativar voz, instale: pip install sounddevice soundfile numpy openai-whisper keyboard pyttsx3")

    # 🔄 Loop principal híbrido (texto + voz)
    while True:
        user_input = None
        
        # 🎯 Captura entrada (voz ou texto)
        if voice_input_available:
            user_input = audio_input.listen_for_command(timeout=30)
        
        # Fallback texto se não capturou voz
        if not user_input:
            try:
                user_input = input("\n💬 Você: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n🌟 Sol: Até mais! 💛✨")
                break
        
        # 🚪 Comandos de saída
        if user_input.lower() in ["sair", "exit", "quit", "tchau", "bye"]:
            farewell_msg = "Até mais! Foi um prazer ajudar você! 💛✨"
            print(f"🌟 Sol: {farewell_msg}")
            if voice_output_available:
                audio_output.speak(farewell_msg)
            break
            
        # ⚙️ Comandos especiais
        elif user_input.lower() == "config":
            show_config_status(config, voice_input_available, voice_output_available)
            continue
            
        elif user_input.lower() == "modo":
            config = toggle_safe_mode(config, log)
            continue
            
        elif user_input.lower() == "teste_audio":
            test_audio_systems(audio_input, audio_output)
            continue
            
        elif user_input.lower() in ["historico", "histórico", "stats", "relatorio"]:
            show_history_report(command_history)
            continue
        
        if not user_input:
            continue

        # 🧠 Processamento principal
        execution_result = "unknown"
        input_method = "voice" if voice_input_available and user_input else "text"
        response_method = "both" if voice_output_available else "text"
        
        try:
            plan = brain.generate_plan(user_input, config, log)
            
            # 🗣️ Resposta da Sol (visual + voz)
            response_text = plan['explicacao']
            print(f"\n🌟 Sol: {response_text}")
            
            if voice_output_available:
                audio_output.speak(response_text)
            
            # 📝 Mostra plano de ação
            if plan["passos"]:
                print("\n📝 Plano de ação:")
                for i, step in enumerate(plan["passos"], start=1):
                    print(f"  {i}. {step}")

                # 🤔 Confirmação (com voz se disponível)
                if confirm.ask_user_confirmation():
                    execution_msg = "Perfeito! Executando agora..."
                    print(f"\n⚡ {execution_msg}")
                    
                    if voice_output_available:
                        audio_output.speak("Executando!")
                    
                    executor.execute_steps(plan["passos"], log, config)
                    
                    completion_msg = "Pronto! Tarefa concluída com sucesso!"
                    print(f"✅ {completion_msg}")
                    
                    if voice_output_available:
                        audio_output.speak("Concluído!")
                    
                    execution_result = "success"
                        
                else:
                    cancel_msg = "Tudo bem, não executei nada."
                    print(f"❌ {cancel_msg}")
                    
                    if voice_output_available:
                        audio_output.speak("Operação cancelada.")
                    
                    execution_result = "cancelled"
            else:
                # Sem ações - só resposta
                execution_result = "info_only"
                    
        except Exception as e:
            error_msg = f"Ops! Houve um erro: {str(e)}"
            log.error(f"Erro durante execução: {str(e)}")
            print(f"❌ {error_msg}")
            
            if voice_output_available:
                audio_output.speak("Desculpe, houve um erro. Tente novamente.")
            
            execution_result = "error"
        
        # 📊 Salva no histórico
        if command_history:
            command_history.save_interaction(
                user_input, 
                plan if 'plan' in locals() else {"explicacao": "Erro", "passos": []},
                execution_result,
                input_method,
                response_method
            )

def show_config_status(config, voice_input_available=False, voice_output_available=False):
    """📊 Mostra status completo do sistema"""
    print("\n⚙️ ═══ STATUS DA SOLAGENT v1.2 ═══")
    print(f"  🔒 Modo seguro: {'ATIVO (simulação)' if config.get('safe_mode', True) else 'EXECUÇÃO REAL'}")
    print(f"  🧠 OpenAI API: {'Configurada' if config.get('openai_api_key', '').strip() not in ['', 'COLE_SUA_CHAVE_AQUI'] else 'Modo demonstração'}")
    print(f"  🔍 Debug: {'ATIVO' if config.get('debug_mode', False) else 'DESATIVO'}")
    print(f"  🎤 Entrada voz: {'✅ Funcionando' if voice_input_available else '❌ Indisponível'}")
    print(f"  🔊 Saída voz: {'✅ Funcionando' if voice_output_available else '❌ Indisponível'}")
    
    if voice_input_available:
        push_key = config.get('push_to_talk_key', 'space')
        whisper_model = config.get('whisper_model', 'tiny')
        print(f"  🎯 Push-to-talk: '{push_key.upper()}'")
        print(f"  🧠 Modelo Whisper: '{whisper_model}'")
    
    if voice_output_available:
        tts_engine = config.get('tts_engine', 'auto')
        voice_speed = config.get('voice_speed', 1.0)
        print(f"  🎵 Engine TTS: '{tts_engine}'")
        print(f"  ⚡ Velocidade voz: {voice_speed}x")

def toggle_safe_mode(config, log):
    current_safe_mode = config.get("safe_mode", True)
    new_safe_mode = not current_safe_mode
    
    if new_safe_mode:
        print("🔒 Modo seguro ATIVADO - ações serão apenas simuladas")
    else:
        print("⚠️ ATENÇÃO: Modo execução REAL ativado!")
        print("   Ações serão executadas no seu sistema.")
        confirm_real = input("   Tem certeza? (digite 'CONFIRMO' para ativar): ").strip()
        if confirm_real != "CONFIRMO":
            print("🔒 Mantendo modo seguro ativo por segurança")
            new_safe_mode = True
        else:
            print("⚡ Modo execução REAL ativado!")
    
    config["safe_mode"] = new_safe_mode
    
    # Salva a configuração
    try:
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        log.log(f"Modo seguro alterado para: {new_safe_mode}")
    except Exception as e:
        log.error(f"Erro ao salvar configuração: {str(e)}")
    
    return config

def test_audio_systems(audio_input, audio_output):
    """🧪 Testa sistemas de áudio completos"""
    print("\n🧪 ═══ TESTE DE SISTEMAS DE ÁUDIO ═══")
    
    # Teste entrada
    if audio_input:
        print("\n🎤 Testando entrada de voz...")
        if audio_input.test_audio_system():
            print("✅ Sistema de entrada OK")
        else:
            print("❌ Sistema de entrada com problemas")
    else:
        print("❌ Sistema de entrada não inicializado")
    
    # Teste saída  
    if audio_output:
        print("\n🔊 Testando saída de voz...")
        if audio_output.test_tts_system():
            print("✅ Sistema de saída OK")
        else:
            print("❌ Sistema de saída com problemas")
    else:
        print("❌ Sistema de saída não inicializado")
    
    print("\n🎯 Teste concluído!")

def show_history_report(command_history):
    """📊 Mostra relatório completo de histórico"""
    print("\n📊 ═══ RELATÓRIO DE USO ═══")
    
    if not command_history:
        print("❌ Sistema de histórico não disponível")
        return
    
    try:
        # Relatório completo
        report = command_history.generate_report()
        print(report)
        
        # Estatísticas rápidas
        today_stats = command_history.get_today_stats()
        print(f"\n🎯 RESUMO RÁPIDO:")
        print(f"  • Comandos hoje: {today_stats.get('total_commands', 0)}")
        print(f"  • Taxa de sucesso: {today_stats.get('success_rate', 0):.1f}%")
        
        # Comandos recentes
        recent = command_history.get_recent_commands(3)
        if recent:
            print(f"\n📋 ÚLTIMOS COMANDOS:")
            for cmd in recent:
                status = "✅" if cmd["result"] == "success" else "❌" if cmd["result"] == "error" else "⏸️"
                method = "🎤" if cmd["method"] == "voice" else "✍️"
                print(f"  {status} {method} {cmd['time']} - {cmd['input']}")
        
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {str(e)}")

if __name__ == "__main__":
    main()