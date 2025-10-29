"""
⚡ SolAgent v1.2 - Histórico de Comandos
=======================================

Sistema de persistência de interações usuário-Sol.
Base para analytics, aprendizado e melhorias.

Funcionalidades:
- Salva todas as interações em JSON
- Timestamps precisos
- Análise de padrões de uso
- Relatórios de eficiência
- Backup automático
- Privacy-first (dados locais)

Autores: Mario, GitHub Copilot & Sol (ela mesma ajudou a se criar!)
Versão: 1.2 (Audio Revolution) - Tríade Criativa
Data: 28/10/2025
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import hashlib

class CommandHistory:
    """
    📊 SISTEMA DE HISTÓRICO INTELIGENTE
    
    Características:
    - Todas as interações salvas localmente
    - Analytics de uso automático
    - Detecção de padrões
    - Relatórios de performance
    - Backup e limpeza automática
    """
    
    def __init__(self, config: dict, log):
        self.config = config
        self.log = log
        
        # 📁 CONFIGURAÇÕES
        self.history_enabled = config.get("history_enabled", True)
        self.history_dir = config.get("history_dir", "history")
        self.max_history_days = config.get("max_history_days", 30)
        self.privacy_mode = config.get("privacy_mode", False)  # Hashifica dados sensíveis
        
        # 📊 ARQUIVOS
        today = datetime.now().strftime("%Y%m%d")
        self.current_file = os.path.join(self.history_dir, f"commands_{today}.json")
        self.analytics_file = os.path.join(self.history_dir, "analytics.json")
        
        self._initialize()
    
    def _initialize(self) -> None:
        """🚀 Inicializa sistema de histórico"""
        
        if not self.history_enabled:
            self.log.log("📊 Histórico desabilitado por configuração")
            return
        
        # Cria diretório se não existir
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)
            self.log.log(f"📁 Diretório criado: {self.history_dir}")
        
        # Limpeza automática de arquivos antigos
        self._cleanup_old_files()
        
        self.log.log("📊 Sistema de histórico inicializado")
    
    def save_interaction(self, 
                        user_input: str, 
                        plan: Dict[str, Any], 
                        execution_result: str = "unknown",
                        input_method: str = "text",
                        response_method: str = "text") -> None:
        """
        💾 SALVA UMA INTERAÇÃO COMPLETA
        
        Args:
            user_input: Comando original do usuário
            plan: Plano gerado pelo brain
            execution_result: success, cancelled, error
            input_method: text, voice
            response_method: text, voice, both
        """
        
        if not self.history_enabled:
            return
        
        try:
            # 🎯 Monta registro da interação
            interaction = {
                "timestamp": datetime.now().isoformat(),
                "user_input": self._sanitize_text(user_input),
                "input_method": input_method,
                "brain_explanation": self._sanitize_text(plan.get("explicacao", "")),
                "steps_count": len(plan.get("passos", [])),
                "steps": plan.get("passos", []),
                "execution_result": execution_result,
                "response_method": response_method,
                "safe_mode": self.config.get("safe_mode", True),
                "ai_mode": "openai" if self.config.get("openai_api_key", "").strip() not in ["", "COLE_SUA_CHAVE_AQUI"] else "mock"
            }
            
            # 🔒 Privacy mode - hashifica dados sensíveis
            if self.privacy_mode:
                interaction["user_input_hash"] = self._hash_text(user_input)
                interaction["user_input"] = "[PRIVATE]"
            
            # 💾 Salva no arquivo diário
            self._append_to_file(self.current_file, interaction)
            
            # 📈 Atualiza analytics
            self._update_analytics(interaction)
            
            self.log.debug(f"📊 Interação salva: {execution_result}")
            
        except Exception as e:
            self.log.error(f"❌ Erro ao salvar histórico: {str(e)}")
    
    def get_today_stats(self) -> Dict[str, Any]:
        """📈 Estatísticas do dia atual"""
        
        if not self.history_enabled or not os.path.exists(self.current_file):
            return {"total_commands": 0, "voice_commands": 0, "successful_executions": 0}
        
        try:
            with open(self.current_file, 'r', encoding='utf-8') as f:
                interactions = [json.loads(line) for line in f if line.strip()]
            
            total_commands = len(interactions)
            voice_commands = sum(1 for i in interactions if i.get("input_method") == "voice")
            successful_executions = sum(1 for i in interactions if i.get("execution_result") == "success")
            
            return {
                "total_commands": total_commands,
                "voice_commands": voice_commands,
                "text_commands": total_commands - voice_commands,
                "successful_executions": successful_executions,
                "success_rate": (successful_executions / total_commands * 100) if total_commands > 0 else 0
            }
            
        except Exception as e:
            self.log.error(f"❌ Erro ao calcular estatísticas: {str(e)}")
            return {"error": str(e)}
    
    def get_recent_commands(self, limit: int = 10) -> List[Dict[str, Any]]:
        """📋 Comandos recentes do usuário"""
        
        if not self.history_enabled or not os.path.exists(self.current_file):
            return []
        
        try:
            with open(self.current_file, 'r', encoding='utf-8') as f:
                interactions = [json.loads(line) for line in f if line.strip()]
            
            # Retorna os mais recentes
            recent = interactions[-limit:] if len(interactions) > limit else interactions
            
            # Simplifica para exibição
            simplified = []
            for interaction in reversed(recent):  # Mais recente primeiro
                simplified.append({
                    "time": datetime.fromisoformat(interaction["timestamp"]).strftime("%H:%M"),
                    "input": interaction["user_input"][:50] + "..." if len(interaction["user_input"]) > 50 else interaction["user_input"],
                    "method": interaction["input_method"], 
                    "result": interaction["execution_result"]
                })
            
            return simplified
            
        except Exception as e:
            self.log.error(f"❌ Erro ao buscar comandos recentes: {str(e)}")
            return []
    
    def get_usage_patterns(self) -> Dict[str, Any]:
        """🎯 Análise de padrões de uso"""
        
        try:
            # Carrega analytics existente
            analytics = self._load_analytics()
            
            # Calcula padrões
            patterns = {
                "most_used_commands": analytics.get("command_frequency", {})[:5],
                "preferred_input_method": analytics.get("input_method_stats", {}),
                "peak_hours": analytics.get("hourly_usage", {}),
                "success_rate_trend": analytics.get("daily_success_rates", [])[-7:],  # Última semana
                "total_interactions": analytics.get("total_interactions", 0)
            }
            
            return patterns
            
        except Exception as e:
            self.log.error(f"❌ Erro ao analisar padrões: {str(e)}")
            return {}
    
    def generate_report(self) -> str:
        """📊 Gera relatório completo de uso"""
        
        try:
            today_stats = self.get_today_stats()
            patterns = self.get_usage_patterns()
            recent_commands = self.get_recent_commands(5)
            
            report = f"""
