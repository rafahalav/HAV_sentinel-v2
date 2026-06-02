#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║       H.A.V. SENTINEL CLI — Command Line Interface                             ║
# ║              Hyper Application Vulnerability Sentinel - Terminal Version         ║
# ║                          Version 2.0 — Production Ready                         ║
# ╚══════════════════════════════════════════════════════════════════════════════════╝

"""
H.A.V. SENTINEL CLI
===================
Interface de linha de comando para análise de vulnerabilidades de aplicações
"""

import os, sys, json, time, argparse, textwrap
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import readline

# Importar core do sentinel
from hav_sentinel_core import (
    log, C, colorize, VERSION, CODENAME, REPORT_DIR,
    StaticCodeAnalyzer, DependencyAnalyzer, ConfigAnalyzer, NetworkAnalyzer,
    ReportGenerator, SentinelScanner, VulnerabilityDatabase,
    AI_MODEL, ANTHROPIC_OK
)

# ─────────────────────────────────────────────
#  BANNER E INTRODUÇÃO
# ─────────────────────────────────────────────
def show_banner():
    """Exibe o banner inicial"""
    banner = f"""
    {C.BCYAN}╔════════════════════════════════════════════════════════════════════════════════╗{C.RESET}
    {C.BCYAN}║{C.RESET}                                                                            {C.BCYAN}║{C.RESET}
    {C.BCYAN}║{C.RESET}  {C.BOLD}{C.BMAGENTA}H.A.V. SENTINEL{C.RESET} — Hyper Application Vulnerability Sentinel         {C.BCYAN}║{C.RESET}
    {C.BCYAN}║{C.RESET}                                                                            {C.BCYAN}║{C.RESET}
    {C.BCYAN}║{C.RESET}  {C.BOLD}Version {C.BGREEN}{VERSION}{C.RESET} | {C.BBLUE}{CODENAME}{C.RESET}                                  {C.BCYAN}║{C.RESET}
    {C.BCYAN}║{C.RESET}  Advanced Application Security Analysis Framework                        {C.BCYAN}║{C.RESET}
    {C.BCYAN}║{C.RESET}                                                                            {C.BCYAN}║{C.RESET}
    {C.BCYAN}║{C.RESET}  {C.DIM}Scan | Analyze | Report | Secure{C.RESET}                                     {C.BCYAN}║{C.RESET}
    {C.BCYAN}║{C.RESET}                                                                            {C.BCYAN}║{C.RESET}
    {C.BCYAN}╚════════════════════════════════════════════════════════════════════════════════╝{C.RESET}
    """
    print(banner)
    print()

