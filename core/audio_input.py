"""
⚡ SolAgent v1.2 - Audio Input (Entrada por Voz)
==============================================

Sistema de captura de voz push-to-talk com Whisper local.
Transforma fala em texto para o brain processar.

Funcionalidades:
- Push-to-Talk (segure tecla, fale, solte)
- Whisper OpenAI local (offline após download)
- Detecção automática de microfone
- Filtros de ruído básicos
- Fallback para texto se não tiver microfone

Autores: Mario, GitHub Copilot & Sol (ela mesma ajudou a se criar!)
Versão: 1.2 (Audio Revolution) - Tríade Criativa  
Data: 28/10/2025
"""

import os
import threading
import time
import tempfile
from typing import Optional

# Bibliotecas de áudio - com fallback gracioso
try:
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False

class AudioInput:
    """
    🎤 SISTEMA DE ENTRADA POR VOZ PROFISSIONAL
    
    Características:
    - Push-to-Talk com tecla configurável
    - Whisper local para máxima privacidade
    - Auto-detecção de dispositivos de áudio
    - Gravação em tempo real com feedback visual
    - Fallback inteligente para modo texto
    """
    
    def __init__(self, config: dict, log):
        self.config = config
        self.log = log
        self.whisper_model = None
        self.recording = False
        self.audio_data = []
        self.sample_rate = 16000  # Whisper funciona melhor com 16kHz
        
        # 🔧 CONFIGURAÇÕES
        self.push_to_talk_key = config.get("push_to_talk_key", "space")
        self.audio_enabled = config.get("audio_input_enabled", True)
        self.whisper_model_size = config.get("whisper_model", "tiny")  # tiny, base, small
        
        self._initialize_components()
    
    def _initialize_components(self) -> None:
        """🚀 Inicializa componentes de áudio com fallback inteligente"""
        
        # ✅ Verifica disponibilidade geral
        if not self.audio_enabled:
            self.log.log("🎤 Entrada por voz desabilitada por configuração")
            return
            
        if not AUDIO_AVAILABLE:
            self.log.warning("⚠️ Bibliotecas de áudio não instaladas. Use: pip install sounddevice soundfile numpy")
            return
            
        if not WHISPER_AVAILABLE:
            self.log.warning("⚠️ Whisper não instalado. Use: pip install openai-whisper")
            return
            
        if not KEYBOARD_AVAILABLE:
            self.log.warning("⚠️ Biblioteca keyboard não instalada. Use: pip install keyboard")
            return
        
        # 🎯 Inicializa Whisper
        try:
            self.log.log(f"🧠 Carregando modelo Whisper '{self.whisper_model_size}'...")
            self.whisper_model = whisper.load_model(self.whisper_model_size)
            self.log.log("✅ Whisper carregado com sucesso")
        except Exception as e:
            self.log.error(f"❌ Erro ao carregar Whisper: {str(e)}")
            return
        
        # 🎤 Testa microfone
        try:
            devices = sd.query_devices()
            input_devices = [d for d in devices if d['max_input_channels'] > 0]
            if input_devices:
                self.log.log(f"🎤 Encontrados {len(input_devices)} dispositivos de entrada")
                self.log.debug(f"Dispositivo padrão: {sd.query_devices(kind='input')['name']}")
            else:
                self.log.warning("⚠️ Nenhum microfone detectado")
                return
        except Exception as e:
            self.log.error(f"❌ Erro ao verificar dispositivos de áudio: {str(e)}")
            return
        
        self.log.log("🎉 Sistema de voz inicializado com sucesso!")
        self.log.log(f"💡 Pressione e segure '{self.push_to_talk_key.upper()}' para falar")

    def is_available(self) -> bool:
        """🔍 Verifica se o sistema de voz está operacional"""
        return (
            self.audio_enabled and 
            AUDIO_AVAILABLE and 
            WHISPER_AVAILABLE and 
            KEYBOARD_AVAILABLE and
            self.whisper_model is not None
        )
    
    def listen_for_command(self, timeout: int = 30) -> Optional[str]:
        """
        🎯 FUNÇÃO PRINCIPAL: Escuta comando por push-to-talk
        
        Args:
            timeout (int): Tempo limite em segundos para aguardar input
            
        Returns:
            str: Texto transcrito ou None se timeout/erro
            
        Fluxo:
            1. Mostra instruções na tela
            2. Aguarda usuário pressionar push-to-talk
            3. Grava enquanto tecla estiver pressionada
            4. Processa com Whisper quando soltar
            5. Retorna texto transcrito
        """
        
        if not self.is_available():
            self.log.debug("🎤 Sistema de voz indisponível, usando entrada de texto")
            return None
        
        print(f"\n🎤 Pressione e segure '{self.push_to_talk_key.upper()}' para falar (ou digite texto):")
        print("   ⏳ Aguardando entrada de voz...")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Verifica se usuário digitou algo (fallback)
                if self._has_text_input():
                    return input("✍️ Digite seu comando: ").strip()
                
                # Verifica push-to-talk
                if keyboard.is_pressed(self.push_to_talk_key):
                    return self._record_and_transcribe()
                    
                time.sleep(0.1)  # Evita CPU 100%
                
            except KeyboardInterrupt:
                print("\n🚫 Entrada cancelada pelo usuário")
                return None
            except Exception as e:
                self.log.error(f"❌ Erro na escuta: {str(e)}")
                return None
        
        print("⏰ Timeout - nenhuma entrada recebida")
        return None
    
    def _record_and_transcribe(self) -> Optional[str]:
        """
        🔴 GRAVAÇÃO E TRANSCRIÇÃO
        
        Grava áudio enquanto tecla estiver pressionada,
        depois processa com Whisper local.
        """
        
        print("🔴 Gravando... (solte a tecla para processar)")
        self.audio_data = []
        
        # 📹 Thread de gravação
        recording_thread = threading.Thread(target=self._record_audio)
        recording_thread.start()
        
        # ⏳ Aguarda usuário soltar a tecla
        while keyboard.is_pressed(self.push_to_talk_key):
            time.sleep(0.05)
        
        # 🛑 Para gravação
        self.recording = False
        recording_thread.join(timeout=2)
        
        if not self.audio_data:
            print("⚠️ Não foi possível capturar áudio")
            return None
        
        print("🎯 Processando com Whisper...")
        
        # 💾 Salva temporariamente
        try:
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                sf.write(tmp_file.name, np.array(self.audio_data), self.sample_rate)
                
                # 🧠 Transcreve com Whisper
                result = self.whisper_model.transcribe(
                    tmp_file.name,
                    language='pt',  # Força português
                    fp16=False,     # Compatibilidade CPU
                    verbose=False   # Sem logs desnecessários
                )
                
                # 🧹 Limpa arquivo temporário
                os.unlink(tmp_file.name)
                
                texto = result['text'].strip()
                if texto:
                    print(f"✅ Reconhecado: '{texto}'")
                    self.log.log(f"🎤 Comando por voz: {texto}")
                    return texto
                else:
                    print("⚠️ Nenhum texto reconhecido")
                    return None
                    
        except Exception as e:
            self.log.error(f"❌ Erro na transcrição: {str(e)}")
            print("❌ Erro ao processar áudio")
            return None
    
    def _record_audio(self) -> None:
        """🎙️ Thread de gravação de áudio em tempo real"""
        
        self.recording = True
        self.audio_data = []
        
        def audio_callback(indata, frames, time, status):
            if status:
                self.log.warning(f"⚠️ Status de áudio: {status}")
            if self.recording:
                self.audio_data.extend(indata[:, 0])  # Canal mono
        
        try:
            with sd.InputStream(
                callback=audio_callback,
                channels=1,
                samplerate=self.sample_rate,
                dtype=np.float32,
                blocksize=1024
            ):
                while self.recording:
                    time.sleep(0.1)
        except Exception as e:
            self.log.error(f"❌ Erro na gravação: {str(e)}")
            self.recording = False
    
    def _has_text_input(self) -> bool:
        """📝 Verifica se há input de texto aguardando (Windows)"""
        try:
            import msvcrt
            return msvcrt.kbhit()
        except ImportError:
            # Unix/Linux - implementação básica
            import select
            import sys
            return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
        except:
            return False
    
    def test_audio_system(self) -> bool:
        """
        🧪 TESTE COMPLETO DO SISTEMA DE ÁUDIO
        
        Executa diagnóstico completo e reporta status.
        Útil para troubleshooting.
        """
        
        print("🧪 Testando sistema de áudio...")
        
        # Teste 1: Bibliotecas
        tests = {
            "sounddevice": AUDIO_AVAILABLE,
            "whisper": WHISPER_AVAILABLE, 
            "keyboard": KEYBOARD_AVAILABLE,
            "configuração": self.audio_enabled
        }
        
        for component, status in tests.items():
            status_icon = "✅" if status else "❌"
            print(f"  {status_icon} {component}")
        
        if not all(tests.values()):
            print("❌ Sistema de áudio não está completamente funcional")
            return False
        
        # Teste 2: Dispositivos
        try:
            devices = sd.query_devices()
            input_devices = [d for d in devices if d['max_input_channels'] > 0]
            print(f"  ✅ Microfones detectados: {len(input_devices)}")
        except Exception as e:
            print(f"  ❌ Erro nos dispositivos: {str(e)}")
            return False
        
        # Teste 3: Whisper
        if self.whisper_model:
            print(f"  ✅ Modelo Whisper '{self.whisper_model_size}' carregado")
        else:
            print("  ❌ Modelo Whisper não carregado")
            return False
        
        print("🎉 Sistema de áudio totalmente funcional!")
        print(f"🎤 Use '{self.push_to_talk_key.upper()}' para ativar gravação")
        return True

# 🎯 EXEMPLO DE USO E TESTE
if __name__ == "__main__":
    print("🎤 SolAgent Audio Input v1.2 - Testando...")
    
    # Mock config e logger
    config_teste = {
        "audio_input_enabled": True,
        "push_to_talk_key": "space",
        "whisper_model": "tiny"
    }
    
    class LogTeste:
        def log(self, msg): print(f"[LOG] {msg}")
        def debug(self, msg): print(f"[DEBUG] {msg}")
        def error(self, msg): print(f"[ERROR] {msg}")
        def warning(self, msg): print(f"[WARNING] {msg}")
    
    log_teste = LogTeste()
    
    # Teste básico
    audio = AudioInput(config_teste, log_teste)
    
    # Diagnóstico
    if audio.test_audio_system():
        print("\n🎯 Teste de gravação (pressione SPACE e fale):")
        resultado = audio.listen_for_command(timeout=10)
        
        if resultado:
            print(f"🎊 Sucesso! Transcrito: '{resultado}'")
        else:
            print("⚠️ Nenhum comando captado")
    else:
        print("❌ Sistema não está pronto para uso")
    
    print("\n✅ Teste concluído!")