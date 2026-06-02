#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║       H.A.V. SENTINEL LAUNCHER — Sistema de Inicialização                      ║
# ║              Hyper Application Vulnerability Sentinel                           ║
# ║                          Version 2.0 — Production Ready                         ║
# ╚══════════════════════════════════════════════════════════════════════════════════╝

"""
H.A.V. SENTINEL Launcher
========================
Seletor de interface (CLI ou GUI) para H.A.V. SENTINEL
"""

import os
import sys
import argparse
from pathlib import Path

# Adicionar diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hav_sentinel_core import VERSION, CODENAME, C

def show_launcher_banner():
    """Exibe banner do launcher"""
    banner = f"""
    {C.BCYAN}╔════════════════════════════════════════════════════════════════════════════════╗{C.RESET}
    {C.BCYAN}║{C.RESET}                                                                            {C.BCYAN}║{C.RESET}
    {C.BCYAN}║{C.RESET}  {C.BOLD}{C.BMAGENTA}H.A.V. SENTINEL LAUNCHER{C.RESET}                                                   {C.BCYAN}║{C.RESET}
    {C.BCYAN}║{C.RESET}  Hyper Application Vulnerability Sentinel                               {C.BCYAN}║{C.RESET}
    {C.BCYAN}║{C.RESET}                                                                            {C.BCYAN}║{C.RESET}
    {C.BCYAN}║{C.RESET}  {C.BOLD}Version {C.BGREEN}{VERSION}{C.RESET} | {C.BBLUE}{CODENAME}{C.RESET}                                  {C.BCYAN}║{C.RESET}
    {C.BCYAN}║{C.RESET}  Choose Your Interface                                                   {C.BCYAN}║{C.RESET}
    {C.BCYAN}║{C.RESET}                                                                            {C.BCYAN}║{C.RESET}
    {C.BCYAN}╚════════════════════════════════════════════════════════════════════════════════╝{C.RESET}
    """
    print(banner)

def interactive_mode():
    """Modo interativo de seleção"""
    show_launcher_banner()

    print(f"\n{C.BOLD}Selecione a interface:{C.RESET}\n")
    print(f"  {C.BCYAN}[1]{C.RESET} {C.BOLD}CLI{C.RESET} — Command Line Interface (Recomendado para automação)")
    print(f"  {C.BCYAN}[2]{C.RESET} {C.BOLD}GUI{C.RESET} — Graphical User Interface (Recomendado para desktop)")
    print(f"  {C.BCYAN}[0]{C.RESET} Sair\n")

    choice = input(f"{C.PROMPT}Escolha:{C.RESET} ").strip()

    if choice == "1":
        launch_cli()
    elif choice == "2":
        launch_gui()
    elif choice == "0":
        print(f"\n{C.DIM}Encerrando...{C.RESET}\n")
        sys.exit(0)
    else:
        print(f"{C.FAIL}Opção inválida{C.RESET}\n")
        interactive_mode()

def launch_cli(target: str = ""):
    """Lança a versão CLI.

    FIX: limpa sys.argv antes de importar main_cli para que o argparse
    interno da CLI não receba --cli / --gui / --target do launcher.
    """
    print(f"\n{C.SUCCESS}Iniciando H.A.V. SENTINEL CLI...{C.RESET}\n")

    # Preservar apenas o nome do executável; repassar --target se fornecido
    sys.argv = [sys.argv[0]]
    if target:
        sys.argv += ["-t", target]

    try:
        from hav_sentinel_cli import main_cli
        main_cli()
    except ImportError as e:
        print(f"{C.FAIL}Erro ao importar CLI:{C.RESET} {e}")
        print(f"\n{C.WARN}Certifique-se de que todos os arquivos estão no mesmo diretório{C.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{C.FAIL}Erro ao executar CLI:{C.RESET} {e}")
        sys.exit(1)

def launch_gui():
    """Lança a versão GUI.

    FIX: limpa sys.argv para evitar que flags do launcher vazem para tkinter.
    """
    print(f"\n{C.SUCCESS}Iniciando H.A.V. SENTINEL GUI...{C.RESET}\n")

    sys.argv = [sys.argv[0]]

    try:
        import tkinter  # noqa: F401
    except ImportError:
        print(f"{C.FAIL}Erro: tkinter não está instalado{C.RESET}")
        print(f"\n{C.WARN}Instale com:{C.RESET}")
        print(f"  {C.DIM}Ubuntu/Debian: sudo apt-get install python3-tk{C.RESET}")
        print(f"  {C.DIM}macOS: brew install python-tk{C.RESET}")
        print(f"  {C.DIM}Windows: use o instalador oficial com 'tcl/tk and IDLE' marcado{C.RESET}")
        sys.exit(1)

    try:
        from hav_sentinel_gui import main_gui
        main_gui()
    except ImportError as e:
        print(f"{C.FAIL}Erro ao importar GUI:{C.RESET} {e}")
        print(f"\n{C.WARN}Certifique-se de que todos os arquivos estão no mesmo diretório{C.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{C.FAIL}Erro ao executar GUI:{C.RESET} {e}")
        sys.exit(1)

def main():
    """Função principal do launcher"""
    parser = argparse.ArgumentParser(
        description="H.A.V. SENTINEL Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python3 hav_sentinel_launcher.py                        # Modo interativo
  python3 hav_sentinel_launcher.py --cli                  # CLI diretamente
  python3 hav_sentinel_launcher.py --gui                  # GUI diretamente
  python3 hav_sentinel_launcher.py --cli --target /app    # CLI com alvo
        """
    )

    parser.add_argument("--cli",    action="store_true", help="Executa versão CLI")
    parser.add_argument("--gui",    action="store_true", help="Executa versão GUI")
    parser.add_argument("--target", help="Alvo para o scan (CLI apenas)")
    parser.add_argument("--version", action="version", version=f"H.A.V. SENTINEL v{VERSION}")

    args = parser.parse_args()

    if not args.cli and not args.gui:
        interactive_mode()
    elif args.cli:
        launch_cli(target=args.target or "")
    elif args.gui:
        launch_gui()

if __name__ == "__main__":
    main()
