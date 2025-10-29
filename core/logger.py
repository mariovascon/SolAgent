"""
⚡ SolAgent v1.1 - Logger Profissional  
=====================================

Sistema de logging com 4 níveis (INFO/DEBUG/WARNING/ERROR).
Timestamps padronizados, console + arquivo, auditoria completa.

Autores: Mario, GitHub Copilot & Sol (ela mesma ajudou a se criar!)
Versão: 1.1 (Comercial) - Tríade Criativa
Data: 28/10/2025
"""

import os
from datetime import datetime

class Logger:
    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        self.log_dir = "logs"
        self.ensure_log_dir()
        
    def ensure_log_dir(self):
        """🗂️ Garante que o diretório de logs existe"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def _stamp(self, level: str, msg: str) -> str:
        """⏰ Gera timestamp padronizado profissional"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{now}] [{level}] {msg}"
    
    def _write_to_file(self, log_entry: str):
        """💾 Escreve no arquivo de log diário"""
        if self.debug_mode:
            log_file = os.path.join(self.log_dir, f"solagent_{datetime.now().strftime('%Y%m%d')}.log")
            try:
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(log_entry + "\n")
            except Exception as e:
                print(f"[LOGGER ERROR] Não conseguiu escrever no arquivo: {e}")
    
    def log(self, message: str):
        """📝 Log INFO - operações normais"""
        stamped = self._stamp("INFO", message)
        print(stamped)
        self._write_to_file(stamped)
    
    def debug(self, message: str):
        """🔍 Log DEBUG - detalhes técnicos (só se debug_mode=True)"""
        if self.debug_mode:
            stamped = self._stamp("DEBUG", message)
            print(stamped)
            self._write_to_file(stamped)
    
    def warning(self, message: str):
        """⚠️ Log WARNING - situações que merecem atenção"""
        stamped = self._stamp("WARNING", message)
        print(stamped)
        self._write_to_file(stamped)
    
    def error(self, message: str):
        """❌ Log ERROR - erros que impedem operação"""
        stamped = self._stamp("ERROR", message)
        print(stamped)
        self._write_to_file(stamped)