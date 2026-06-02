#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║       H.A.V. SENTINEL GUI — Graphical User Interface                           ║
# ║              Hyper Application Vulnerability Sentinel - GUI Version              ║
# ║                          Version 2.0 — Production Ready                         ║
# ╚══════════════════════════════════════════════════════════════════════════════════╝

"""
H.A.V. SENTINEL GUI
===================
Interface gráfica moderna para análise de vulnerabilidades
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os, json, subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Importar core do sentinel
from hav_sentinel_core import (
    log, C, VERSION, CODENAME, REPORT_DIR,
    StaticCodeAnalyzer, DependencyAnalyzer, ConfigAnalyzer, NetworkAnalyzer,
    ReportGenerator, SentinelScanner, VulnerabilityDatabase,
    WORKSPACE_DIR, LOG_DIR
)

# ─────────────────────────────────────────────
#  APLICAÇÃO GUI PRINCIPAL
# ─────────────────────────────────────────────
class HAVSentinelGUI:
    """Aplicação GUI principal do H.A.V. SENTINEL"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"H.A.V. SENTINEL v{VERSION} - GUI")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1a1a1a")
        
        # Configurar estilo
        self._setup_styles()
        
        # Inicializar componentes
        self.scanner = SentinelScanner()
        self.vuln_db = VulnerabilityDatabase()
        self.report_gen = ReportGenerator()
        self.last_scan_results = None
        self.scan_thread = None
        self.is_scanning = False
        
        # Criar UI
        self._create_ui()
        
        # Atualizar status
        self.update_status("Pronto para análise")

    def _setup_styles(self):
        """Configura estilos tkinter"""
        style = ttk.Style()
        
        # Tema dark
        style.theme_use('clam')
        
        # Cores
        bg_dark = "#1a1a1a"
        bg_medium = "#2a2a2a"
        bg_light = "#3a3a3a"
        text_color = "#ffffff"
        accent_color = "#667eea"
        
        style.configure('TFrame', background=bg_dark)
        style.configure('TLabel', background=bg_dark, foreground=text_color)
        style.configure('TButton', background=bg_medium, foreground=text_color)
        style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), foreground=accent_color)
        style.configure('Treeview', background=bg_medium, foreground=text_color, fieldbackground=bg_medium)
        style.configure('Treeview.Heading', background=accent_color, foreground=text_color)

    def _create_ui(self):
        """Cria a interface do usuário"""
        # Menu principal
        self._create_menu()
        
        # Container principal
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self._create_header(main_container)
        
        # Conteúdo principal (Notebook com abas)
        self._create_notebook(main_container)
        
        # Rodapé
        self._create_footer(main_container)

    def _create_menu(self):
        """Cria barra de menu"""
        menubar = tk.Menu(self.root, bg="#2a2a2a", fg="#ffffff")
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0, bg="#2a2a2a", fg="#ffffff")
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Novo Scan", command=self.new_scan)
        file_menu.add_command(label="Abrir Relatório", command=self.open_report)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        
        # Menu Ferramentas
        tools_menu = tk.Menu(menubar, tearoff=0, bg="#2a2a2a", fg="#ffffff")
        menubar.add_cascade(label="Ferramentas", menu=tools_menu)
        tools_menu.add_command(label="Gerenciar Banco de Dados", command=self.show_vulndb)
        tools_menu.add_command(label="Limpador de Cache", command=self.clear_cache)
        tools_menu.add_command(label="Abrir Logs", command=self.open_logs)
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0, bg="#2a2a2a", fg="#ffffff")
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=self.show_about)
        help_menu.add_command(label="Documentação", command=self.show_help)

    def _create_header(self, parent):
        """Cria cabeçalho"""
        header = ttk.Frame(parent)
        header.pack(fill=tk.X, pady=(0, 10))
        
        # Título
        title = ttk.Label(header, text="H.A.V. SENTINEL - Hyper Application Vulnerability Sentinel", 
                         style='Header.TLabel')
        title.pack(side=tk.LEFT)
        
        # Info
        info = ttk.Label(header, text=f"v{VERSION} | {CODENAME}")
        info.pack(side=tk.RIGHT)

    def _create_notebook(self, parent):
        """Cria abas principais"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Aba: Scan
        self.scan_tab = ttk.Frame(notebook)
        notebook.add(self.scan_tab, text="🔍 Scan de Segurança")
        self._create_scan_tab()
        
        # Aba: Resultados
        self.results_tab = ttk.Frame(notebook)
        notebook.add(self.results_tab, text="📊 Resultados")
        self._create_results_tab()
        
        # Aba: Relatórios
        self.reports_tab = ttk.Frame(notebook)
        notebook.add(self.reports_tab, text="📄 Relatórios")
        self._create_reports_tab()
        
        # Aba: Banco de Dados
        self.vulndb_tab = ttk.Frame(notebook)
        notebook.add(self.vulndb_tab, text="🗄️ Banco de Vulnerabilidades")
        self._create_vulndb_tab()
        
        # Aba: Rede
        self.network_tab = ttk.Frame(notebook)
        notebook.add(self.network_tab, text="🌐 Testes de Rede")
        self._create_network_tab()

    def _create_scan_tab(self):
        """Aba: Scan de Segurança"""
        frame = ttk.Frame(self.scan_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Seção de seleção
        select_frame = ttk.LabelFrame(frame, text="Seleção de Alvo", padding=10)
        select_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(select_frame, text="Caminho para análise:").pack(side=tk.LEFT)
        
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(select_frame, textvariable=self.path_var, width=50)
        self.path_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(select_frame, text="Procurar", command=self.browse_path).pack(side=tk.LEFT, padx=2)
        
        # Seção de tipo de scan
        type_frame = ttk.LabelFrame(frame, text="Tipo de Scan", padding=10)
        type_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.scan_options = {
            'static': tk.BooleanVar(value=True),
            'dependencies': tk.BooleanVar(value=True),
            'config': tk.BooleanVar(value=True),
            'network': tk.BooleanVar(value=False)
        }
        
        ttk.Checkbutton(type_frame, text="Análise Estática de Código", 
                       variable=self.scan_options['static']).pack(anchor=tk.W)
        ttk.Checkbutton(type_frame, text="Análise de Dependências", 
                       variable=self.scan_options['dependencies']).pack(anchor=tk.W)
        ttk.Checkbutton(type_frame, text="Análise de Configuração", 
                       variable=self.scan_options['config']).pack(anchor=tk.W)
        ttk.Checkbutton(type_frame, text="Testes de Rede", 
                       variable=self.scan_options['network']).pack(anchor=tk.W)
        
        # Seção de controles
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.scan_button = ttk.Button(control_frame, text="▶ Iniciar Scan", command=self.start_scan)
        self.scan_button.pack(side=tk.LEFT, padx=2)
        
        self.stop_button = ttk.Button(control_frame, text="⏹ Parar", command=self.stop_scan, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=2)
        
        # Seção de progresso
        progress_frame = ttk.LabelFrame(frame, text="Progresso", padding=10)
        progress_frame.pack(fill=tk.BOTH, expand=True)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        self.status_text = scrolledtext.ScrolledText(progress_frame, height=10, width=80, 
                                                    bg="#2a2a2a", fg="#ffffff")
        self.status_text.pack(fill=tk.BOTH, expand=True)

    def _create_results_tab(self):
        """Aba: Resultados"""
        frame = ttk.Frame(self.results_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Resumo
        summary_frame = ttk.LabelFrame(frame, text="Resumo", padding=10)
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Grid de estatísticas
        stats_grid = ttk.Frame(summary_frame)
        stats_grid.pack(fill=tk.X)
        
        self.stat_labels = {}
        for i, (severity, color) in enumerate([
            ("CRITICAL", "#ff4444"),
            ("HIGH", "#ff8844"),
            ("MEDIUM", "#ffaa44"),
            ("LOW", "#44aaff")
        ]):
            label = ttk.Label(stats_grid, text=f"{severity}: 0", foreground=color)
            label.pack(side=tk.LEFT, padx=20)
            self.stat_labels[severity] = label
        
        # Tabela de vulnerabilidades
        table_frame = ttk.LabelFrame(frame, text="Vulnerabilidades Encontradas", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        columns = ('ID', 'Severidade', 'Tipo', 'Alvo', 'CVE')
        self.results_tree = ttk.Treeview(table_frame, columns=columns, height=15, show='headings')
        
        # Definir colunas
        self.results_tree.column('ID', width=30)
        self.results_tree.column('Severidade', width=100)
        self.results_tree.column('Tipo', width=200)
        self.results_tree.column('Alvo', width=300)
        self.results_tree.column('CVE', width=100)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscroll=scrollbar.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind para seleção
        self.results_tree.bind('<<TreeviewSelect>>', self.on_result_select)

    def _create_reports_tab(self):
        """Aba: Relatórios"""
        frame = ttk.Frame(self.reports_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Seção de geração
        gen_frame = ttk.LabelFrame(frame, text="Gerar Relatórios", padding=10)
        gen_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(gen_frame, text="📄 Gerar JSON", command=self.generate_json_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(gen_frame, text="🌐 Gerar HTML", command=self.generate_html_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(gen_frame, text="📊 Gerar CSV", command=self.generate_csv_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(gen_frame, text="📂 Abrir Pasta", command=self.open_report_dir).pack(side=tk.LEFT, padx=5)
        
        # Lista de relatórios
        list_frame = ttk.LabelFrame(frame, text="Relatórios Recentes", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.reports_tree = ttk.Treeview(list_frame, columns=('Nome', 'Data', 'Tamanho'), 
                                        height=15, show='headings')
        self.reports_tree.column('Nome', width=400)
        self.reports_tree.column('Data', width=150)
        self.reports_tree.column('Tamanho', width=100)
        
        for col in ['Nome', 'Data', 'Tamanho']:
            self.reports_tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.reports_tree.yview)
        self.reports_tree.configure(yscroll=scrollbar.set)
        
        self.reports_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.refresh_reports_list()

    def _create_vulndb_tab(self):
        """Aba: Banco de Vulnerabilidades"""
        frame = ttk.Frame(self.vulndb_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Busca
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(search_frame, text="Buscar", command=self.search_vulndb).pack(side=tk.LEFT)
        
        # Tabela
        self.vulndb_tree = ttk.Treeview(frame, columns=('Tipo', 'Severidade', 'CVE', 'Remediação'), 
                                       height=20, show='headings')
        
        self.vulndb_tree.column('Tipo', width=200)
        self.vulndb_tree.column('Severidade', width=100)
        self.vulndb_tree.column('CVE', width=150)
        self.vulndb_tree.column('Remediação', width=400)
        
        for col in ['Tipo', 'Severidade', 'CVE', 'Remediação']:
            self.vulndb_tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.vulndb_tree.yview)
        self.vulndb_tree.configure(yscroll=scrollbar.set)
        
        self.vulndb_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.refresh_vulndb()

    def _create_network_tab(self):
        """Aba: Testes de Rede"""
        frame = ttk.Frame(self.network_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Controles
        control_frame = ttk.LabelFrame(frame, text="Configuração", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(control_frame, text="Host/IP:").pack(side=tk.LEFT)
        self.network_host_var = tk.StringVar()
        ttk.Entry(control_frame, textvariable=self.network_host_var, width=30).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="🔍 Port Scan", command=self.port_scan).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="🔐 SSL Check", command=self.ssl_check).pack(side=tk.LEFT, padx=2)
        
        # Resultados
        result_frame = ttk.LabelFrame(frame, text="Resultados", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.network_text = scrolledtext.ScrolledText(result_frame, height=20, width=80,
                                                     bg="#2a2a2a", fg="#ffffff")
        self.network_text.pack(fill=tk.BOTH, expand=True)

    def _create_footer(self, parent):
        """Cria rodapé"""
        footer = ttk.Frame(parent, relief="flat", borderwidth=1)
        footer.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(footer, text="Pronto")
        self.status_label.pack(side=tk.LEFT)
        
        self.progress_label = ttk.Label(footer, text="")
        self.progress_label.pack(side=tk.RIGHT)

    # ─────────────────────────────────────────
    #  MÉTODOS DE INTERAÇÃO
    # ─────────────────────────────────────────
    
    def browse_path(self):
        """Abre diálogo de seleção de pasta"""
        path = filedialog.askdirectory(title="Selecione o diretório para análise")
        if path:
            self.path_var.set(path)

    def start_scan(self):
        """Inicia o scan"""
        path = self.path_var.get()
        if not path:
            messagebox.showerror("Erro", "Selecione um caminho")
            return
        
        if not os.path.exists(path):
            messagebox.showerror("Erro", "Caminho não existe")
            return
        
        self.is_scanning = True
        self.scan_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        
        # Executar em thread separada
        self.scan_thread = threading.Thread(target=self._perform_scan, args=(path,), daemon=True)
        self.scan_thread.start()

    def _perform_scan(self, path: str):
        """Realiza o scan em thread separada"""
        try:
            self.update_progress_text(f"Iniciando scan em: {path}\n")
            
            results = self.scanner.scan_application(path)
            self.last_scan_results = results
            
            self.update_progress_text(f"\n✓ Scan concluído em {results['duration']}\n")
            
            # Atualizar resultados
            self.root.after(0, self._display_results, results)
            
        except Exception as e:
            self.update_progress_text(f"\n✗ Erro: {str(e)}\n")
        
        finally:
            self.is_scanning = False
            self.root.after(0, lambda: self.scan_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))

    def stop_scan(self):
        """Para o scan"""
        self.is_scanning = False
        self.update_progress_text("\n⏹ Scan cancelado\n")

    def _display_results(self, results: Dict):
        """Exibe resultados do scan"""
        all_findings = (
            results.get('static_findings', []) +
            results.get('dep_findings', []) +
            results.get('config_findings', [])
        )
        
        # Limpar tabela
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Adicionar resultados
        for i, finding in enumerate(all_findings, 1):
            severity = finding.get('severity', 'LOW')
            self.results_tree.insert('', 'end', values=(
                i,
                severity,
                finding.get('type', finding.get('title', 'N/A')),
                finding.get('target', finding.get('file', 'N/A')),
                finding.get('cve', 'N/A')
            ))
        
        # Atualizar estatísticas
        severities = {}
        for finding in all_findings:
            sev = finding.get('severity', 'LOW')
            severities[sev] = severities.get(sev, 0) + 1
        
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            count = severities.get(severity, 0)
            self.stat_labels[severity].config(text=f"{severity}: {count}")

    def on_result_select(self, event):
        """Quando um resultado é selecionado"""
        selected = self.results_tree.selection()
        if selected:
            item = selected[0]
            values = self.results_tree.item(item)['values']
            # Poderia exibir detalhes aqui

    def update_progress_text(self, text: str):
        """Atualiza texto de progresso"""
        self.root.after(0, lambda: self.status_text.insert(tk.END, text))
        self.root.after(0, lambda: self.status_text.see(tk.END))

    def update_status(self, status: str):
        """Atualiza status"""
        self.root.after(0, lambda: self.status_label.config(text=status))

    def generate_json_report(self):
        """Gera relatório JSON"""
        if not self.last_scan_results:
            messagebox.showerror("Erro", "Execute um scan primeiro")
            return
        
        all_findings = (
            self.last_scan_results.get('static_findings', []) +
            self.last_scan_results.get('dep_findings', []) +
            self.last_scan_results.get('config_findings', [])
        )
        
        filepath = self.report_gen.generate_json_report(all_findings, self.path_var.get())
        messagebox.showinfo("Sucesso", f"Relatório gerado:\n{filepath}")
        self.refresh_reports_list()

    def generate_html_report(self):
        """Gera relatório HTML"""
        if not self.last_scan_results:
            messagebox.showerror("Erro", "Execute um scan primeiro")
            return
        
        all_findings = (
            self.last_scan_results.get('static_findings', []) +
            self.last_scan_results.get('dep_findings', []) +
            self.last_scan_results.get('config_findings', [])
        )
        
        filepath = self.report_gen.generate_html_report(all_findings, self.path_var.get())
        messagebox.showinfo("Sucesso", f"Relatório gerado:\n{filepath}")
        self.refresh_reports_list()

    def generate_csv_report(self):
        """Gera relatório CSV"""
        messagebox.showinfo("Info", "Função em desenvolvimento")

    def open_report_dir(self):
        """Abre pasta de relatórios"""
        if os.path.exists(REPORT_DIR):
            subprocess.Popen(['open' if os.name == 'posix' else 'explorer', REPORT_DIR])
        else:
            messagebox.showerror("Erro", "Pasta de relatórios não existe")

    def refresh_reports_list(self):
        """Atualiza lista de relatórios"""
        for item in self.reports_tree.get_children():
            self.reports_tree.delete(item)
        
        if os.path.exists(REPORT_DIR):
            for file in sorted(os.listdir(REPORT_DIR), reverse=True)[:10]:
                filepath = os.path.join(REPORT_DIR, file)
                size = os.path.getsize(filepath)
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M')
                self.reports_tree.insert('', 'end', values=(file, mtime, f"{size} B"))

    def refresh_vulndb(self):
        """Atualiza banco de vulnerabilidades"""
        for item in self.vulndb_tree.get_children():
            self.vulndb_tree.delete(item)
        
        for vuln_type, details in self.vuln_db.common_vulns.items():
            self.vulndb_tree.insert('', 'end', values=(
                vuln_type,
                details['severity'],
                details['cve'],
                details['remediation']
            ))

    def search_vulndb(self):
        """Busca no banco de vulnerabilidades"""
        search_term = self.search_var.get().lower()
        
        for item in self.vulndb_tree.get_children():
            self.vulndb_tree.delete(item)
        
        for vuln_type, details in self.vuln_db.common_vulns.items():
            if search_term in vuln_type.lower() or search_term in details['remediation'].lower():
                self.vulndb_tree.insert('', 'end', values=(
                    vuln_type,
                    details['severity'],
                    details['cve'],
                    details['remediation']
                ))

    def port_scan(self):
        """Realiza port scan"""
        host = self.network_host_var.get()
        if not host:
            messagebox.showerror("Erro", "Digite um host/IP")
            return
        
        self.network_text.delete(1.0, tk.END)
        self.network_text.insert(tk.END, f"Escaneando {host}...\n\n")
        
        def perform_scan():
            net_analyzer = NetworkAnalyzer()
            results = net_analyzer.scan_common_ports(host)
            
            text = "Resultado do Port Scan:\n"
            text += "=" * 40 + "\n"
            
            for port, is_open in sorted(results.items()):
                status = "ABERTA" if is_open else "FECHADA"
                text += f"Porta {port}: {status}\n"
            
            self.root.after(0, lambda: self.network_text.insert(tk.END, text))
        
        thread = threading.Thread(target=perform_scan, daemon=True)
        thread.start()

    def ssl_check(self):
        """Verifica SSL"""
        host = self.network_host_var.get()
        if not host:
            messagebox.showerror("Erro", "Digite um host")
            return
        
        self.network_text.delete(1.0, tk.END)
        self.network_text.insert(tk.END, f"Verificando SSL para {host}...\n\n")
        
        def check_ssl():
            net_analyzer = NetworkAnalyzer()
            cert_info = net_analyzer.check_ssl_cert(host)
            
            text = "Certificado SSL/TLS:\n"
            text += "=" * 40 + "\n"
            
            if cert_info['valid']:
                text += "Status: Válido\n"
                text += f"Subject: {cert_info.get('subject', 'N/A')}\n"
                text += f"Válido até: {cert_info.get('expires', 'N/A')}\n"
            else:
                text += "Status: Inválido\n"
                text += f"Erro: {cert_info.get('error', 'Desconhecido')}\n"
            
            self.root.after(0, lambda: self.network_text.insert(tk.END, text))
        
        thread = threading.Thread(target=check_ssl, daemon=True)
        thread.start()

    def show_vulndb(self):
        """Mostra gerenciador de banco de dados"""
        messagebox.showinfo("Info", "Veja a aba 'Banco de Vulnerabilidades'")

    def clear_cache(self):
        """Limpa cache"""
        from hav_sentinel_core import CACHE_DIR
        try:
            for file in os.listdir(CACHE_DIR):
                os.remove(os.path.join(CACHE_DIR, file))
            messagebox.showinfo("Sucesso", "Cache limpo")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao limpar cache: {e}")

    def open_logs(self):
        """Abre pasta de logs"""
        if os.path.exists(LOG_DIR):
            subprocess.Popen(['open' if os.name == 'posix' else 'explorer', LOG_DIR])

    def open_report(self):
        """Abre um relatório"""
        file = filedialog.askopenfilename(initialdir=REPORT_DIR, 
                                         filetypes=[("HTML", "*.html"), ("JSON", "*.json")])
        if file and os.path.exists(file):
            if file.endswith('.html'):
                subprocess.Popen(['open' if os.name == 'posix' else 'explorer', file])
            else:
                with open(file, 'r') as f:
                    messagebox.showinfo("Relatório", json.dumps(json.load(f), indent=2)[:500])

    def new_scan(self):
        """Novo scan"""
        self.path_var.set("")
        self.status_text.delete(1.0, tk.END)

    def show_help(self):
        """Mostra ajuda"""
        help_text = """
H.A.V. SENTINEL - Guia Rápido

Tabs:
1. Scan de Segurança: Execute scans em aplicações
2. Resultados: Veja as vulnerabilidades encontradas
3. Relatórios: Gere e gerencie relatórios
4. Banco de Vulnerabilidades: Consulte vulnerabilidades conhecidas
5. Testes de Rede: Execute testes de rede

Para começar:
1. Selecione um diretório na aba "Scan de Segurança"
2. Escolha os tipos de scan desejados
3. Clique em "Iniciar Scan"
4. Veja os resultados na aba "Resultados"
5. Gere relatórios na aba "Relatórios"
        """
        messagebox.showinfo("Ajuda", help_text)

    def show_about(self):
        """Mostra informações sobre"""
        about_text = f"""
H.A.V. SENTINEL v{VERSION}
Hyper Application Vulnerability Sentinel

Advanced Application Security Analysis Framework

© 2026 Security Operations
{CODENAME}
        """
        messagebox.showinfo("Sobre", about_text)

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main_gui():
    """Função principal para GUI"""
    root = tk.Tk()
    app = HAVSentinelGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main_gui()
