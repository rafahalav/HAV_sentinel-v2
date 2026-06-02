#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║       H.A.V. SENTINEL — Hyper Application Vulnerability Sentinel               ║
# ║              Advanced Application Security Analysis Framework                   ║
# ║                          Version 2.0 — Production Ready                         ║
# ╚══════════════════════════════════════════════════════════════════════════════════╝

"""
H.A.V. SENTINEL Core Module
============================
Framework avançado de análise de vulnerabilidades de aplicações
com suporte a scanning de segurança, análise estática/dinâmica e geração de relatórios
"""

import os, sys, re, json, time, socket, struct, random, string, hashlib
import subprocess, threading, queue, logging, base64, binascii, shutil
import urllib.request, urllib.parse, urllib.error, http.client, ssl
import ipaddress, platform, getpass, argparse, textwrap, signal, stat
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple, Set
from collections import defaultdict, OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
import configparser, csv, tempfile, mimetypes
import hashlib as hl

# ─────────────────────────────────────────────
#  DETECÇÃO DE DEPENDÊNCIAS
# ─────────────────────────────────────────────
try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

try:
    from anthropic import Anthropic
    ANTHROPIC_OK = True
except ImportError:
    ANTHROPIC_OK = False

try:
    import readline
    READLINE_OK = True
except ImportError:
    READLINE_OK = False

try:
    import hashlib as hashlib_lib
    import hmac
    CRYPTO_OK = True
except ImportError:
    CRYPTO_OK = False

# ─────────────────────────────────────────────
#  CONSTANTES E CONFIGURAÇÃO
# ─────────────────────────────────────────────
VERSION = "2.0.0"
CODENAME = "SENTINEL VIGILANCE"
BUILD_DATE = "2026"
AUTHOR = "Security Operations"

CONFIG_FILE = os.path.expanduser("~/.hav_sentinel.ini")
LOG_DIR = os.path.expanduser("~/.hav_logs")
REPORT_DIR = os.path.expanduser("~/hav_reports")
WORKSPACE_DIR = os.path.expanduser("~/.hav_workspace")
HISTORY_FILE = os.path.expanduser("~/.hav_history")
CACHE_DIR = os.path.expanduser("~/.hav_cache")
VULN_DB = os.path.expanduser("~/.hav_vulndb.json")

