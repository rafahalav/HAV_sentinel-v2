# H.A.V. SENTINEL - Quick Start Guide

## ⚡ Comece em 5 Minutos

### 1️⃣ Instalação Básica

```bash
# Clone ou baixe os arquivos
cd hav-sentinel

# Instale dependências opcionais (recomendado)
pip install requests anthropic

# Para GUI (tkinter geralmente já vem instalado)
# Se não tiver:
# Ubuntu: sudo apt-get install python3-tk
# macOS: brew install python-tk
```

### 2️⃣ Primeiro Scan

#### Via CLI (Terminal)

```bash
# Modo interativo
python3 hav_sentinel_launcher.py

# Ou direto
python3 hav_sentinel_launcher.py --cli --target /caminho/projeto

# Executar comando específico
sentinel $ scan ~/meu-projeto
```

#### Via GUI (Interface Gráfica)

```bash
python3 hav_sentinel_launcher.py --gui
# Clique em "Procurar" e selecione seu projeto
# Clique em "Iniciar Scan"
# Veja os resultados na aba "Resultados"
```

### 3️⃣ Gerar Relatório

```bash
# CLI
sentinel $ report html

# GUI
# Vá para aba "Relatórios" → Clique em "Gerar HTML"
```

---

## 🎯 Cenários Comuns

### Cenário 1: Encontrar Vulnerabilidades de Segurança

```bash
python3 hav_sentinel_launcher.py --cli --target ./meu-app
# Espere a análise completar
# Os resultados mostrarão vulnerabilidades encontradas
```

### Cenário 2: Verificar Dependências Vulneráveis

```bash
python3 hav_sentinel_launcher.py --cli

sentinel $ scan ~/projeto
# Procure por achados em "MEDIUM" ou "HIGH" em dependências
```

### Cenário 3: Testar Segurança de Rede

```bash
python3 hav_sentinel_launcher.py --cli

sentinel $ network portscan seu-servidor.com
sentinel $ network ssl seu-servidor.com 443
```

### Cenário 4: Buscar Secrets Hardcoded

```bash
python3 hav_sentinel_launcher.py --cli

sentinel $ analyze ./config.py
sentinel $ analyze .env
# Procure por achados "HARDCODED_SECRETS"
```

---

## 📊 Entender os Resultados

### Níveis de Severidade

| Nível | Ícone | Descrição | Ação |
|-------|-------|-----------|------|
| **CRITICAL** | 🔴 | Risco imediato | CORRIGIR AGORA |
| **HIGH** | 🟠 | Risco importante | Corrigir em dias |
| **MEDIUM** | 🟡 | Risco moderado | Corrigir em semanas |
| **LOW** | 🔵 | Risco baixo | Corrigir quando possível |
| **INFO** | ℹ️ | Informação | Revisar |

### Exemplo de Resultado

```
  ┌─[VULNERABILITY: CRITICAL]─────────────────────────
  │ Title: SQL Injection Risk
  │ CVE: CVE-2023-XXXXX
  │ Target: app/models.py
  │ Desc: Query dinâmica usando concatenação de strings
  └─────────────────────────────────────────────
```

**O que fazer:**
1. Abra o arquivo `app/models.py`
2. Procure pela linha com concatenação SQL
3. Implemente prepared statements (queries parametrizadas)

---

## 🔍 Dicas e Truques

### CLI - Comandos Úteis

```bash
# Ver todos os comandos
sentinel $ help

# Ver status atual
sentinel $ status

# Buscar no banco de vulnerabilidades
sentinel $ vulndb search XSS
sentinel $ vulndb list

# Exportar em diferentes formatos
sentinel $ export json
sentinel $ export html
```

### GUI - Atalhos

- **Ctrl+C**: Não use! Use o botão "Parar" 
- **Tab**: Navegue entre campos
- **Enter**: Selecione diretório após "Procurar"

### Performance

```bash
# Scans grandes podem demorar
# Para acelerar, ignore diretórios:

# Diretórios ignorados automaticamente:
# .git, node_modules, __pycache__, .venv, venv

# Para projeto grande:
sentinel $ scan /caminho/projeto  # Pode demorar 2-5 min
```

