# 🛡️ SolAgent - Governança e Proteção de Branches

## 📋 O Problema Técnico

Estamos tentando proteger a branch `main` do repositório `SolAgent` usando regras de proteção de branch (branch protection rules).

Essas regras são importantes porque queremos garantir que:
- ninguém faça push direto para `main`
- qualquer mudança na `main` só aconteça via pull request
- ninguém apague a `main`
- ninguém consiga dar `force push` e sobrescrever histórico

Isso é **padrão de governança de produto**.

### ⚠️ Limitação Descoberta

O GitHub mostrou o aviso:
> "Rules on your private repos can't be enforced until you upgrade to GitHub Team or Enterprise."

**Tradução direta:**
- Como o repositório está privado e a conta é pessoal/gratuita, o GitHub salva a regra mas **NÃO aplica de verdade**
- Na prática, ainda dá pra dar `push origin main` direto e quebrar tudo

## 🎯 Por Que Isso Importa Para a SolAgent

A SolAgent não é mais um script pessoal. Agora é um **produto** com:

- **`main`** → versão estável e vendável (v1.2)
- **`dev`** → linha de desenvolvimento ativo  
- **`v2_cloud`** → roadmap SaaS

A `main` precisa estar protegida porque:
- é a versão que será mostrada para cliente e investidor
- é a que vamos demonstrar em vídeo
- é a que precisa rodar **SEM quebrar**

**Se a `main` quebrar por um push direto errado, perdemos: confiança, demo, credibilidade.**

## 🔧 Plano de Solução (2 Etapas)

### Etapa A — Blindagem Técnica

Garantir que nenhum dado sensível possa vazar antes de tornar público:

1. **Proteger credenciais:**
   - ✅ `config.json` no `.gitignore`  
   - ✅ Manter apenas `config.example.json` com campos falsos
   - ✅ Nunca commitar chaves OpenAI

2. **Proteger dados do usuário:**
   - ✅ Arquivos de áudio (`.wav`, `.mp3`) excluídos
   - ✅ Logs pessoais excluídos
   - ✅ Cache do Whisper excluído

3. **Código limpo:**
   - ✅ Sem credenciais hardcoded
   - ✅ Leitura sempre do `config.json` local

### Etapa B — Ativar Proteção Real

**Opção 1: Repositório Público** (RECOMENDADA)
- Tornar `SolAgent` **público** ativa as regras de proteção automaticamente
- Pull request obrigatório ✅
- Force push bloqueado ✅  
- Main protegida ✅
- **Estratégia:** Produto open-source, venda serviços premium

**Opção 2: Disciplina Manual** (privado)
- Fluxo interno rígido:
  1. Todo trabalho em `dev`
  2. Merge controlado `dev` → `main`
  3. **NUNCA** push direto na `main`

## 📐 Política Operacional

### Estrutura de Branches:
- **`main`** = "PRODUTO LIBERADO" (sempre estável, sempre funcional)
- **`dev`** = "LABORATÓRIO" (desenvolvimento ativo, testes)  
- **`v2_cloud`** = "ROADMAP SaaS" (funcionalidades futuras)

### Fluxo de Trabalho:
```bash
# Desenvolvimento
git checkout dev
git pull origin dev
# ... fazer mudanças ...
git commit -m "feat: nova funcionalidade"
git push origin dev

# Quando estável, merge para main
git checkout main
git merge dev
git push origin main
```

### Regras de Ouro:
1. **Main é sagrada** - só recebe código testado e funcional
2. **Dev é playground** - pode quebrar, pode experimentar
3. **V2_cloud é visão** - roadmap para o futuro SaaS

## 🎯 TL;DR

- **Problema:** GitHub não aplica proteção de branch em repos privados gratuitos
- **Risco:** Push direto na `main` pode quebrar versão vendável
- **Solução:** Blindagem de dados + disciplina operacional + eventual migração para público
- **Estratégia:** `main` = produto, `dev` = laboratório, `v2_cloud` = SaaS

---

**Esta governança garante que a SolAgent mantenha qualidade empresarial mesmo em repositório pessoal.**

*Criado em 29/10/2025 - SolAgent v1.2*