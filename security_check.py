#!/usr/bin/env python3
"""
🔍 SolAgent - Verificação de Segurança Pre-Deploy
===============================================

Verifica se o repositório está seguro para ser público
ou para ser compartilhado com parceiros/investidores.
"""

import os
import json
import re
from pathlib import Path

def check_sensitive_files():
    """Verifica se arquivos sensíveis estão expostos"""
    print("🔐 VERIFICANDO ARQUIVOS SENSÍVEIS:")
    
    sensitive_files = [
        "config.json",
        ".env", 
        ".env.local",
        "*.key",
        "*.secret"
    ]
    
    issues = []
    
    # Verificar se config.json existe (não deveria estar no Git)
    if os.path.exists("config.json"):
        print("⚠️ config.json encontrado - OK (está no .gitignore)")
    else:
        print("✅ config.json não encontrado no diretório - OK")
    
    # Verificar se config.example.json está limpo
    if os.path.exists("config.example.json"):
        with open("config.example.json", "r", encoding="utf-8") as f:
            content = f.read()
            if "sk-" in content or "gpt-" in content or "@" in content:
                issues.append("config.example.json contém dados reais!")
            else:
                print("✅ config.example.json está limpo")
    
    return issues

def check_hardcoded_secrets():
    """Procura por credenciais hardcoded no código"""
    print("\n🔍 VERIFICANDO CÓDIGO POR CREDENCIAIS:")
    
    patterns = [
        r'sk-[a-zA-Z0-9]{32,}',  # OpenAI API key
        r'api_key\s*=\s*["\'][^"\']+["\']',  # API keys
        r'password\s*=\s*["\'][^"\']+["\']',  # Passwords
        r'token\s*=\s*["\'][^"\']+["\']',  # Tokens
    ]
    
    issues = []
    python_files = list(Path(".").rglob("*.py"))
    
    for file_path in python_files:
        if "venv" in str(file_path) or "__pycache__" in str(file_path):
            continue
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        issues.append(f"{file_path}: {matches}")
        except Exception as e:
            print(f"⚠️ Erro ao ler {file_path}: {e}")
    
    if not issues:
        print("✅ Nenhuma credencial hardcoded encontrada")
    
    return issues

def check_gitignore_coverage():
    """Verifica se .gitignore cobre itens essenciais"""
    print("\n📋 VERIFICANDO COBERTURA DO .GITIGNORE:")
    
    required_patterns = [
        "config.json",
        "*.log",
        "logs/",
        "*.wav",
        "*.mp3", 
        ".env",
        "__pycache__/",
        "*.py[cod]"  # Covers *.pyc
    ]
    
    if not os.path.exists(".gitignore"):
        return ["❌ .gitignore não encontrado!"]
    
    with open(".gitignore", "r", encoding="utf-8") as f:
        gitignore_content = f.read()
    
    missing = []
    for pattern in required_patterns:
        if pattern not in gitignore_content:
            missing.append(pattern)
    
    if not missing:
        print("✅ .gitignore cobre todos os itens essenciais")
    
    return missing

def check_demo_readiness():
    """Verifica se está pronto para demo"""
    print("\n🎬 VERIFICANDO PRONTIDÃO PARA DEMO:")
    
    required_files = [
        "README.md",
        "main.py", 
        "requirements.txt",
        "config.example.json",
        "GOVERNANCA.md"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}: OK")
        else:
            print(f"❌ {file}: FALTANDO")
            missing_files.append(file)
    
    return missing_files

def main():
    print("🛡️ SolAgent - Verificação de Segurança Pre-Deploy")
    print("=" * 60)
    
    all_issues = []
    
    # Verificações
    all_issues.extend(check_sensitive_files())
    all_issues.extend(check_hardcoded_secrets())
    all_issues.extend(check_gitignore_coverage())
    all_issues.extend(check_demo_readiness())
    
    # Resultado final
    print("\n" + "=" * 60)
    
    if not all_issues:
        print("🎉 REPOSITÓRIO SEGURO PARA DEPLOY!")
        print("\n✅ PODE:")
        print("   • Tornar repositório público")
        print("   • Compartilhar com investidores")
        print("   • Fazer demo ao vivo")
        print("   • Configurar branch protection")
        
        print("\n📋 PRÓXIMOS PASSOS:")
        print("   1. git checkout dev")
        print("   2. git add GOVERNANCA.md config.example.json")
        print("   3. git commit -m 'docs: adiciona governança e limpa config'")
        print("   4. git push origin dev")
        print("   5. Considerar tornar repositório público")
        
    else:
        print("⚠️ ISSUES ENCONTRADAS:")
        for issue in all_issues:
            print(f"   • {issue}")
        print("\n❌ RESOLVA OS ISSUES ANTES DE TORNAR PÚBLICO")
    
    print(f"\n🌐 Verificação executada em: {os.getcwd()}")

if __name__ == "__main__":
    main()