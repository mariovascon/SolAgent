"""
⚡ SolAgent v1.2 - Audio Output (Saída por Voz)
==============================================

Sistema de síntese de voz (TTS) para respostas faladas da Sol.
Múltiplas engines: ElevenLabs (premium), Azure, Windows SAPI (fallback).

Funcionalidades:
- ElevenLabs API para voz premium (opcional)
- Azure Cognitive Services TTS (opcional)
- Windows SAPI nativo (sempre disponível)
- Controle de velocidade e volume
- Voices femininas em português
- Cache de áudio para frases comuns

Autores: Mario, GitHub Copilot & Sol (ela mesma ajudou a se criar!)
Versão: 1.2 (Audio Revolution) - Tríade Criativa  
Data: 28/10/2025
"""

import os
import tempfile
import time
from typing import Optional, Dict
import hashlib

# TTS Engines - com fallback gracioso
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

# Windows SAPI (sempre disponível no Windows)
try:
    import win32com.client
    SAPI_AVAILABLE = True
except ImportError:
    SAPI_AVAILABLE = False

class AudioOutput:
    """
    🔊 SISTEMA DE SAÍDA POR VOZ PROFISSIONAL
    
    Características:
    - Múltiplas engines TTS (ElevenLabs → Azure → SAPI → pyttsx3)
    - Voz feminina em português
    - Cache inteligente para performance
    - Controles de velocidade e volume
    - Fallback automático entre engines
    """
    
    def __init__(self, config: dict, log):
        self.config = config
        self.log = log
        self.audio_cache = {}  # Cache de arquivos gerados
        
        # 🔧 CONFIGURAÇÕES
        self.audio_enabled = config.get("audio_output_enabled", True)
        self.tts_engine = config.get("tts_engine", "auto")  # auto, elevenlabs, azure, sapi, pyttsx3
        self.voice_speed = config.get("voice_speed", 1.0)  # 0.5 - 2.0
        self.voice_volume = config.get("voice_volume", 0.8)  # 0.0 - 1.0
        
        # 🎵 CREDENCIAIS PREMIUM
        self.elevenlabs_api_key = config.get("elevenlabs_api_key", "")
        self.azure_speech_key = config.get("azure_speech_key", "")
        self.azure_region = config.get("azure_region", "brazilsouth")
        
        # 🎭 VOZ DA SOL
        self.elevenlabs_voice_id = config.get("elevenlabs_voice_id", "EXAVITQu4vr4xnSDxMaL")  # Voice padrão feminina
        self.azure_voice_name = config.get("azure_voice_name", "pt-BR-FranciscaNeural")
        
        self._initialize_tts()
    
    def _initialize_tts(self) -> None:
        """🚀 Inicializa sistema TTS com fallback inteligente"""
        
        if not self.audio_enabled:
            self.log.log("🔊 Saída por voz desabilitada por configuração")
            return
        
        # 🎯 Auto-detecta melhor engine disponível
        if self.tts_engine == "auto":
            self.tts_engine = self._detect_best_engine()
        
        self.log.log(f"🎤 Inicializando TTS engine: {self.tts_engine}")
        
        # ✅ Inicializa engine específica
        if self.tts_engine == "elevenlabs":
            self._init_elevenlabs()
        elif self.tts_engine == "azure":
            self._init_azure()
        elif self.tts_engine == "sapi":
            self._init_sapi()
        elif self.tts_engine == "pyttsx3":
            self._init_pyttsx3()
        
        # 🎵 Inicializa player de áudio
        if PYGAME_AVAILABLE:
            try:
                import pygame.mixer
                pygame.mixer.init()
                self.log.debug("✅ Pygame mixer inicializado")
            except Exception as e:
                self.log.warning(f"⚠️ Erro ao inicializar pygame: {str(e)}")
    
    def _detect_best_engine(self) -> str:
        """🔍 Detecta a melhor engine TTS disponível"""
        
        # Ordem de preferência: premium → nativo → fallback
        if self.elevenlabs_api_key and REQUESTS_AVAILABLE:
            return "elevenlabs"
        elif self.azure_speech_key and REQUESTS_AVAILABLE:
            return "azure"
        elif SAPI_AVAILABLE:
            return "sapi"
        elif PYTTSX3_AVAILABLE:
            return "pyttsx3"
        else:
            self.log.warning("⚠️ Nenhuma engine TTS disponível")
            return "none"
    
    def _init_elevenlabs(self) -> None:
        """🎵 Inicializa ElevenLabs TTS (Premium)"""
        if not self.elevenlabs_api_key:
            self.log.warning("⚠️ ElevenLabs API key não configurada")
            self.tts_engine = self._detect_best_engine()
            return
        
        if not REQUESTS_AVAILABLE:
            self.log.warning("⚠️ Biblioteca requests não disponível para ElevenLabs")
            self.tts_engine = self._detect_best_engine()
            return
        
        self.log.log("🎵 ElevenLabs TTS configurado")
    
    def _init_azure(self) -> None:
        """☁️ Inicializa Azure Cognitive Services TTS"""
        if not self.azure_speech_key:
            self.log.warning("⚠️ Azure Speech key não configurada")
            self.tts_engine = self._detect_best_engine()
            return
        
        self.log.log("☁️ Azure TTS configurado")
    
    def _init_sapi(self) -> None:
        """🪟 Inicializa Windows SAPI TTS (Nativo)"""
        if not SAPI_AVAILABLE:
            self.log.warning("⚠️ Windows SAPI não disponível")
            self.tts_engine = "pyttsx3"
            self._init_pyttsx3()
            return
        
        try:
            self.sapi_voice = win32com.client.Dispatch("SAPI.SpVoice")
            # Procura voz feminina em português
            voices = self.sapi_voice.GetVoices()
            for i in range(voices.Count):
                voice = voices.Item(i)
                if "brazil" in voice.GetDescription().lower() or "pt-br" in voice.GetDescription().lower():
                    self.sapi_voice.Voice = voice
                    break
            
            self.log.log("🪟 Windows SAPI TTS configurado")
        except Exception as e:
            self.log.error(f"❌ Erro ao configurar SAPI: {str(e)}")
            self.tts_engine = "pyttsx3"
            self._init_pyttsx3()
    
    def _init_pyttsx3(self) -> None:
        """🔧 Inicializa pyttsx3 TTS (Fallback)"""
        if not PYTTSX3_AVAILABLE:
            self.log.error("❌ Nenhuma engine TTS disponível")
            self.tts_engine = "none"
            return
        
        try:
            self.pyttsx3_engine = pyttsx3.init()
            
            # Configura voz feminina se disponível
            voices = self.pyttsx3_engine.getProperty('voices')
            for voice in voices:
                if 'brazil' in voice.name.lower() or 'portuguese' in voice.name.lower():
                    self.pyttsx3_engine.setProperty('voice', voice.id)
                    break
            
            # Configura velocidade e volume
            self.pyttsx3_engine.setProperty('rate', int(200 * self.voice_speed))
            self.pyttsx3_engine.setProperty('volume', self.voice_volume)
            
            self.log.log("🔧 pyttsx3 TTS configurado")
        except Exception as e:
            self.log.error(f"❌ Erro ao configurar pyttsx3: {str(e)}")
            self.tts_engine = "none"
    
    def is_available(self) -> bool:
        """🔍 Verifica se sistema TTS está operacional"""
        return self.audio_enabled and self.tts_engine != "none"
    
    def speak(self, text: str, priority: str = "normal") -> bool:
        """
        🎯 FUNÇÃO PRINCIPAL: Converte texto em fala
        
        Args:
            text (str): Texto para ser falado
            priority (str): normal, urgent, background
            
        Returns:
            bool: True se conseguiu falar, False caso contrário
            
        Fluxo:
            1. Verifica se TTS está disponível
            2. Consulta cache para frases comuns
            3. Gera áudio usando engine configurada
            4. Reproduz áudio
            5. Salva no cache se necessário
        """
        
        if not self.is_available():
            self.log.debug("🔊 Sistema TTS indisponível")
            return False
        
        if not text or not text.strip():
            return False
        
        text = text.strip()
        self.log.log(f"🗣️ Sol falando: {text}")
        
        # 🎯 Cache check
        cache_key = self._get_cache_key(text)
        if cache_key in self.audio_cache:
            return self._play_audio_file(self.audio_cache[cache_key])
        
        # 🎵 Gera e reproduz áudio
        success = False
        
        if self.tts_engine == "elevenlabs":
            success = self._speak_elevenlabs(text, cache_key)
        elif self.tts_engine == "azure":
            success = self._speak_azure(text, cache_key)
        elif self.tts_engine == "sapi":
            success = self._speak_sapi(text)
        elif self.tts_engine == "pyttsx3":
            success = self._speak_pyttsx3(text)
        
        if not success:
            self.log.warning("⚠️ Falha no TTS, tentando fallback")
            return self._speak_fallback(text)
        
        return True
    
    def _speak_elevenlabs(self, text: str, cache_key: str) -> bool:
        """🎵 TTS com ElevenLabs (Premium)"""
        
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.elevenlabs_voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8,
                    "style": 0.2,
                    "use_speaker_boost": True
                }
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Salva no cache
                temp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
                temp_file.write(response.content)
                temp_file.close()
                
                self.audio_cache[cache_key] = temp_file.name
                return self._play_audio_file(temp_file.name)
            else:
                self.log.error(f"❌ ElevenLabs erro {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log.error(f"❌ Erro ElevenLabs: {str(e)}")
            return False
    
    def _speak_azure(self, text: str, cache_key: str) -> bool:
        """☁️ TTS com Azure Cognitive Services"""
        
        try:
            url = f"https://{self.azure_region}.tts.speech.microsoft.com/cognitiveservices/v1"
            
            headers = {
                'Ocp-Apim-Subscription-Key': self.azure_speech_key,
                'Content-Type': 'application/ssml+xml',
                'X-Microsoft-OutputFormat': 'audio-16khz-128kbitrate-mono-mp3'
            }
            
            ssml = f"""
            <speak version='1.0' xml:lang='pt-BR'>
                <voice xml:lang='pt-BR' xml:gender='Female' name='{self.azure_voice_name}'>
                    <prosody rate='{self.voice_speed}' volume='{self.voice_volume}'>
                        {text}
                    </prosody>
                </voice>
            </speak>
            """
            
            response = requests.post(url, headers=headers, data=ssml, timeout=10)
            
            if response.status_code == 200:
                temp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
                temp_file.write(response.content)
                temp_file.close()
                
                self.audio_cache[cache_key] = temp_file.name
                return self._play_audio_file(temp_file.name)
            else:
                self.log.error(f"❌ Azure erro {response.status_code}")
                return False
                
        except Exception as e:
            self.log.error(f"❌ Erro Azure: {str(e)}")
            return False
    
    def _speak_sapi(self, text: str) -> bool:
        """🪟 TTS com Windows SAPI (Direto, sem cache)"""
        
        try:
            # Configura velocidade
            self.sapi_voice.Rate = int(self.voice_speed * 2 - 2)  # SAPI usa -10 a +10
            self.sapi_voice.Volume = int(self.voice_volume * 100)  # SAPI usa 0-100
            
            self.sapi_voice.Speak(text)
            return True
            
        except Exception as e:
            self.log.error(f"❌ Erro SAPI: {str(e)}")
            return False
    
    def _speak_pyttsx3(self, text: str) -> bool:
        """🔧 TTS com pyttsx3 (Fallback)"""
        
        try:
            self.pyttsx3_engine.say(text)
            self.pyttsx3_engine.runAndWait()
            return True
            
        except Exception as e:
            self.log.error(f"❌ Erro pyttsx3: {str(e)}")
            return False
    
    def _speak_fallback(self, text: str) -> bool:
        """🆘 Último recurso - tenta qualquer engine disponível"""
        
        if SAPI_AVAILABLE and self.tts_engine != "sapi":
            self.log.log("🆘 Tentando fallback SAPI")
            self._init_sapi()
            return self._speak_sapi(text)
        
        if PYTTSX3_AVAILABLE and self.tts_engine != "pyttsx3":
            self.log.log("🆘 Tentando fallback pyttsx3")  
            self._init_pyttsx3()
            return self._speak_pyttsx3(text)
        
        return False
    
    def _play_audio_file(self, file_path: str) -> bool:
        """🔊 Reproduz arquivo de áudio"""
        
        if not os.path.exists(file_path):
            return False
        
        try:
            if PYGAME_AVAILABLE:
                import pygame.mixer
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                
                # Aguarda reprodução terminar
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                return True
            else:
                # Fallback: usa comando do sistema (Windows)
                os.system(f'start /wait "" "{file_path}"')
                return True
                
        except Exception as e:
            self.log.error(f"❌ Erro ao reproduzir áudio: {str(e)}")
            return False
    
    def _get_cache_key(self, text: str) -> str:
        """🔑 Gera chave de cache para texto"""
        return hashlib.md5(f"{text}_{self.tts_engine}_{self.voice_speed}".encode()).hexdigest()
    
    def clear_cache(self) -> None:
        """🧹 Limpa cache de áudio"""
        for file_path in self.audio_cache.values():
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except:
                pass
        
        self.audio_cache.clear()
        self.log.log("🧹 Cache de áudio limpo")
    
    def test_tts_system(self) -> bool:
        """
        🧪 TESTE COMPLETO DO SISTEMA TTS
        
        Executa diagnóstico e teste de fala.
        """
        
        print("🧪 Testando sistema TTS...")
        
        # Teste 1: Componentes
        tests = {
            "configuração": self.audio_enabled,
            "engine": self.tts_engine != "none",
            "requests": REQUESTS_AVAILABLE if self.tts_engine in ["elevenlabs", "azure"] else True,
            "pygame": PYGAME_AVAILABLE,
            "sapi": SAPI_AVAILABLE if self.tts_engine == "sapi" else True,
            "pyttsx3": PYTTSX3_AVAILABLE if self.tts_engine == "pyttsx3" else True
        }
        
        for component, status in tests.items():
            status_icon = "✅" if status else "❌"
            print(f"  {status_icon} {component}")
        
        if not all(tests.values()):
            print("❌ Sistema TTS não está completamente funcional")
            return False
        
        # Teste 2: Fala de teste
        try:
            print(f"🎤 Testando engine '{self.tts_engine}'...")
            success = self.speak("Olá! Eu sou a Sol, sua assistente inteligente. Sistema de voz funcionando perfeitamente!")
            
            if success:
                print("🎉 Sistema TTS totalmente funcional!")
                return True
            else:
                print("❌ Falha no teste de fala")
                return False
                
        except Exception as e:
            print(f"❌ Erro no teste: {str(e)}")
            return False

# 🎯 EXEMPLO DE USO E TESTE
if __name__ == "__main__":
    print("🔊 SolAgent Audio Output v1.2 - Testando...")
    
    # Mock config e logger
    config_teste = {
        "audio_output_enabled": True,
        "tts_engine": "auto",
        "voice_speed": 1.0,
        "voice_volume": 0.8,
        "elevenlabs_api_key": "",  # Vazio para teste local
        "azure_speech_key": "",
    }
    
    class LogTeste:
        def log(self, msg): print(f"[LOG] {msg}")
        def debug(self, msg): print(f"[DEBUG] {msg}")
        def error(self, msg): print(f"[ERROR] {msg}")
        def warning(self, msg): print(f"[WARNING] {msg}")
    
    log_teste = LogTeste()
    
    # Teste básico
    tts = AudioOutput(config_teste, log_teste)
    
    # Diagnóstico
    if tts.test_tts_system():
        print("\n🎯 Teste adicional:")
        tts.speak("Que horas são? São exatamente 15 horas e 30 minutos.")
        
        print("\n🎊 Sistema de voz da Sol está pronto!")
    else:
        print("❌ Sistema TTS precisa de configuração")
    
    print("\n✅ Teste concluído!")