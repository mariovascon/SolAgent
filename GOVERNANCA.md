# 🛡️ SolAgent - Governança e Proteção de Branches

## 🧠 Contexto Técnico — Branch Protection e Estratégia de Governança

### O problema

Durante a configuração de proteção da branch `main`, identificamos uma limitação do GitHub para contas pessoais **com repositórios privados**.
Mesmo que as regras de proteção (branch protection rules) sejam salvas, o GitHub exibe o aviso:

> "Rules on your private repos can't be enforced until you upgrade to GitHub Team or Enterprise."

Isso significa que as proteções configuradas — como impedir `force push`, bloquear `delete`, e exigir `pull request` — **não são aplicadas de fato** enquanto o repositório for privado em uma conta pessoal gratuita.
O GitHub apenas guarda a configuração, mas **não executa as restrições**.

### Por que isso importa

A SolAgent já não é um projeto experimental.
Ela tem estrutura profissional de branches:

* `main` → versão estável e pública (v1.2)
* `dev` → linha de desenvolvimento ativo
* `v2_cloud` → roadmap SaaS futuro

A `main` representa o **produto** — é a versão que vai pra demonstrações, vídeos e clientes.
Por isso, precisa estar protegida contra pushs diretos, merges sem revisão e exclusões acidentais.

### A solução adotada

Após análise, decidimos o seguinte plano estratégico para contornar a limitação sem comprometer segurança:

#### ✅ Etapa 1 — Tornar o repositório público

O repositório foi tornado público.
Com isso, o GitHub passou a aplicar automaticamente todas as **branch protection rules** mesmo no plano gratuito.

A `main` agora está protegida por:

* Require Pull Request before merging
* Require 1 approval
* Dismiss stale PR approvals when new commits are pushed
* Require linear history
* Do not allow force push
* Do not allow deletion

Essa decisão garante governança corporativa e credibilidade técnica sem custo adicional.

---

#### ✅ Etapa 2 — Blindagem de segurança

Antes de tornar o código público, fizemos uma limpeza completa para garantir que **nenhum dado sensível fosse exposto**:

* `config.json` foi incluído no `.gitignore`
* Criado `config.example.json` limpo:

  ```json
  {
    "openai_api_key": "COLOQUE_SUA_CHAVE_AQUI",
    "safe_mode": true,
    "voice_enabled": true
  }
  ```
* Logs, cache, áudios e pastas locais foram ignorados:

  ```
  /__pycache__/
  /.venv/
  /logs/
  *.wav
  *.mp3
  *.json
  !config.example.json
  ```
* Implementado script `security_check.py` para auditoria automática de chaves hardcoded antes de qualquer release.

### 🧩 Política de Branches

| Branch       | Propósito                 | Regras                                                    |
| ------------ | ------------------------- | --------------------------------------------------------- |
| **main**     | Versão estável / Produção | Protegida. Apenas merges via PR e com revisão.            |
| **dev**      | Desenvolvimento ativo     | Livre para commits e testes. Fonte de merges para `main`. |
| **v2_cloud** | Roadmap SaaS futuro       | Branch experimental, não protegida.                       |

---

### 🧠 Processo Operacional

1. Todo novo código é feito em **dev**.
2. Quando estável, é feito **merge de dev → main** via PR.
3. A `main` só recebe commits revisados e testados.
4. A `v2_cloud` serve para testes e inovações não estáveis.

### 📜 Conclusão

Essa governança garante:

* Segurança de código e chaves
* Fluxo controlado de releases
* Proteção da branch principal
* Estrutura pronta para escalabilidade (SaaS)
* Conformidade com práticas de produto corporativo

A SolAgent agora segue o padrão de desenvolvimento de uma empresa real — com governança, segurança e rastreabilidade completas.

---

## 🎯 TL;DR

- **Problema:** GitHub não aplica proteção de branch em repos privados gratuitos
- **Solução:** Repositório público + blindagem de segurança + branch protection automática
- **Resultado:** Governança corporativa sem custo + credibilidade técnica
- **Estratégia:** `main` = produto estável, `dev` = laboratório, `v2_cloud` = roadmap SaaS

---

**Esta governança garante que a SolAgent mantenha qualidade empresarial e segurança de dados.**

*Atualizado em 29/10/2025 - SolAgent v1.2 com governança empresarial*