MAX_THREADS = 200
DEFAULT_TIMEOUT = 5
AI_MODEL = "claude-sonnet-4-20250514"

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(WORKSPACE_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

# ─────────────────────────────────────────────
#  PALETA ANSI — DESIGN MODERNO
# ─────────────────────────────────────────────
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDER = "\033[4m"
    BLINK = "\033[5m"
    REV = "\033[7m"
    
    # Foreground
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright
    BRED = "\033[91m"
    BGREEN = "\033[92m"
    BYELLOW = "\033[93m"
    BBLUE = "\033[94m"
    BMAGENTA = "\033[95m"
    BCYAN = "\033[96m"
    BWHITE = "\033[97m"
    
    # Background
    BGBLACK = "\033[40m"
    BGRED = "\033[41m"
    BGGREEN = "\033[42m"
    BGYELLOW = "\033[43m"
    BGBLUE = "\033[44m"
    BGMAGENTA = "\033[45m"
    BGCYAN = "\033[46m"
    BGWHITE = "\033[47m"
    
    # Compostos
    PROMPT = "\033[1m\033[96m"
    SUCCESS = "\033[1m\033[92m"
    FAIL = "\033[1m\033[91m"
    WARN = "\033[1m\033[93m"
    INFO = "\033[1m\033[94m"
    CRITICAL = "\033[1m\033[31m"
    SCAN = "\033[1m\033[35m"
    VULN = "\033[1m\033[91m"
    PASS = "\033[1m\033[92m"
    ALERT = "\033[5m\033[1m\033[91m"

def colorize(text: str, *attrs) -> str:
    return "".join(attrs) + text + C.RESET

# ─────────────────────────────────────────────
#  LOGGER AVANÇADO
# ─────────────────────────────────────────────
class SentinelLogger:
    def __init__(self, name: str = "HAV_SENTINEL"):
        self.log_file = os.path.join(LOG_DIR, f"sentinel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        logging.basicConfig(
            filename=self.log_file,
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.logger = logging.getLogger(name)
        self.findings: List[Dict] = []
        self.metrics = {"scans": 0, "vulns_found": 0, "high_risk": 0}

    def info(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{C.DIM}[{ts}]{C.RESET} {C.INFO}[*]{C.RESET} {msg}")
        self.logger.info(msg)

    def success(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{C.DIM}[{ts}]{C.RESET} {C.SUCCESS}[+]{C.RESET} {msg}")
        self.logger.info(f"SUCCESS: {msg}")

    def warn(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{C.DIM}[{ts}]{C.RESET} {C.WARN}[!]{C.RESET} {msg}")
        self.logger.warning(msg)

    def error(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{C.DIM}[{ts}]{C.RESET} {C.FAIL}[-]{C.RESET} {msg}")
        self.logger.error(msg)

    def critical(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{C.DIM}[{ts}]{C.RESET} {C.CRITICAL}[CRITICAL]{C.RESET} {C.BOLD}{msg}{C.RESET}")
        self.logger.critical(msg)

    def scan(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{C.DIM}[{ts}]{C.RESET} {C.SCAN}[SCAN]{C.RESET} {msg}")
        self.logger.info(f"SCAN: {msg}")

    def vulnerability(self, severity: str, title: str, desc: str, target: str = "", cve: str = ""):
        f = {
            "id": len(self.findings),
            "time": datetime.now().isoformat(),
            "severity": severity,
            "title": title,
            "description": desc,
            "target": target,
            "cve": cve,
            "remediation": ""
        }
        self.findings.append(f)
        self.metrics["vulns_found"] += 1
        
        if severity in ["CRITICAL", "HIGH"]:
            self.metrics["high_risk"] += 1
        
        colors = {
            "CRITICAL": C.FAIL,
            "HIGH": C.BRED,
            "MEDIUM": C.WARN,
            "LOW": C.BBLUE,
            "INFO": C.BCYAN
        }
        color = colors.get(severity, C.WHITE)
        
        print(f"\n  {C.BOLD}{color}┌─[VULNERABILITY: {severity}]─────────────────────────{C.RESET}")
        print(f"  {color}│{C.RESET} {C.BOLD}Title:{C.RESET} {title}")
        if cve:
            print(f"  {color}│{C.RESET} {C.BOLD}CVE:{C.RESET} {cve}")
        print(f"  {color}│{C.RESET} {C.BOLD}Target:{C.RESET} {target}")
        print(f"  {color}│{C.RESET} {C.BOLD}Desc:{C.RESET} {desc}")
        print(f"  {C.BOLD}{color}└─────────────────────────────────────────────{C.RESET}\n")
        
        self.logger.critical(f"VULNERABILITY [{severity}] {title} | CVE: {cve} | {target} | {desc}")

log = SentinelLogger()

# ─────────────────────────────────────────────
#  BANCO DE DADOS DE VULNERABILIDADES
# ─────────────────────────────────────────────
class VulnerabilityDatabase:
    def __init__(self):
        self.db = self._load_or_create_db()
        self.common_vulns = {
            "SQL_INJECTION": {
                "cve": "CVE-2023-XXXXX",
                "severity": "CRITICAL",
                "patterns": [r"(?:union|select|insert|update|delete)\s+(?:from|into|where)", r"(?:or|and)\s+1=1"],
                "remediation": "Use prepared statements and parameterized queries"
            },
            "XSS": {
                "cve": "CVE-2023-XXXXX",
                "severity": "HIGH",
                "patterns": [r"<script[^>]*>", r"javascript:", r"on\w+\s*="],
                "remediation": "Implement proper input validation and output encoding"
            },
            "WEAK_AUTH": {
                "cve": "CWE-521",
                "severity": "HIGH",
                "patterns": [r"password['\"]?\s*[:=]", r"api[_-]?key\s*[:=]"],
                "remediation": "Implement strong authentication mechanisms (MFA, OAuth2)"
            },
            "INSECURE_DESERIALIZATION": {
                "cve": "CVE-2023-XXXXX",
                "severity": "CRITICAL",
                "patterns": [r"pickle\.\w+|yaml\.load|json\.loads"],
                "remediation": "Use safe deserialization methods and validate all input"
            },
            "PATH_TRAVERSAL": {
                "cve": "CVE-2023-XXXXX",
                "severity": "HIGH",
                "patterns": [r"\.\./", r"\.\.", r"%2e%2e"],
                "remediation": "Validate and sanitize all file path inputs"
            },
            "HARDCODED_SECRETS": {
                "cve": "CWE-798",
                "severity": "HIGH",
                "patterns": [r"(?:secret|password|api_key|token)\s*=\s*['\"]([^'\"]+)['\"]"],
                "remediation": "Use environment variables and secret management tools"
            },
            "INSECURE_CRYPTO": {
                "cve": "CVE-2023-XXXXX",
                "severity": "HIGH",
                "patterns": [r"MD5|SHA1|DES|RC4"],
                "remediation": "Use SHA-256 or stronger cryptographic algorithms"
            },
            "MISSING_VALIDATION": {
                "cve": "CWE-20",
                "severity": "MEDIUM",
                "patterns": [r"without.*validat|skip.*validat"],
                "remediation": "Implement comprehensive input validation"
            }
        }

    def _load_or_create_db(self) -> Dict:
        if os.path.exists(VULN_DB):
            try:
                with open(VULN_DB, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"vulnerabilities": [], "last_updated": datetime.now().isoformat()}

    def save_db(self):
        with open(VULN_DB, 'w') as f:
            json.dump(self.db, f, indent=2)

    def add_vulnerability(self, vuln: Dict):
        self.db["vulnerabilities"].append({
            **vuln,
            "timestamp": datetime.now().isoformat()
        })
        self.save_db()

    def get_severity_score(self, severity: str) -> int:
        scores = {"CRITICAL": 100, "HIGH": 80, "MEDIUM": 60, "LOW": 30, "INFO": 10}
        return scores.get(severity, 0)

vuln_db = VulnerabilityDatabase()

# ─────────────────────────────────────────────
#  ANALISADORES DE SEGURANÇA
# ─────────────────────────────────────────────
class StaticCodeAnalyzer:
    """Análise estática de código"""
    def __init__(self):
        self.findings = []

    def analyze_file(self, filepath: str) -> List[Dict]:
        """Analisa um arquivo em busca de vulnerabilidades"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            self.findings = []
            file_ext = Path(filepath).suffix.lower()
            
            if file_ext in ['.py', '.js', '.ts', '.java', '.go', '.rb', '.php']:
                self._scan_python(content, filepath) if file_ext == '.py' else None
                self._scan_generic(content, filepath)
            
            return self.findings
        except Exception as e:
            log.error(f"Erro analisando {filepath}: {e}")
            return []

    def _scan_python(self, content: str, filepath: str):
        """Análise específica para Python"""
        issues = [
            (r"exec\s*\(", "Dynamic Code Execution", "CRITICAL"),
            (r"eval\s*\(", "Eval Usage", "HIGH"),
            (r"subprocess.*shell\s*=\s*True", "Shell Injection Risk", "CRITICAL"),
            (r"pickle\.\w+", "Insecure Deserialization", "CRITICAL"),
            (r"yaml\.load\s*\((?!.*Loader)", "YAML Injection", "HIGH"),
            (r"import\s+os.*os\.system", "OS Command Injection", "HIGH"),
            (r"requests\.get.*verify\s*=\s*False", "Insecure HTTPS", "MEDIUM"),
            (r"SQL.*\+" or r"SQL.*f['\"]", "SQL Injection Risk", "HIGH"),
        ]
        
        for pattern, title, severity in issues:
            if re.search(pattern, content):
                self.findings.append({
                    "file": filepath,
                    "type": title,
                    "severity": severity,
                    "line": "Multiple"
                })

    def _scan_generic(self, content: str, filepath: str):
        """Análise genérica para todos os arquivos"""
        for vuln_type, details in vuln_db.common_vulns.items():
            for pattern in details["patterns"]:
                if re.search(pattern, content, re.IGNORECASE):
                    self.findings.append({
                        "file": filepath,
                        "type": vuln_type,
                        "severity": details["severity"],
                        "cve": details["cve"]
                    })

class DependencyAnalyzer:
    """Análise de dependências vulneráveis"""
    def __init__(self):
        self.vulnerable_packages = self._load_vuln_packages()

    def _load_vuln_packages(self) -> Dict:
        # Base de dados de pacotes vulneráveis conhecidos
        return {
            "django": {"2.0.0": "CVE-2019-XXXX", "1.11.0": "CVE-2021-XXXX"},
            "flask": {"0.10.0": "CVE-2018-XXXX", "1.0.0": "CVE-2019-XXXX"},
            "requests": {"2.20.0": "CVE-2018-XXXX"},
            "numpy": {"1.19.0": "CVE-2021-XXXX"},
            "pillow": {"7.0.0": "CVE-2020-XXXX"},
        }

    def check_requirements(self, requirements_file: str) -> List[Dict]:
        """Verifica dependências em requirements.txt"""
        vulnerabilities = []
        
        try:
            with open(requirements_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse package name and version
                    match = re.match(r'([a-zA-Z0-9\-_.]+)([><=!]*)(.*)', line)
                    if match:
                        pkg_name, op, version = match.groups()
                        
                        if pkg_name.lower() in self.vulnerable_packages:
                            vulns = self.vulnerable_packages[pkg_name.lower()]
                            if version in vulns:
                                vulnerabilities.append({
                                    "package": pkg_name,
                                    "version": version,
                                    "cve": vulns[version],
                                    "severity": "HIGH"
                                })
        except FileNotFoundError:
            log.error(f"Arquivo não encontrado: {requirements_file}")
        
        return vulnerabilities

class ConfigAnalyzer:
    """Análise de configurações inseguras"""
    def __init__(self):
        pass

    def analyze_config(self, config_file: str) -> List[Dict]:
        """Analisa arquivo de configuração"""
        issues = []
        
        try:
            with open(config_file, 'r') as f:
                content = f.read()
            
            # Verificar por secrets hardcoded
            if re.search(r'(password|secret|token|api[_-]?key)\s*[:=]\s*["\']?(?!<|{|\$|env)', content):
                issues.append({
                    "type": "Hardcoded Secrets",
                    "severity": "CRITICAL",
                    "file": config_file
                })
            
            # Verificar por debug habilitado
            if re.search(r'(debug|DEBUG)\s*[:=]\s*(true|True|1)', content):
                issues.append({
                    "type": "Debug Mode Enabled",
                    "severity": "MEDIUM",
                    "file": config_file
                })
            
            # Verificar por conexões inseguras
            if re.search(r'(http|mysql|mongodb)://(?!localhost|127\.0\.0\.1)', content):
                issues.append({
                    "type": "Insecure Remote Connection",
                    "severity": "HIGH",
                    "file": config_file
                })
        
        except Exception as e:
            log.error(f"Erro analisando config {config_file}: {e}")
        
        return issues

class NetworkAnalyzer:
    """Análise de segurança de rede"""
    def __init__(self):
        pass

    def scan_port(self, host: str, port: int, timeout: int = 3) -> bool:
        """Verifica se uma porta está aberta"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                return result == 0
        except:
            return False

    def scan_common_ports(self, host: str) -> Dict[int, bool]:
        """Escaneia portas comuns"""
        common_ports = {
            22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL",
            5432: "PostgreSQL", 6379: "Redis", 27017: "MongoDB",
            8080: "Alt-HTTP", 8443: "Alt-HTTPS"
        }
        
        results = {}
        log.scan(f"Iniciando port scan em {host}")
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(self.scan_port, host, port): port
                for port in common_ports.keys()
            }
            
            for future in as_completed(futures):
                port = futures[future]
                try:
                    results[port] = future.result()
                except Exception as e:
                    log.error(f"Erro scanando porta {port}: {e}")
        
        return results

    def check_ssl_cert(self, host: str, port: int = 443) -> Dict[str, Any]:
        """Verifica certificado SSL"""
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((host, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        "valid": True,
                        "subject": dict(x[0] for x in cert['subject']),
                        "issued": cert.get('notBefore'),
                        "expires": cert.get('notAfter')
                    }
        except Exception as e:
            return {"valid": False, "error": str(e)}

# ─────────────────────────────────────────────
#  GERADOR DE RELATÓRIOS
# ─────────────────────────────────────────────
class ReportGenerator:
    """Gera relatórios detalhados de segurança"""
    def __init__(self):
        self.timestamp = datetime.now()

    def generate_json_report(self, findings: List[Dict], target: str = "") -> str:
        """Gera relatório em JSON"""
        report = {
            "tool": "H.A.V. SENTINEL",
            "version": VERSION,
            "timestamp": self.timestamp.isoformat(),
            "target": target,
            "summary": self._generate_summary(findings),
            "findings": findings
        }
        
        filename = f"report_{self.timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(REPORT_DIR, filename)
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filepath

    def generate_html_report(self, findings: List[Dict], target: str = "") -> str:
        """Gera relatório em HTML"""
        summary = self._generate_summary(findings)
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>H.A.V. SENTINEL Report</title>
    <style>
        * {{ margin: 0; padding: 0; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #1a1a1a; color: #fff; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }}
        .stat {{ background: #2a2a2a; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea; }}
        .critical {{ border-left-color: #ff4444; }}
        .high {{ border-left-color: #ff8844; }}
        .medium {{ border-left-color: #ffaa44; }}
        .low {{ border-left-color: #44aaff; }}
        .stat-value {{ font-size: 28px; font-weight: bold; }}
        .stat-label {{ font-size: 12px; color: #aaa; margin-top: 5px; }}
        .finding {{ background: #2a2a2a; margin: 15px 0; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea; }}
        .finding.critical {{ border-left-color: #ff4444; }}
        .finding.high {{ border-left-color: #ff8844; }}
        .finding.medium {{ border-left-color: #ffaa44; }}
        .finding.low {{ border-left-color: #44aaff; }}
        .finding-title {{ font-weight: bold; font-size: 16px; }}
        .finding-cve {{ color: #aaa; font-size: 12px; }}
        .finding-desc {{ margin-top: 8px; color: #ccc; }}
        .remediation {{ background: #1a3a1a; padding: 10px; margin-top: 10px; border-radius: 4px; color: #44ff44; }}
        .timestamp {{ color: #aaa; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>H.A.V. SENTINEL v{VERSION}</h1>
        <p>Hyper Application Vulnerability Sentinel</p>
    </div>
    <div class="container">
        <p class="timestamp">Relatório gerado: {self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}</p>
        <h2>Target: {target}</h2>
        
        <h3 style="margin-top: 30px;">Resumo</h3>
        <div class="summary">
            <div class="stat critical">
                <div class="stat-value">{summary['critical']}</div>
                <div class="stat-label">Critical</div>
            </div>
            <div class="stat high">
                <div class="stat-value">{summary['high']}</div>
                <div class="stat-label">High</div>
            </div>
            <div class="stat medium">
                <div class="stat-value">{summary['medium']}</div>
                <div class="stat-label">Medium</div>
            </div>
            <div class="stat low">
                <div class="stat-value">{summary['low']}</div>
                <div class="stat-label">Low</div>
            </div>
        </div>
        
        <h3 style="margin-top: 30px;">Vulnerabilidades Encontradas</h3>
        {"".join(f'''
        <div class="finding {finding.get("severity", "").lower()}">
            <div class="finding-title">{finding.get("title", "N/A")}</div>
            <div class="finding-cve">{finding.get("cve", "N/A")}</div>
            <div class="finding-desc">{finding.get("description", "N/A")}</div>
            <div class="remediation"><strong>Remediação:</strong> {finding.get("remediation", "Consulte documentação")}</div>
        </div>
        ''' for finding in findings)}
    </div>
</body>
</html>
"""
        
        filename = f"report_{self.timestamp.strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(REPORT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath

    def _generate_summary(self, findings: List[Dict]) -> Dict[str, int]:
        summary = {
            "total": len(findings),
            "critical": sum(1 for f in findings if f.get("severity") == "CRITICAL"),
            "high": sum(1 for f in findings if f.get("severity") == "HIGH"),
            "medium": sum(1 for f in findings if f.get("severity") == "MEDIUM"),
            "low": sum(1 for f in findings if f.get("severity") == "LOW"),
        }
        return summary

# ─────────────────────────────────────────────
#  SCANNER COMPLETO
# ─────────────────────────────────────────────
class SentinelScanner:
    """Scanner completo de vulnerabilidades"""
    def __init__(self):
        self.static_analyzer = StaticCodeAnalyzer()
        self.dep_analyzer = DependencyAnalyzer()
        self.config_analyzer = ConfigAnalyzer()
        self.network_analyzer = NetworkAnalyzer()
        self.report_gen = ReportGenerator()
        self.all_findings = []

    def scan_directory(self, directory: str) -> List[Dict]:
        """Escaneia um diretório completo"""
        log.scan(f"Iniciando análise de {directory}")
        self.all_findings = []
        
        for root, dirs, files in os.walk(directory):
            # Ignorar diretórios comuns
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv', 'venv']]
            
            for file in files:
                filepath = os.path.join(root, file)
                
                # Análise estática
                if Path(file).suffix in ['.py', '.js', '.ts', '.java', '.go', '.rb', '.php']:
                    findings = self.static_analyzer.analyze_file(filepath)
                    self.all_findings.extend(findings)
                
                # Análise de configuração
                if file in ['config.yaml', 'config.json', '.env', 'settings.py']:
                    issues = self.config_analyzer.analyze_config(filepath)
                    self.all_findings.extend(issues)
                
                # Análise de dependências
                if file == 'requirements.txt':
                    vulns = self.dep_analyzer.check_requirements(filepath)
                    self.all_findings.extend(vulns)
        
        log.success(f"Análise concluída: {len(self.all_findings)} problemas encontrados")
        return self.all_findings

    def scan_application(self, app_path: str, app_type: str = "auto") -> Dict[str, Any]:
        """Escaneia uma aplicação completa"""
        results = {
            "target": app_path,
            "type": app_type,
            "start_time": datetime.now(),
            "static_findings": [],
            "dep_findings": [],
            "config_findings": [],
            "network_findings": [],
            "total_risk_score": 0
        }
        
        # Análise estática
        results["static_findings"] = self.scan_directory(app_path)
        
        # Análise de configuração
        for root, dirs, files in os.walk(app_path):
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__']]
            for file in ['config.yaml', 'config.json', '.env', 'settings.py']:
                if file in files:
                    results["config_findings"].extend(
                        self.config_analyzer.analyze_config(os.path.join(root, file))
                    )
        
        # Análise de dependências
        for root, dirs, files in os.walk(app_path):
            if 'requirements.txt' in files:
                results["dep_findings"].extend(
                    self.dep_analyzer.check_requirements(os.path.join(root, 'requirements.txt'))
                )
        
        results["end_time"] = datetime.now()
        results["duration"] = str(results["end_time"] - results["start_time"])
        
        return results

report_generator = ReportGenerator()
scanner = SentinelScanner()
