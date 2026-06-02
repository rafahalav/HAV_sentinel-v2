# H.A.V. SENTINEL - Exemplos Práticos

## 📋 Tabela de Conteúdos

1. [Exemplos CLI](#exemplos-cli)
2. [Exemplos GUI](#exemplos-gui)
3. [Casos de Uso Reais](#casos-de-uso-reais)
4. [Integração CI/CD](#integração-cicd)
5. [Scripts de Automação](#scripts-de-automação)

---

## Exemplos CLI

### Exemplo 1: Scan Básico

```bash
$ python3 hav_sentinel_launcher.py --cli

sentinel $ scan ~/meu-projeto

  [SCAN] Iniciando análise de /home/user/meu-projeto
  [SCAN] Analisando arquivos...
  
  ┌─[VULNERABILITY: CRITICAL]─────────────────────────
  │ Title: SQL Injection Risk
  │ CVE: CVE-2023-XXXXX
  │ Target: /home/user/meu-projeto/models.py
  │ Desc: Query dinâmica usando f-strings
  └─────────────────────────────────────────────

  [+] Análise concluída: 15 problemas encontrados
  
    [CRITICAL]  2
    [HIGH]      5
    [MEDIUM]    6
    [LOW]       2
    ────────────
    Total      15

sentinel $ 
```

### Exemplo 2: Analisar Arquivo Específico

```bash
$ python3 hav_sentinel_launcher.py --cli

sentinel $ analyze app/controllers/user_controller.py

  [*] Analisando: app/controllers/user_controller.py

  Vulnerabilidades encontradas:

  1. [HIGH] SQL Injection
     Arquivo: app/controllers/user_controller.py
     CVE: CVE-2023-XXXXX

  2. [MEDIUM] Missing Input Validation
     Arquivo: app/controllers/user_controller.py

  3. [HIGH] Insecure Password Hashing
     Arquivo: app/controllers/user_controller.py

sentinel $ 
```

### Exemplo 3: Gerar Relatórios

```bash
$ python3 hav_sentinel_launcher.py --cli

sentinel $ scan ~/projeto-web

  [+] Análise concluída: 8 problemas encontrados

sentinel $ report html

  [+] Relatório HTML gerado: /home/user/hav_reports/report_20260525_143022.html

sentinel $ report json

  [+] Relatório JSON gerado: /home/user/hav_reports/report_20260525_143022.json

sentinel $ 
```

### Exemplo 4: Buscar no Banco de Vulnerabilidades

```bash
$ python3 hav_sentinel_launcher.py --cli

sentinel $ vulndb list

  Vulnerabilidades conhecidas:

  ● SQL_INJECTION
    CVE: CVE-2023-XXXXX
    Severidade: CRITICAL
    Remediação: Use prepared statements and parameterized queries

  ● XSS
    CVE: CVE-2023-XXXXX
    Severidade: HIGH
    Remediação: Implement proper input validation and output encoding

  ● WEAK_AUTH
    CVE: CWE-521
    Severidade: HIGH
    Remediação: Implement strong authentication mechanisms (MFA, OAuth2)

  [... mais vulnerabilidades ...]

sentinel $ 
```

### Exemplo 5: Buscar Vulnerabilidade Específica

```bash
$ python3 hav_sentinel_launcher.py --cli

sentinel $ vulndb search INJECTION

  Buscando: injection

  ● SQL_INJECTION
    CVE: CVE-2023-XXXXX
    Severidade: CRITICAL
    Remediação: Use prepared statements and parameterized queries

  ● INSECURE_DESERIALIZATION
    CVE: CVE-2023-XXXXX
    Severidade: CRITICAL
    Remediação: Use safe deserialization methods and validate all input

sentinel $ 
```

### Exemplo 6: Testes de Rede

```bash
$ python3 hav_sentinel_launcher.py --cli

sentinel $ network portscan 192.168.1.100

  [SCAN] Iniciando port scan em 192.168.1.100

  Resultado do Port Scan:

  ✓ Porta 22 - ABERTA
  ✓ Porta 80 - ABERTA
  ✓ Porta 443 - ABERTA
  ✓ Porta 3306 - ABERTA

sentinel $ network ssl example.com 443

  Certificado SSL/TLS:

  Status: Válido
  Subject: {'commonName': 'example.com', 'organizationName': 'Example Inc'}
  Válido até: May 25, 2027

sentinel $ 
```

### Exemplo 7: Verificar Status

```bash
$ python3 hav_sentinel_launcher.py --cli

sentinel $ status

  ───────────────────────────────────────
  STATUS
  ───────────────────────────────────────

  Versão: 2.0.0
  Build: SENTINEL VIGILANCE
  Target Atual: /home/user/meu-projeto
  Scans Executados: 3
  Vulnerabilidades Encontradas: 27
  Críticas/Altas: 12
  Diretório de Relatórios: /home/user/hav_reports

sentinel $ 
```

### Exemplo 8: Session com Múltiplos Scans

```bash
$ python3 hav_sentinel_launcher.py --cli

sentinel $ scan ~/projeto-a
  [+] Análise concluída: 5 problemas encontrados

sentinel $ scan ~/projeto-b
  [+] Análise concluído: 12 problemas encontrados

sentinel $ scan ~/projeto-c
  [+] Análise concluída: 3 problemas encontrados

sentinel $ report html
  [+] Relatório agregado gerado: /home/user/hav_reports/report_*.html

sentinel $ status
  Vulnerabilidades Encontradas: 20  # Total de todos os scans

sentinel $ exit
```

---

## Exemplos GUI

### Fluxo Básico da GUI

```
1. Abrir aplicação
   └─ python3 hav_sentinel_launcher.py --gui

2. Aba "Scan de Segurança"
   └─ Clique em "Procurar" → Selecione /caminho/projeto
   └─ Verifique opções de scan (todas marcadas por padrão)
   └─ Clique em "Iniciar Scan"
   └─ Acompanhe progresso em tempo real

3. Aba "Resultados"
   └─ Veja tabela com vulnerabilidades encontradas
   └─ Resumo: CRITICAL (2) | HIGH (5) | MEDIUM (6) | LOW (2)
   └─ Clique em vulnerabilidade para ver detalhes

4. Aba "Relatórios"
   └─ Clique em "Gerar HTML" ou "Gerar JSON"
   └─ Abra arquivo gerado no navegador/editor

5. Aba "Banco de Vulnerabilidades"
   └─ Busque por tipo de vulnerabilidade
   └─ Veja CVE, severidade e remediação

6. Aba "Testes de Rede"
   └─ Digite host/IP
   └─ Clique "Port Scan" para testar portas
   └─ Clique "SSL Check" para verificar certificado
```

### Interpretando o Dashboard

```
┌─ Resumo ──────────────────────────────────────┐
│                                                │
│ CRITICAL: 2  HIGH: 5  MEDIUM: 6  LOW: 2      │
│                                                │
└────────────────────────────────────────────────┘

┌─ Vulnerabilidades Encontradas ─────────────────┐
│                                                │
│ ID  Severidade   Tipo              Alvo   CVE │
│ 1   CRITICAL     SQL Injection     app.py ...│
│ 2   HIGH         XSS               ...    ...│
│ 3   MEDIUM       Weak Auth         ...    ...│
│ ...                                           │
│                                                │
└────────────────────────────────────────────────┘
```

---

## Casos de Uso Reais

### Caso 1: Aplicação Web Python/Django

```bash
# Estrutura do projeto
meu-projeto/
├── manage.py
├── requirements.txt
├── app/
│   ├── models.py       # Pode ter SQL Injection
│   ├── views.py        # Pode ter XSS
│   └── forms.py
└── config/
    └── settings.py     # Pode ter secrets hardcoded

# Scan
python3 hav_sentinel_launcher.py --cli --target ~/meu-projeto

# Resultados esperados:
# - Vulnerabilidades em models.py (SQL Injection)
# - Vulnerabilidades em views.py (XSS, CSRF)
# - Secrets em settings.py (API_KEY hardcoded)
# - Pacotes vulneráveis em requirements.txt (Django, requests)

# Ações corretivas:
# 1. Django ORM em vez de queries brutas
# 2. Template escaping automático
# 3. Usar django-environ ou secrets
# 4. Atualizar dependências
```

### Caso 2: Node.js/Express API

```bash
# Estrutura
app/
├── package.json
├── .env.example
├── src/
│   ├── routes/
│   ├── controllers/
│   └── models/
└── config.js

# Scan
python3 hav_sentinel_launcher.py --cli --target ~/app

# Vulnerabilidades típicas encontradas:
# - SQL Injection em queries não parametrizadas
# - XSS em tratamento de entrada
# - Secrets em .env (não adicionado a .gitignore)
# - Dependências desatualizadas (npm audit)

# Ações:
# 1. Usar prepared statements (parameterized queries)
# 2. Sanitizar entrada (express-sanitizer)
# 3. Usar .env com dotenv
# 4. npm audit fix
```

### Caso 3: Java Application

```bash
# Estrutura
project/
├── pom.xml          # Dependências Maven
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   ├── models/
│   │   │   ├── controllers/
│   │   │   └── security/
│   │   └── resources/
│   │       └── application.properties

# Scan
python3 hav_sentinel_launcher.py --cli --target ~/project

# Vulnerabilidades:
# - Desserialização insegura (ObjectInputStream)
# - Hardcoded credentials em properties
# - Dependências vulneráveis (Spring, libraries)
# - SQL Injection em JDBC

# Ações:
# 1. Usar PreparedStatement sempre
# 2. Externalize configuration
# 3. Atualize dependências
# 4. Use Spring Security
```

### Caso 4: Auditoria de Configuração

```bash
# Arquivos a verificar
config/
├── database.yml       # Senhas hardcoded?
├── secrets.yml        # Secrets em VCS?
├── nginx.conf         # HTTPS habilitado?
├── .env.prod          # Keys expostas?
└── docker-compose.yml # Vulnerabilidades?

# Scan específico
python3 hav_sentinel_launcher.py --cli

sentinel $ analyze config/database.yml
sentinel $ analyze config/.env.prod
sentinel $ analyze docker-compose.yml

# Procurar por:
# - Passwords em plain text
# - API keys
# - Admin credentials
# - Default credentials
```

---

## Integração CI/CD

### GitHub Actions

```yaml
name: Security Scan with H.A.V. SENTINEL

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install H.A.V. SENTINEL
      run: |
        cp hav_sentinel*.py $GITHUB_WORKSPACE/
        pip install requests anthropic
    
    - name: Run Security Scan
      run: |
        python3 hav_sentinel_launcher.py --cli \
          --target ${{ github.workspace }} > scan_report.txt
    
    - name: Upload Report
      uses: actions/upload-artifact@v3
      with:
        name: security-report
        path: scan_report.txt
    
    - name: Check for Critical Issues
      run: |
        if grep -q "CRITICAL" scan_report.txt; then
          echo "Critical vulnerabilities found!"
          exit 1
        fi
```

### GitLab CI

```yaml
stages:
  - scan

security_scan:
  stage: scan
  image: python:3.10
  script:
    - pip install requests anthropic
    - cp hav_sentinel*.py .
    - python3 hav_sentinel_launcher.py --cli --target ./
  artifacts:
    reports:
      - security_report.json
    paths:
      - reports/
  allow_failure: false
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    stages {
        stage('Security Scan') {
            steps {
                script {
                    sh 'pip install requests anthropic'
                    sh 'cp hav_sentinel*.py .'
                    sh '''
                        python3 hav_sentinel_launcher.py --cli \
                            --target ${WORKSPACE} \
                            > security_scan.log
                    '''
                }
            }
        }
        
        stage('Parse Results') {
            steps {
                script {
                    if (sh(script: 'grep -q CRITICAL security_scan.log', returnStatus: true) == 0) {
                        error('Critical vulnerabilities found!')
                    }
                }
            }
        }
        
        stage('Generate Report') {
            steps {
                archiveArtifacts artifacts: 'security_scan.log'
            }
        }
    }
}
```

---

## Scripts de Automação

### Script 1: Scan Múltiplos Projetos

```bash
#!/bin/bash
# scan_all_projects.sh

PROJECTS_DIR="/home/user/projects"
REPORT_DIR="/home/user/hav_reports"

for project in $(ls $PROJECTS_DIR); do
    echo "Scanning $project..."
    python3 hav_sentinel_launcher.py --cli \
        --target "$PROJECTS_DIR/$project" \
        > "$REPORT_DIR/${project}_scan.log"
    
    # Gerar relatório
    echo "Generating report for $project..."
    python3 -c "
from hav_sentinel_core import ReportGenerator
import json

with open('$REPORT_DIR/${project}_scan.log', 'r') as f:
    content = f.read()
    
report_gen = ReportGenerator()
report_gen.generate_html_report([], '$project')
"
done

echo "All scans completed!"
```

### Script 2: Monitoramento Contínuo

```bash
#!/bin/bash
# continuous_security_monitor.sh

while true; do
    echo "[$(date)] Starting security scan..."
    
    python3 hav_sentinel_launcher.py --cli \
        --target ~/aplicacao \
        >> ~/hav_logs/monitor.log 2>&1
    
    # Verificar por vulnerabilidades críticas
    if grep -q "CRITICAL" ~/hav_logs/monitor.log; then
        echo "ALERT: Critical vulnerability detected!"
        # Enviar notificação
        # mail -s "Security Alert" admin@example.com < alert.txt
    fi
    
    # Aguardar 24 horas
    sleep 86400
done
```

### Script 3: Comparador de Scans

```python
#!/usr/bin/env python3
# compare_scans.py

import json
import sys
from datetime import datetime

def compare_reports(report1, report2):
    """Compara dois relatórios de scan"""
    
    with open(report1, 'r') as f:
        scan1 = json.load(f)
    
    with open(report2, 'r') as f:
        scan2 = json.load(f)
    
    findings1 = set(str(f) for f in scan1['findings'])
    findings2 = set(str(f) for f in scan2['findings'])
    
    new_vulns = findings2 - findings1
    fixed_vulns = findings1 - findings2
    persistent = findings1 & findings2
    
    print(f"Novas Vulnerabilidades: {len(new_vulns)}")
    print(f"Vulnerabilidades Corrigidas: {len(fixed_vulns)}")
    print(f"Vulnerabilidades Persistentes: {len(persistent)}")
    
    if new_vulns:
        print("\nNovas:")
        for vuln in list(new_vulns)[:5]:
            print(f"  - {vuln[:80]}")
    
    if fixed_vulns:
        print("\nCorrigidas:")
        for vuln in list(fixed_vulns)[:5]:
            print(f"  - {vuln[:80]}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 compare_scans.py report1.json report2.json")
        sys.exit(1)
    
    compare_reports(sys.argv[1], sys.argv[2])
```

### Script 4: Automação com Cronjob

```bash
# /etc/cron.d/hav-sentinel-scan

# Executar scan diariamente às 02:00 AM
0 2 * * * /home/user/scripts/daily_security_scan.sh

# Gerar relatório semanal às 08:00 AM de segunda
0 8 * * 1 /home/user/scripts/weekly_report.sh

# Arquivo: daily_security_scan.sh
#!/bin/bash
cd /home/user/hav-sentinel
python3 hav_sentinel_launcher.py --cli --target ~/aplicacao
```

---

## Dicas de Ouro 🌟

### 1. Filtrando Resultados

```bash
# Buscar apenas CRITICAL
sentinel $ scan ~/projeto | grep CRITICAL

# Buscar apenas um tipo de vulnerabilidade
sentinel $ analyze file.py | grep "SQL"
```

### 2. Comparando com Scans Anteriores

```bash
# Manter relatórios datados
python3 hav_sentinel_launcher.py --cli --target ~/projeto
# Relatório salvo com timestamp automático
```

### 3. Integrando com Other Tools

```bash
# Exportar para JSON e processar com jq
sentinel $ report json | jq '.findings[] | select(.severity=="CRITICAL")'

# Enviar relatório por email
sentinel $ report html
mail -s "Security Report" team@example.com < report_*.html
```

### 4. Criando Baselines

```bash
# Primeiro scan como baseline
python3 hav_sentinel_launcher.py --cli --target ~/proj > baseline.txt

# Comparar contra baseline periodicamente
python3 hav_sentinel_launcher.py --cli --target ~/proj > current.txt
diff baseline.txt current.txt
```

---

**Pronto para começar? Execute: `python3 hav_sentinel_launcher.py` 🚀**