---

## 📈 Próximos Passos

### 1. Configure Seu Projeto

```bash
# Identifique todos os achados CRITICAL e HIGH
python3 hav_sentinel_launcher.py --cli --target seu-projeto
```

### 2. Priorize Remediações

```bash
# Foque em CRITICAL primeiro
# Depois em HIGH
# Depois em MEDIUM
```

### 3. Gere Relatório para Stakeholders

```bash
# Abra a GUI e gere relatório HTML
python3 hav_sentinel_launcher.py --gui
# Aba "Relatórios" → "Gerar HTML"
# Abra o arquivo .html no navegador
```

### 4. Implemente Fixes

- Siga as recomendações de "Remediação"
- Teste localmente
- Execute novo scan para confirmar

### 5. Monitore Continuamente

```bash
# Execute scans regularmente
# Configure em seu CI/CD pipeline
# Gere relatórios periódicos
```

---

## ❓ FAQ

### P: Quanto tempo leva um scan?
**R:** Depende do tamanho:
- Pequeno (< 100 arquivos): 5-10 segundos
- Médio (100-1000 arquivos): 30-60 segundos
- Grande (> 1000 arquivos): 2-5 minutos

### P: Posso testar produção?
**R:** ⚠️ **Não recomendado**
- Use em desenvolvimento/staging primeiro
- Obtenha aprovação antes de testar produção
- O scan é read-only, não modifica nada

### P: Como integrar no CI/CD?
**R:** 
```yaml
# GitHub Actions exemplo
- name: Security Scan
  run: python3 hav_sentinel_launcher.py --cli --target ./src
```

### P: Posso exportar resultados?
**R:** Sim! Vários formatos:
```bash
sentinel $ report json  # JSON para integração
sentinel $ report html  # HTML para visualização
```

### P: Como atualizar o banco de vulnerabilidades?
**R:**
```bash
sentinel $ vulndb list  # Ver o banco atual
# O banco é atualizado automaticamente com novas vulnerabilidades
```

---

## 🚨 Problemas Comuns

### Problema: "Permission denied"
```bash
# Solução:
chmod +x hav_sentinel_*.py
```

### Problema: "No module named 'tkinter'"
```bash
# Ubuntu/Debian:
sudo apt-get install python3-tk

# macOS:
brew install python-tk
```

### Problema: GUI muito lenta
```bash
# Solução:
# 1. Feche outras aplicações
# 2. Use CLI para projetos grandes
# 3. Reduza número de workers: edite hav_sentinel_core.py MAX_THREADS
```

### Problema: Scan não encontra nada
```bash
# Verificar:
# 1. Caminho está correto? (use caminho absoluto)
# 2. Arquivos têm permissão de leitura? (ls -la)
# 3. Formatos suportados? (.py, .js, .java, etc.)
```

---

## 📚 Recursos Adicionais

### Documentação Completa
```bash
cat README.md
```

### Exemplos de Código Vulnerável
```bash
# Veja comentários em hav_sentinel_core.py
# Seção: VulnerabilityDatabase
```

### CVEs e Remediações
```bash
sentinel $ vulndb search <termo>
# Mostra CVE, severidade e como corrigir
```

---

## 🎓 Entender Vulnerabilidades

### SQL Injection
```python
# ❌ Errado
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ Correto
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

### XSS (Cross-Site Scripting)
```python
# ❌ Errado
return f"<h1>{user_input}</h1>"

# ✅ Correto
from flask import escape
return f"<h1>{escape(user_input)}</h1>"
```

### Hardcoded Secrets
```python
# ❌ Errado
API_KEY = "sk-1234567890abcdef"

# ✅ Correto
import os
API_KEY = os.getenv("API_KEY")
```

---

## 📞 Precisa de Ajuda?

1. **Verifique FAQ acima**
2. **Leia README.md completo**
3. **Veja exemplos em EXAMPLES.md**
4. **Execute `help` na CLI**

---

**Boa sorte com seus testes de segurança! 🚀**

*H.A.V. SENTINEL v2.0 - Sentinel Vigilance*