📊 ═══ RELATÓRIO SOLAGENT v1.2 ═══
📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}

🎯 ESTATÍSTICAS DE HOJE:
  • Total de comandos: {today_stats.get('total_commands', 0)}
  • Comandos por voz: {today_stats.get('voice_commands', 0)}
  • Comandos por texto: {today_stats.get('text_commands', 0)}
  • Execuções bem-sucedidas: {today_stats.get('successful_executions', 0)}
  • Taxa de sucesso: {today_stats.get('success_rate', 0):.1f}%

📈 PADRÕES GERAIS:
  • Total de interações históricas: {patterns.get('total_interactions', 0)}
  • Método preferido: {self._get_preferred_method(patterns)}

📋 COMANDOS RECENTES:
"""
            
            for cmd in recent_commands:
                status_icon = "✅" if cmd["result"] == "success" else "❌" if cmd["result"] == "error" else "⏸️"
                method_icon = "🎤" if cmd["method"] == "voice" else "✍️"
                report += f"  {status_icon} {method_icon} {cmd['time']} - {cmd['input']}\n"
            
            if not recent_commands:
                report += "  (Nenhum comando registrado hoje)\n"
            
            report += f"""
💡 DICAS:
  • Use comandos por voz para maior produtividade
  • Configure sua chave OpenAI para IA mais inteligente
  • Ative modo execução real quando confiante
  
