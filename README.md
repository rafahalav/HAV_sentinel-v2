# H.A.V. SENTINEL v2.0
## Hyper Application Vulnerability Sentinel

![Version](https://img.shields.io/badge/Version-2.0.0-blue)
![Build](https://img.shields.io/badge/Build-SENTINEL%20VIGILANCE-green)
![License](https://img.shields.io/badge/License-MIT-orange)

---

## 📋 Visão Geral

**H.A.V. SENTINEL** é um framework avançado de análise de segurança de aplicações que detecta vulnerabilidades em código-fonte, dependências, configurações e infraestrutura de rede.

### Características Principais

✅ **Análise Estática de Código** - Detecção de vulnerabilidades comuns (SQL Injection, XSS, etc.)
✅ **Análise de Dependências** - Identifica pacotes vulneráveis conhecidos
✅ **Verificação de Configuração** - Detecta secrets hardcoded, debug mode, conexões inseguras
✅ **Testes de Rede** - Port scanning e verificação de certificados SSL
✅ **Duas Interfaces** - CLI para terminal e GUI para desktop
✅ **Relatórios Detalhados** - JSON, HTML e exportação customizada
✅ **Banco de Dados de Vulnerabilidades** - Consulte CVEs e remediações
✅ **Threading Otimizado** - Processamento paralelo para melhor performance

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

#### 1. Clonar ou Baixar o Projeto

```bash
# Se estiver em um repositório git
git clone <repository-url>
cd hav-sentinel

# Ou simplesmente extrair os arquivos no diretório desejado
```

#### 2. Instalar Dependências Opcionais

```bash
# Instalar todas as dependências
pip install -r requirements.txt

# Ou instalar manualmente
pip install requests anthropic
```

#### 3. Para GUI (Opcional)

A maioria dos sistemas já tem tkinter instalado. Se não:

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS
brew install python-tk

# Windows - usar instalador oficial de Python com "tcl/tk" ativado
```

---

## 📖 Guia de Uso

### Iniciar o Launcher

```bash
python3 hav_sentinel_launcher.py
```

Será exibido um menu interativo para escolher entre **CLI** ou **GUI**.

### Opção 1: Modo Interactive

```bash
python3 hav_sentinel_launcher.py
# Selecione 1 para CLI ou 2 para GUI
```

### Opção 2: Linha de Comando

```bash
# Iniciar CLI
python3 hav_sentinel_launcher.py --cli

# Iniciar GUI
python3 hav_sentinel_launcher.py --gui

# CLI com alvo específico
python3 hav_sentinel_launcher.py --cli --target /caminho/aplicacao
```

---

## 🖥️ Interface CLI (Linha de Comando)

### Comandos Disponíveis

#### 1. `scan <caminho>`
Escaneia um diretório ou arquivo em busca de vulnerabilidades

```bash
sentinel $ scan /caminho/para/aplicacao
sentinel $ scan ./projeto-web
```

**O que faz:**
- Análise estática de código
- Verificação de dependências
- Análise de configuração
- Gera resumo de vulnerabilidades

#### 2. `analyze <arquivo>`
Analisa um arquivo específico para vulnerabilidades

```bash
sentinel $ analyze app.py
sentinel $ analyze config.json
```

#### 3. `report [json|html]`
Gera relatório do último scan executado

```bash
sentinel $ report json      # Gera JSON
sentinel $ report html      # Gera HTML
sentinel $ report           # Gera ambos
```

#### 4. `vulndb [list|search]`
Gerencia o banco de dados de vulnerabilidades

```bash
sentinel $ vulndb list                      # Lista todas
sentinel $ vulndb search SQL_INJECTION      # Busca específica
```

#### 5. `network [portscan|ssl]`
Executa testes de segurança de rede

```bash
sentinel $ network portscan 192.168.1.1
sentinel $ network ssl example.com 443
```

#### 6. `status`
Mostra status atual da sessão

```bash
sentinel $ status
```

#### 7. `config`
Mostra configurações do sistema

```bash
sentinel $ config
```

#### 8. `clear`
Limpa a tela

```bash
sentinel $ clear
```

#### 9. `help`
Mostra lista de comandos

```bash
sentinel $ help
```

#### 10. `exit`
Encerra o programa

```bash
sentinel $ exit
```

### Exemplo de Fluxo CLI

```bash
$ python3 hav_sentinel_launcher.py --cli

  [*] Digite 'help' para ver comandos disponíveis

sentinel $ scan /home/user/meu-projeto
  [SCAN] Iniciando análise de /home/user/meu-projeto
  [SCAN] Analisando arquivos...
  [+] Análise concluída: 15 problemas encontrados

  ┌─[VULNERABILITY: CRITICAL]─────────────────────────
  │ Title: SQL Injection Risk
  │ Target: /home/user/meu-projeto/models.py
  └─────────────────────────────────────────────

sentinel $ report html
  [+] Relatório HTML gerado: /home/user/hav_reports/report_20260525_143022.html

sentinel $ status
  Versão: 2.0.0
  Build: SENTINEL VIGILANCE
  Target Atual: /home/user/meu-projeto
  Vulnerabilidades Encontradas: 15

sentinel $ exit
```

---

## 🎨 Interface GUI (Gráfica)

### Abas Principais

#### 1. 🔍 Scan de Segurança
- Selecione o diretório a ser analisado
- Escolha os tipos de scan desejados
- Monitore progresso em tempo real
- Visualize logging detalhado

#### 2. 📊 Resultados
- Tabela com todas as vulnerabilidades
- Filtro por severidade (Critical, High, Medium, Low)
- Estatísticas resumidas
- Detalhes expandíveis de cada achado

#### 3. 📄 Relatórios
- Geração de relatórios em JSON, HTML
- Lista de relatórios recentes
- Acesso rápido à pasta de relatórios
- Histórico de exportações

#### 4. 🗄️ Banco de Vulnerabilidades
- Consulte vulnerabilidades conhecidas
- Busque por tipo ou CVE
- Veja remediações recomendadas
- Informações de severidade

#### 5. 🌐 Testes de Rede
- **Port Scan**: Escaneia portas comuns (22, 80, 443, 3306, 5432, etc.)
- **SSL Check**: Verifica certificados SSL/TLS
- Resultados em tempo real
- Histórico de testes

### Menu Superior

**Arquivo**
- Novo Scan
- Abrir Relatório
- Sair

**Ferramentas**
- Gerenciar Banco de Dados
- Limpador de Cache
- Abrir Logs

**Ajuda**
- Sobre
- Documentação

---

## 📊 Tipos de Vulnerabilidades Detectadas

### SQL Injection
- Detecta padrões de concatenação SQL
- Identifica queries dinâmicas inseguras
- **Remediação**: Use prepared statements

### XSS (Cross-Site Scripting)
- Scripts inline não sanitizados
- Event handlers perigosos
- **Remediação**: Implemente validação de entrada e codificação de saída

### Autenticação Fraca
- Senhas armazenadas inseguramente
- Falta de MFA
- **Remediação**: Implemente autenticação forte (OAuth2, MFA)

### Desserialização Insegura
- Uso de pickle.loads(), yaml.load()
- Entrada não validada em desserialização
- **Remediação**: Use método de desserialização seguro

### Traversal de Diretório
- Padrões "./" e "../" em paths
- **Remediação**: Valide e sanitize entradas de path

### Secrets Hardcoded
- API keys, tokens em código
- Senhas em plain text
- **Remediação**: Use variáveis de ambiente e secret managers

### Criptografia Insegura
- Algoritmos fracos (MD5, SHA1, DES)
- **Remediação**: Use SHA-256 ou superior

### Dependências Vulneráveis
- Pacotes com CVEs conhecidos
- Versões desatualizadas
- **Remediação**: Atualize para versões seguras

---

## 📁 Estrutura de Arquivos

```
hav-sentinel/
├── hav_sentinel_core.py        # Core do sistema (engines de análise)
├── hav_sentinel_cli.py         # Interface CLI
├── hav_sentinel_gui.py         # Interface GUI
├── hav_sentinel_launcher.py    # Launcher (seletor CLI/GUI)
├── README.md                   # Este arquivo
└── requirements.txt            # Dependências Python

Diretórios criados automaticamente:
~/.hav_logs/                    # Logs de execução
~/hav_reports/                  # Relatórios gerados
~/.hav_workspace/               # Área de trabalho
~/.hav_cache/                   # Cache do sistema
~/.hav_vulndb.json             # Banco de vulnerabilidades
```

---

## 📈 Relatórios Gerados

### Relatório JSON
```json
{
  "tool": "H.A.V. SENTINEL",
  "version": "2.0.0",
  "timestamp": "2026-05-25T14:30:22.000000",
  "target": "/caminho/aplicacao",
  "summary": {
    "total": 15,
    "critical": 2,
    "high": 5,
    "medium": 6,
    "low": 2
  },
  "findings": [
    {
      "severity": "CRITICAL",
      "title": "SQL Injection",
      "cve": "CVE-2023-XXXXX",
      "target": "models.py",
      "description": "...",
      "remediation": "..."
    }
  ]
}
```

### Relatório HTML
- Dashboard visual com gráficos
- Sumário executivo
- Detalhes de cada vulnerabilidade
- Recomendações de remediação
- Design responsivo

---

## ⚙️ Configuração

### Arquivo de Configuração

Localizado em: `~/.hav_sentinel.ini`

```ini
[AI]
api_key = sua_chave_aqui
model = claude-sonnet-4-20250514
max_tokens = 4096
temperature = 0.7

[NETWORK]
timeout = 5
threads = 200
retry = 2

[WORKSPACE]
dir = ~/.hav_workspace
auto_save = true
report_format = html,json,txt

[STEALTH]
user_agent = Mozilla/5.0...
delay_min = 0
delay_max = 0
randomize_headers = false
```

---

## 🔐 Segurança

### Boas Práticas

1. **Nunca armazene credentials no código**
   - Use variáveis de ambiente
   - Use secret managers

2. **Valide sempre a entrada do usuário**
   - Whitelist de valores esperados
   - Sanitização de caracteres perigosos

3. **Use HTTPS sempre**
   - Verifique certificados SSL
   - Mantenha TLS atualizado

4. **Atualize dependências regularmente**
   - Execute scans periódicos
   - Monitore CVE databases

5. **Implemente logging e auditoria**
   - Registre ações sensíveis
   - Mantenha histórico

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'tkinter'"

**Solução:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS
brew install python-tk

# Windows
Reinstale Python e marque "tcl/tk and IDLE"
```

### Erro: "Permission denied" ao criar logs

**Solução:**
```bash
chmod 755 ~/.hav_logs
chmod 755 ~/hav_reports
```

### GUI abre mas está lenta

**Solução:**
- Feche outras aplicações
- Reduza o tamanho do alvo de scan
- Use a CLI para scans grandes

### Scan não encontra nenhuma vulnerabilidade

**Verificar:**
- O caminho está correto?
- Arquivos têm permissão de leitura?
- Formato de arquivo é suportado? (.py, .js, .java, etc.)

---

## 📚 Exemplos de Uso

### Exemplo 1: Scan de Segurança Completo

```bash
python3 hav_sentinel_launcher.py --cli

sentinel $ scan ~/meuprojeto
sentinel $ report html
sentinel $ exit
# Relatório gerado em: ~/hav_reports/report_*.html
```

### Exemplo 2: Verificar Dependências

```bash
python3 hav_sentinel_launcher.py --cli

sentinel $ scan ~/meuprojeto
sentinel $ analyze ~/meuprojeto/requirements.txt
```

### Exemplo 3: Port Scan e SSL Check

```bash
python3 hav_sentinel_launcher.py --cli

sentinel $ network portscan example.com
sentinel $ network ssl example.com 443
```

### Exemplo 4: Usar GUI para Relatórios

```bash
python3 hav_sentinel_launcher.py --gui
# Interface gráfica abre
# 1. Selecione diretório na aba "Scan de Segurança"
# 2. Clique em "Iniciar Scan"
# 3. Veja resultados na aba "Resultados"
# 4. Gere relatórios na aba "Relatórios"
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está sob licença MIT. Veja `LICENSE` para detalhes.

---

## 📞 Suporte

### Documentação
- Veja `README.md` para guia completo
- Execute `help` na CLI
- Clique em "Ajuda" na GUI

### Relatórios de Bug
- Abra uma issue no GitHub
- Inclua: versão, SO, passos para reproduzir

### Contato
- Email: security@example.com
- Discussões: GitHub Discussions

---

## 🎯 Roadmap v3.0

- [ ] Integração com APIs de terceiros (Snyk, WhiteSource)
- [ ] Análise dinâmica com instrumentation
- [ ] Suporte a containers (Docker)
- [ ] Integração com CI/CD (GitHub Actions, GitLab CI)
- [ ] Machine Learning para detecção de anomalias
- [ ] Mobile app (iOS/Android)
- [ ] Dashboard online com histórico
- [ ] SBOM generation (Software Bill of Materials)

---

## 📊 Performance

### Benchmarks

| Alvo | Tamanho | Tempo Média |
|-----|---------|-----------|
| Projeto Pequeno (< 100 arquivos) | < 5 MB | 5-10s |
| Projeto Médio (100-1000 arquivos) | 5-50 MB | 30-60s |
| Projeto Grande (> 1000 arquivos) | > 50 MB | 2-5 min |

### Otimizações

- Threading paralelo para I/O
- Cache de resultados
- Índice de arquivos
- Regex compilado

---

## 🏆 Créditos

**H.A.V. SENTINEL v2.0**

Desenvolvido como framework avançado de segurança de aplicações.

---

## ⚠️ Disclaimer

**H.A.V. SENTINEL** é uma ferramenta de segurança para fins educacionais e de teste autorizado. 

- ✅ Use apenas em sistemas que você possui ou tem permissão
- ✅ Cumpra todas as leis e regulações aplicáveis
- ✅ Obtenha autorização antes de testar sistemas de terceiros
- ❌ Não use para atividades ilegais ou não autorizadas

Os autores não são responsáveis por uso indevido ou dano causado por esta ferramenta.

---

**Last Updated:** 2026-05-25
**Version:** 2.0.0
**Status:** Production Ready
