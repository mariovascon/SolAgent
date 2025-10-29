# SolAgent 💻🎙🤖  
Assistente Pessoal Autônoma para Windows  
Versão atual: **v1.2 (local, segura, com voz)**  
Autores: Mario + Sol (assistente IA) + suporte copiloto

---

## 🚀 O que é a SolAgent?
A SolAgent é uma assistente pessoal que roda localmente no seu PC Windows e:
- entende comandos em linguagem natural (texto ou voz),
- gera um plano de ação passo a passo,
- pede sua confirmação,
- e executa ações reais no computador.

Tudo isso com segurança, transparência e auditoria completa.

Ela funciona como um "braço digital" que te ajuda a operar seu computador.

---

## ✨ Principais recursos da versão v1.2
- 🎤 **Entrada por voz (push-to-talk)**  
  Você fala: "Sol, abre o YouTube e procura lo-fi".
- 🔊 **Resposta por voz**  
  A Sol responde com fala usando TTS local (pyttsx3).
- 🧠 **IA conectada**  
  Integração com OpenAI. Se disponível, ela interpreta intenção e gera plano detalhado.
- 🛡️ **Fallback offline**  
  Sem IA? Sem problema. A Sol ainda funciona em modo demonstração.
- 🖥 **Executor seguro com 13+ comandos internos**  
  Abrir navegador, abrir URL, pesquisar no YouTube, criar pasta, listar arquivos, obter hora/data, etc.
- 🔒 **Modo Seguro (safe_mode)**  
  Por padrão, ela NÃO executa nada destrutivo. Ela simula e mostra o que faria.
- ✅ **Confirmação explícita**  
  Antes de rodar qualquer ação real, ela pergunta: "Posso executar estes passos?"
- 📜 **Histórico auditável**  
  Cada interação é registrada com: comando do usuário, plano de ação, passos, e se executou ou não.

> A SolAgent é desenhada pra ser ética, rastreável e segura.

---

## 🧩 Arquitetura (visão simples)
```text
main.py                -> Loop principal (texto/voz -> plano -> confirmação -> execução)
core/brain.py          -> "Cérebro": interpreta intenção e gera passos
core/executor.py       -> "Braço": executa (ou simula) ações no Windows
core/logger.py         -> Logger com timestamps e níveis (INFO/DEBUG/WARNING/ERROR)
core/audio_input.py    -> Captura áudio do microfone (push-to-talk)
core/audio_output.py   -> Fala com você por voz
command_history.py     -> Guarda histórico de tudo que foi pedido e feito
config.json            -> Configurações (safe_mode, chave da IA etc.)
requirements.txt       -> Dependências
```

---

## � Segurança e Privacidade
A SolAgent:
- Não executa nada sem pedir autorização.
- Registra todas as ações em log.
- Informa sempre se está em modo simulação ou execução real.
- Não tenta rastrear localização, IP ou dados sensíveis do usuário.
- Não coleta nem envia seus arquivos pessoais para servidores externos (a não ser que você ative recursos de nuvem futuramente).

Isso torna a SolAgent adequada para criadores, autônomos e pequenas empresas.

---

## � Requisitos
- Windows 10 ou 11
- Python 3.11+
- Microfone (para modo voz)
- Conexão com a internet (apenas se você quiser ativar a IA)
---

## 🔧 Instalação
1. Clone ou baixe este repositório.
2. Abra um terminal dentro da pasta `SolAgent`.
3. Instale dependências:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```
4. Copie `config.example.json` para `config.json` (ou edite `config.json` existente).
5. Abra `config.json` e coloque:
   - `"openai_api_key"` com sua chave da OpenAI
   - `"safe_mode": true` (recomendado no início)

---

## ▶ Como usar
1. Rode:
   ```bash
   python main.py
   ```
2. Escolha se quer digitar ou usar voz (push-to-talk).
3. Exemplo de comandos:
   - "que horas são?"
   - "que dia é hoje?"
   - "abre o YouTube e procura lo-fi"
   - "cria uma pasta em C:\\Projetos\\ClienteX"
   - "me mostra o status do sistema"
4. A Sol vai:
   - explicar o que ela entendeu,
   - listar o plano passo a passo,
   - pedir confirmação,
   - executar (ou simular, se estiver em modo seguro).

5. Você pode dizer:
   - `historico` → ver as últimas interações
   - `sair` → encerrar

---

## 🧠 Sobre o Brain
O módulo `core/brain.py` faz:
- transforma linguagem humana em plano de ação técnico
- retorna JSON do tipo:
  ```json
  {
    "explicacao": "Vou abrir o YouTube e pesquisar lo-fi.",
    "passos": [
      "abrir_navegador",
      "abrir_url:https://www.youtube.com",
      "pesquisar_no_youtube:lo-fi"
    ]
  }
  ```

Esses passos são passados para o `executor.py`, que conhece esses comandos e sabe como simular ou executar com segurança.

---

## 🦾 Sobre o Executor
O módulo `core/executor.py` já suporta, entre outros:

- `abrir_navegador`
- `abrir_url:https://...`
- `pesquisar_no_youtube:TERMO`
- `pesquisar_google:TERMO`
- `abrir_explorador_arquivos`
- `criar_pasta:C:\\caminho\\novo`
- `abrir_programa:notepad`
- `listar_arquivos:C:\\alguma\\pasta`
- `obter_data_atual`
- `obter_hora_atual`
- `mostrar_status_sistema`
- `executar_comando:whoami` (limitado a whitelist segura)
- `falar_para_usuario:mensagem`

Cada passo é logado com timestamp, e no modo seguro ele só simula e avisa.

---

## 🗂 Histórico e Auditoria
O módulo `command_history.py` registra:
- o que você pediu
- como a Sol interpretou
- quais passos ela planejou
- se você autorizou a execução ou não
- quando isso aconteceu

Isso é importante pra confiança e também pra empresas que precisam de trilha de auditoria.

---

## 📢 Roadmap
### v1.3 (Local)
- Ativação/desativação de safe_mode direto por comando de voz ("Sol, modo execução real")
- Perfis de automação por nicho (criador de conteúdo, escritório, consultório, jurídico)

### v2_cloud (SaaS)
- Dashboard web
- Integração com automações externas (Drive, YouTube, social media)
- Gestão de chave IA sem expor chave do cliente
- Assinatura mensal

---

## ⚠ Aviso Legal
Este assistente pode executar ações no seu computador.
Use o modo seguro (`safe_mode: true`) até confiar totalmente nas rotinas.
Você é sempre o aprovador final.

---

## 📄 Licença
Proprietary - Todos os direitos reservados.
Projeto comercial em desenvolvimento.

---

## Contato / Branding
A SolAgent foi criada para ser o primeiro "funcionário digital confiável" que qualquer pessoa pode ter em casa ou na empresa.

Você está usando a v1.2 — a primeira versão pública falante.