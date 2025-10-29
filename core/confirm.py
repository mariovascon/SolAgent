def ask_user_confirmation() -> bool:
    """
    Pergunta ao usuário se pode executar os passos do plano.
    Retorna True se o usuário confirmar, False caso contrário.
    """
    print("\n🤔 Sol: Posso executar esses passos?")
    resp = input("   Digite 's' para SIM ou 'n' para NÃO: ").strip().lower()
    
    if resp in ["s", "sim", "y", "yes", "ok", "pode", "vai"]:
        return True
    elif resp in ["n", "nao", "não", "no", "para", "cancela"]:
        return False
    else:
        print("   Resposta não reconhecida. Por segurança, cancelando...")
        return False

def ask_detailed_confirmation(steps: list) -> bool:
    """
    Confirmação detalhada para ações mais sensíveis.
    """
    print("\n🚨 CONFIRMAÇÃO DETALHADA NECESSÁRIA")
    print("   As seguintes ações serão executadas:")
    
    for i, step in enumerate(steps, 1):
        print(f"   {i}. {step}")
    
    print("\n⚠️  Tem certeza que deseja continuar?")
    resp = input("   Digite 'CONFIRMO' para executar ou qualquer outra coisa para cancelar: ").strip()
    
    return resp == "CONFIRMO"