🔗 Histórico salvo em: {self.current_file}
"""
            
            return report
            
        except Exception as e:
            return f"❌ Erro ao gerar relatório: {str(e)}"
    
    def _append_to_file(self, filepath: str, data: Dict[str, Any]) -> None:
        """💾 Adiciona linha ao arquivo JSON Lines"""
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
    
    def _update_analytics(self, interaction: Dict[str, Any]) -> None:
        """📈 Atualiza arquivo de analytics"""
        
        try:
            analytics = self._load_analytics()
            
            # Contadores gerais
            analytics["total_interactions"] = analytics.get("total_interactions", 0) + 1
            analytics["last_updated"] = datetime.now().isoformat()
            
            # Frequência de comandos (baseado na explicação)
            explanation = interaction.get("brain_explanation", "").lower()
            command_freq = analytics.setdefault("command_frequency", {})
            command_freq[explanation] = command_freq.get(explanation, 0) + 1
            
            # Estatísticas de método de entrada
            input_method = interaction.get("input_method", "text")
            input_stats = analytics.setdefault("input_method_stats", {})
            input_stats[input_method] = input_stats.get(input_method, 0) + 1
            
            # Uso por hora
            hour = datetime.fromisoformat(interaction["timestamp"]).hour
            hourly = analytics.setdefault("hourly_usage", {})
            hourly[str(hour)] = hourly.get(str(hour), 0) + 1
            
            # Taxa de sucesso diária
            today = datetime.now().strftime("%Y-%m-%d")
            daily_rates = analytics.setdefault("daily_success_rates", {})
            if today not in daily_rates:
                daily_rates[today] = {"total": 0, "success": 0}
            
            daily_rates[today]["total"] += 1
            if interaction.get("execution_result") == "success":
                daily_rates[today]["success"] += 1
            
            # Salva analytics atualizados
            with open(self.analytics_file, 'w', encoding='utf-8') as f:
                json.dump(analytics, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            self.log.error(f"❌ Erro ao atualizar analytics: {str(e)}")
    
    def _load_analytics(self) -> Dict[str, Any]:
        """📊 Carrega arquivo de analytics"""
        
        if os.path.exists(self.analytics_file):
            try:
                with open(self.analytics_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _cleanup_old_files(self) -> None:
        """🧹 Remove arquivos de histórico antigos"""
        
        try:
            cutoff_date = datetime.now() - timedelta(days=self.max_history_days)
            
            for filename in os.listdir(self.history_dir):
                if filename.startswith("commands_") and filename.endswith(".json"):
                    file_path = os.path.join(self.history_dir, filename)
                    file_date_str = filename.replace("commands_", "").replace(".json", "")
                    
                    try:
                        file_date = datetime.strptime(file_date_str, "%Y%m%d")
                        if file_date < cutoff_date:
                            os.remove(file_path)
                            self.log.debug(f"🧹 Arquivo antigo removido: {filename}")
                    except ValueError:
                        continue  # Ignora arquivos com formato inválido
                        
        except Exception as e:
            self.log.error(f"❌ Erro na limpeza: {str(e)}")
    
    def _sanitize_text(self, text: str) -> str:
        """🧹 Remove caracteres problemáticos do texto"""
        if not text:
            return ""
        
        # Remove quebras de linha e espaços extras
        sanitized = ' '.join(text.strip().split())
        
        # Trunca se muito longo
        if len(sanitized) > 500:
            sanitized = sanitized[:497] + "..."
        
        return sanitized
    
    def _hash_text(self, text: str) -> str:
        """🔒 Cria hash de texto para privacy mode"""
        return hashlib.sha256(text.encode()).hexdigest()[:16]
    
    def _get_preferred_method(self, patterns: Dict[str, Any]) -> str:
        """🎯 Determina método de entrada preferido"""
        input_stats = patterns.get("input_method_stats", {})
        
        if not input_stats:
            return "Não definido"
        
        preferred = max(input_stats.items(), key=lambda x: x[1])
        return f"{'🎤 Voz' if preferred[0] == 'voice' else '✍️ Texto'} ({preferred[1]} usos)"

# 🎯 EXEMPLO DE USO E TESTE
if __name__ == "__main__":
    print("📊 SolAgent Command History v1.2 - Testando...")
    
    # Mock config e logger
    config_teste = {
        "history_enabled": True,
        "history_dir": "test_history",
        "max_history_days": 7,
        "privacy_mode": False
    }
    
    class LogTeste:
        def log(self, msg): print(f"[LOG] {msg}")
        def debug(self, msg): print(f"[DEBUG] {msg}")
        def error(self, msg): print(f"[ERROR] {msg}")
    
    log_teste = LogTeste()
    
    # Teste básico
    history = CommandHistory(config_teste, log_teste)
    
    # Simula algumas interações
    test_interactions = [
        ("que horas são", {"explicacao": "Vou mostrar a hora", "passos": ["obter_hora_atual"]}, "success", "text"),
        ("abrir youtube", {"explicacao": "Vou abrir o YouTube", "passos": ["abrir_url:youtube.com"]}, "success", "voice"),
        ("comando inválido", {"explicacao": "Não entendi", "passos": []}, "cancelled", "text")
    ]
    
    for user_input, plan, result, method in test_interactions:
        history.save_interaction(user_input, plan, result, method, "text")
    
    # Mostra relatório
    print("\n" + history.generate_report())
    
    print("\n✅ Teste concluído!")