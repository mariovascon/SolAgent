#!/usr/bin/env python3
"""
🔍 SolAgent v1.2 - Verificação de Setup
=====================================

Script para verificar se tudo está funcionando corretamente
antes de subir para o GitHub.
"""

import os
import sys
import json
import importlib.util

def check_file_exists(filepath, name):
    """Verifica se um arquivo existe"""
    if os.path.exists(filepath):
        print(f"✅ {name}: OK")
        return True
    else:
        print(f"❌ {name}: FALTANDO")
        return False

def check_python_module(module_name):
    """Verifica se um módulo Python pode ser importado"""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            print(f"✅ Módulo {module_name}: OK")
            return True
        else:
            print(f"❌ Módulo {module_name}: NÃO ENCONTRADO")
            return False
    except Exception as e:
        print(f"❌ Módulo {module_name}: ERRO - {e}")
        return False

def main():
    print("🌟 SolAgent v1.2 - Verificação de Setup")
    print("=" * 50)
    
    # Verificar arquivos essenciais
    files_to_check = [
        ("main.py", "Arquivo principal"),
        ("config.example.json", "Configuração exemplo"),
        ("requirements.txt", "Dependências"),
        ("README.md", "Documentação"),
        (".gitignore", "Git ignore"),
        ("core/brain.py", "Cérebro principal"),
        ("core/executor.py", "Executor"),
        ("core/logger.py", "Sistema de logs"),
        ("core/audio_input.py", "Entrada de áudio"),
        ("core/audio_output.py", "Saída de áudio"),
        ("actions/browser_actions.py", "Ações do navegador"),
        ("actions/system_actions.py", "Ações do sistema"),
    ]
    
    print("\n📁 VERIFICANDO ARQUIVOS:")
    all_files_ok = True
    for filepath, name in files_to_check:
        if not check_file_exists(filepath, name):
            all_files_ok = False
    
    # Verificar módulos Python essenciais
    print("\n🐍 VERIFICANDO MÓDULOS PYTHON:")
    modules_to_check = [
        "openai",
        "speech_recognition", 
        "pyttsx3",
        "pyaudio",
        "whisper",
        "keyboard",
        "requests"
    ]
    
    all_modules_ok = True
    for module in modules_to_check:
        if not check_python_module(module):
            all_modules_ok = False
    
    # Verificar config.json
    print("\n⚙️ VERIFICANDO CONFIGURAÇÃO:")
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            
            if "openai_api_key" in config:
                if config["openai_api_key"] and config["openai_api_key"] != "sua-chave-aqui":
                    print("✅ Chave OpenAI: CONFIGURADA")
                else:
                    print("⚠️ Chave OpenAI: NÃO CONFIGURADA (opcional)")
            
            print(f"✅ Configuração: {len(config)} parâmetros")
            
        except Exception as e:
            print(f"❌ Erro ao ler config.json: {e}")
    else:
        print("⚠️ config.json não encontrado (pode usar config.example.json)")
    
    # Resumo final
    print("\n" + "=" * 50)
    if all_files_ok and all_modules_ok:
        print("🎉 SETUP COMPLETO! SolAgent está pronto para o GitHub!")
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Criar repositório no GitHub")
        print("2. git remote add origin <URL-DO-REPO>")
        print("3. git push -u origin main")
        print("4. Criar demo de 3 minutos")
        print("5. 🚀 LANÇAR!")
    else:
        print("⚠️ Alguns itens precisam de atenção antes do upload")
        if not all_modules_ok:
            print("💡 Execute: pip install -r requirements.txt")
    
    print(f"\n🌐 Versão: SolAgent v1.2")
    print(f"📍 Diretório: {os.getcwd()}")

if __name__ == "__main__":
    main()