# ─────────────────────────────────────────────
#  PROCESSADOR DE COMANDOS CLI
# ─────────────────────────────────────────────
class CLIProcessor:
    """Processador de comandos para interface CLI"""
    
    def __init__(self):
        self.running = True
        self.current_target = None
        self.scanner = SentinelScanner()
        self.last_scan_results = None
        self.vuln_db = VulnerabilityDatabase()
        self.commands = {
            'scan': self.cmd_scan,
            'analyze': self.cmd_analyze,
            'report': self.cmd_report,
            'vulndb': self.cmd_vulndb,
            'network': self.cmd_network,
            'help': self.cmd_help,
            'exit': self.cmd_exit,
            'clear': self.cmd_clear,
            'status': self.cmd_status,
            'config': self.cmd_config,
            'export': self.cmd_export,
        }

    def execute(self, command: str):
        """Executa um comando"""
        parts = command.strip().split(None, 1)
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd in self.commands:
            try:
                self.commands[cmd](args)
            except Exception as e:
                log.error(f"Erro executando comando: {e}")
        else:
            log.error(f"Comando desconhecido: {cmd}. Digite 'help' para ajuda")

    def cmd_scan(self, args: str):
        """Comando: scan - Escaneia um alvo"""
        print()
        print(f"{C.CYAN}{'─'*70}{C.RESET}")
        print(f"  {C.BOLD}SCAN DIRECTORY{C.RESET}")
        print(f"{C.CYAN}{'─'*70}{C.RESET}\n")
        
        if not args:
            print(f"{C.WARN}Uso: scan <caminho>{C.RESET}\n")
            print(f"  Exemplos:")
            print(f"    scan /caminho/para/aplicacao")
            print(f"    scan ./projeto")
            print()
            return
        
        target_path = args.strip()
        
        if not os.path.exists(target_path):
            log.error(f"Caminho não existe: {target_path}")
            return
        
        self.current_target = target_path
        log.scan(f"Iniciando scan em: {target_path}")
        
        # Análise completa
        results = self.scanner.scan_application(target_path)
        self.last_scan_results = results
        
        # Exibir resultados
        self._display_scan_results(results)
        
        log.success(f"Scan concluído em {results['duration']}")
        print()

    def cmd_analyze(self, args: str):
        """Comando: analyze - Analisa um arquivo específico"""
        print()
        print(f"{C.CYAN}{'─'*70}{C.RESET}")
        print(f"  {C.BOLD}ANALYZE FILE{C.RESET}")
        print(f"{C.CYAN}{'─'*70}{C.RESET}\n")
        
        if not args:
            print(f"{C.WARN}Uso: analyze <arquivo>{C.RESET}\n")
            return
        
        filepath = args.strip()
        
        if not os.path.exists(filepath):
            log.error(f"Arquivo não encontrado: {filepath}")
            return
        
        log.info(f"Analisando: {filepath}")
        
        analyzer = StaticCodeAnalyzer()
        findings = analyzer.analyze_file(filepath)
        
        if findings:
            print(f"\n  {C.BOLD}Vulnerabilidades encontradas:{C.RESET}\n")
            for i, finding in enumerate(findings, 1):
                severity_color = self._get_severity_color(finding.get("severity"))
                print(f"  {C.DIM}{i}.{C.RESET} {severity_color}[{finding.get('severity')}]{C.RESET} {finding.get('type')}")
                print(f"     {C.DIM}Arquivo: {finding.get('file')}{C.RESET}")
                if finding.get('cve'):
                    print(f"     {C.DIM}CVE: {finding.get('cve')}{C.RESET}")
                print()
        else:
            log.success("Nenhuma vulnerabilidade encontrada")
        
        print()

    def cmd_report(self, args: str):
        """Comando: report - Gera relatórios"""
        print()
        print(f"{C.CYAN}{'─'*70}{C.RESET}")
        print(f"  {C.BOLD}REPORT GENERATOR{C.RESET}")
        print(f"{C.CYAN}{'─'*70}{C.RESET}\n")
        
        if not self.last_scan_results:
            log.error("Nenhum scan foi executado. Execute 'scan' primeiro.")
            print()
            return
        
        # Consolidar todos os findings
        all_findings = (
            self.last_scan_results.get('static_findings', []) +
            self.last_scan_results.get('dep_findings', []) +
            self.last_scan_results.get('config_findings', [])
        )
        
        report_gen = ReportGenerator()
        
        # Gerar relatórios
        if 'json' in args.lower() or not args:
            json_report = report_gen.generate_json_report(all_findings, self.current_target)
            log.success(f"Relatório JSON gerado: {json_report}")
        
        if 'html' in args.lower() or not args:
            html_report = report_gen.generate_html_report(all_findings, self.current_target)
            log.success(f"Relatório HTML gerado: {html_report}")
        
        print()

    def cmd_vulndb(self, args: str):
        """Comando: vulndb - Gerencia banco de dados de vulnerabilidades"""
        print()
        print(f"{C.CYAN}{'─'*70}{C.RESET}")
        print(f"  {C.BOLD}VULNERABILITY DATABASE{C.RESET}")
        print(f"{C.CYAN}{'─'*70}{C.RESET}\n")
        
        if 'list' in args.lower():
            print(f"  {C.BOLD}Vulnerabilidades conhecidas:{C.RESET}\n")
            for vuln_type, details in self.vuln_db.common_vulns.items():
                print(f"  {C.BRED}●{C.RESET} {vuln_type}")
                print(f"    {C.DIM}CVE: {details['cve']}{C.RESET}")
                print(f"    {C.DIM}Severidade: {details['severity']}{C.RESET}")
                print(f"    {C.DIM}Remediação: {details['remediation']}{C.RESET}")
                print()
        
        elif 'search' in args.lower():
            search_term = args.replace('search', '').strip()
            if not search_term:
                log.error("Forneça um termo de busca")
                print()
                return
            
            print(f"  Buscando: {search_term}\n")
            for vuln_type in self.vuln_db.common_vulns:
                if search_term.lower() in vuln_type.lower():
                    details = self.vuln_db.common_vulns[vuln_type]
                    print(f"  {C.BRED}●{C.RESET} {vuln_type}")
                    print(f"    {C.DIM}CVE: {details['cve']}{C.RESET}")
                    print(f"    {C.DIM}Severidade: {details['severity']}{C.RESET}")
                    print()
        
        else:
            print(f"  Opções disponíveis:\n")
            print(f"    {C.BCYAN}vulndb list{C.RESET}          - Lista todas as vulnerabilidades conhecidas")
            print(f"    {C.BCYAN}vulndb search <termo>{C.RESET}  - Busca por vulnerabilidade")
            print()

    def cmd_network(self, args: str):
        """Comando: network - Testes de rede"""
        print()
        print(f"{C.CYAN}{'─'*70}{C.RESET}")
        print(f"  {C.BOLD}NETWORK SECURITY{C.RESET}")
        print(f"{C.CYAN}{'─'*70}{C.RESET}\n")
        
        if 'portscan' in args.lower():
            parts = args.split()
            if len(parts) < 2:
                log.error("Uso: network portscan <host>")
                print()
                return
            
            host = parts[1]
            log.info(f"Escaneando portas em {host}")
            
            net_analyzer = NetworkAnalyzer()
            results = net_analyzer.scan_common_ports(host)
            
            print(f"\n  {C.BOLD}Resultado do Port Scan:{C.RESET}\n")
            open_ports = [p for p, is_open in results.items() if is_open]
            
            if open_ports:
                for port in sorted(open_ports):
                    print(f"  {C.SUCCESS}✓{C.RESET} Porta {port} - ABERTA")
            else:
                log.info("Nenhuma porta aberta encontrada")
            
            print()
        
        elif 'ssl' in args.lower():
            parts = args.split()
            if len(parts) < 2:
                log.error("Uso: network ssl <host> [porta]")
                print()
                return
            
            host = parts[1]
            port = int(parts[2]) if len(parts) > 2 else 443
            
            net_analyzer = NetworkAnalyzer()
            cert_info = net_analyzer.check_ssl_cert(host, port)
            
            print(f"\n  {C.BOLD}Certificado SSL/TLS:{C.RESET}\n")
            if cert_info['valid']:
                print(f"  Status: {C.SUCCESS}Válido{C.RESET}")
                print(f"  Subject: {cert_info['subject']}")
                print(f"  Válido até: {cert_info['expires']}")
            else:
                print(f"  Status: {C.FAIL}Inválido{C.RESET}")
                print(f"  Erro: {cert_info['error']}")
            
            print()
        
        else:
            print(f"  Opções disponíveis:\n")
            print(f"    {C.BCYAN}network portscan <host>{C.RESET}    - Escaneia portas comuns")
            print(f"    {C.BCYAN}network ssl <host> [porta]{C.RESET}  - Verifica certificado SSL")
            print()

    def cmd_help(self, args: str):
        """Comando: help - Mostra ajuda"""
        print()
        print(f"{C.CYAN}{'─'*70}{C.RESET}")
        print(f"  {C.BOLD}COMANDOS DISPONÍVEIS{C.RESET}")
        print(f"{C.CYAN}{'─'*70}{C.RESET}\n")
        
        commands_help = {
            'scan <caminho>': 'Escaneia um diretório ou arquivo',
            'analyze <arquivo>': 'Analisa um arquivo específico',
            'report [json|html]': 'Gera relatório do último scan',
            'vulndb [list|search]': 'Gerencia banco de vulnerabilidades',
            'network [portscan|ssl]': 'Testes de segurança de rede',
            'status': 'Mostra status atual',
            'export <formato>': 'Exporta resultados',
            'config': 'Mostra configurações',
            'clear': 'Limpa a tela',
            'help': 'Mostra esta mensagem',
            'exit': 'Sai do programa',
        }
        
        for cmd, desc in commands_help.items():
            print(f"  {C.BCYAN}{cmd:30s}{C.RESET} {desc}")
        
        print()

    def cmd_status(self, args: str):
        """Comando: status - Mostra status"""
        print()
        print(f"{C.CYAN}{'─'*70}{C.RESET}")
        print(f"  {C.BOLD}STATUS{C.RESET}")
        print(f"{C.CYAN}{'─'*70}{C.RESET}\n")
        
        print(f"  Versão: {C.BGREEN}{VERSION}{C.RESET}")
        print(f"  Build: {C.DIM}{CODENAME}{C.RESET}")
        print(f"  Target Atual: {C.BCYAN}{self.current_target or 'Nenhum'}{C.RESET}")
        print(f"  Scans Executados: {C.BYELLOW}{log.metrics['scans']}{C.RESET}")
        print(f"  Vulnerabilidades Encontradas: {C.BRED}{log.metrics['vulns_found']}{C.RESET}")
        print(f"  Críticas/Altas: {C.CRITICAL}{log.metrics['high_risk']}{C.RESET}")
        print(f"  Diretório de Relatórios: {C.DIM}{REPORT_DIR}{C.RESET}")
        print()

    def cmd_config(self, args: str):
        """Comando: config - Mostra configurações"""
        print()
        print(f"{C.CYAN}{'─'*70}{C.RESET}")
        print(f"  {C.BOLD}CONFIGURAÇÕES{C.RESET}")
        print(f"{C.CYAN}{'─'*70}{C.RESET}\n")
        
        print(f"  Modelo IA: {C.BBLUE}{AI_MODEL}{C.RESET}")
        print(f"  Anthropic OK: {C.BGREEN if ANTHROPIC_OK else C.BRED}{'Sim' if ANTHROPIC_OK else 'Não'}{C.RESET}")
        print(f"  Diretório de Logs: {C.DIM}{log.log_file}{C.RESET}")
        print(f"  Diretório de Workspace: {C.DIM}{REPORT_DIR}{C.RESET}")
        print()

    def cmd_clear(self, args: str):
        """Comando: clear - Limpa tela"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def cmd_export(self, args: str):
        """Comando: export - Exporta resultados"""
        print()
        if not self.last_scan_results:
            log.error("Nenhum scan foi executado")
            print()
            return
        
        format_type = args.strip().lower() if args else 'json'
        
        all_findings = (
            self.last_scan_results.get('static_findings', []) +
            self.last_scan_results.get('dep_findings', []) +
            self.last_scan_results.get('config_findings', [])
        )
        
        if format_type == 'json':
            report_gen = ReportGenerator()
            filepath = report_gen.generate_json_report(all_findings, self.current_target)
            log.success(f"Exportado para: {filepath}")
        elif format_type == 'html':
            report_gen = ReportGenerator()
            filepath = report_gen.generate_html_report(all_findings, self.current_target)
            log.success(f"Exportado para: {filepath}")
        else:
            log.error(f"Formato não suportado: {format_type}")
        
        print()

    def cmd_exit(self, args: str):
        """Comando: exit - Sai do programa"""
        print()
        print(f"{C.CYAN}{'─'*70}{C.RESET}")
        print(f"  {C.BOLD}Encerrando H.A.V. SENTINEL{C.RESET}")
        print(f"  Scans: {log.metrics['scans']} | Vulnerabilidades: {log.metrics['vulns_found']}")
        print(f"{C.CYAN}{'─'*70}{C.RESET}\n")
        self.running = False

    def _display_scan_results(self, results: Dict):
        """Exibe resultados do scan"""
        all_findings = (
            results.get('static_findings', []) +
            results.get('dep_findings', []) +
            results.get('config_findings', [])
        )
        
        print(f"\n  {C.BOLD}Resultados do Scan:{C.RESET}\n")
        
        # Contar por severidade
        severity_counts = {
            'CRITICAL': sum(1 for f in all_findings if f.get('severity') == 'CRITICAL'),
            'HIGH': sum(1 for f in all_findings if f.get('severity') == 'HIGH'),
            'MEDIUM': sum(1 for f in all_findings if f.get('severity') == 'MEDIUM'),
            'LOW': sum(1 for f in all_findings if f.get('severity') == 'LOW'),
        }
        
        # Exibir estatísticas
        print(f"  {C.FAIL}[CRITICAL]{C.RESET} {severity_counts['CRITICAL']:3d}")
        print(f"  {C.BRED}[HIGH]{C.RESET}     {severity_counts['HIGH']:3d}")
        print(f"  {C.WARN}[MEDIUM]{C.RESET}   {severity_counts['MEDIUM']:3d}")
        print(f"  {C.BBLUE}[LOW]{C.RESET}      {severity_counts['LOW']:3d}")
        print(f"  {C.DIM}────────────{C.RESET}")
        print(f"  {C.BCYAN}Total{C.RESET}      {len(all_findings):3d}\n")
        
        # Exibir alguns findings
        if all_findings:
            print(f"  {C.BOLD}Top Vulnerabilidades:{C.RESET}\n")
            for i, finding in enumerate(all_findings[:10], 1):
                severity_color = self._get_severity_color(finding.get("severity"))
                print(f"  {C.DIM}{i}.{C.RESET} {severity_color}[{finding.get('severity')}]{C.RESET} {finding.get('type', finding.get('title', 'Unknown'))}")

    def _get_severity_color(self, severity: str) -> str:
        """Retorna cor baseada em severidade"""
        colors = {
            'CRITICAL': C.FAIL,
            'HIGH': C.BRED,
            'MEDIUM': C.WARN,
            'LOW': C.BBLUE,
            'INFO': C.BCYAN
        }
        return colors.get(severity, C.WHITE)

# ─────────────────────────────────────────────
#  MAIN LOOP CLI
# ─────────────────────────────────────────────
def get_prompt() -> str:
    """Retorna o prompt"""
    return f"{C.PROMPT}sentinel{C.RESET} {C.DIM}${C.RESET} "

def main_cli():
    """Main loop da CLI"""
    show_banner()
    
    parser = argparse.ArgumentParser(description="H.A.V. SENTINEL CLI")
    parser.add_argument("-t", "--target", help="Alvo inicial")
    parser.add_argument("-c", "--cmd", help="Executar comando e sair")
    parser.add_argument("--no-banner", action="store_true", help="Sem banner")
    # parse_known_args ignora flags do launcher (--cli, --gui, --target)
    args, _ = parser.parse_known_args()
    
    cli = CLIProcessor()
    
    if args.target:
        cli.current_target = args.target
        cli.cmd_scan(args.target)
    
    if args.cmd:
        cli.execute(args.cmd)
        return
    
    log.info(f"Digite 'help' para ver comandos disponíveis")
    print()
    
    try:
        while cli.running:
            try:
                prompt = get_prompt()
                line = input(prompt).strip()
                
                if not line:
                    continue
                
                cli.execute(line)
            
            except KeyboardInterrupt:
                print(f"\n{C.WARN}[!] Use 'exit' para sair{C.RESET}\n")
                continue
            except EOFError:
                cli.cmd_exit([])
                break
            except Exception as e:
                log.error(f"Erro: {e}")
    
    except KeyboardInterrupt:
        print()
        cli.cmd_exit([])

if __name__ == "__main__":
    main_cli()
