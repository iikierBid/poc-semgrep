#!/usr/bin/env python3
"""
Script para visualizar relatórios SARIF do Semgrep localmente
Uso: python view_report.py [arquivo.sarif]
"""

import sys
import os
import webbrowser
from convert_sarif_to_html import convert_sarif_to_html

def main():
    # Arquivo SARIF padrão ou passado como argumento
    sarif_file = sys.argv[1] if len(sys.argv) > 1 else "semgrep.sarif"
    html_file = "semgrep-report.html"
    
    if not os.path.exists(sarif_file):
        print(f"❌ Arquivo não encontrado: {sarif_file}")
        print("💡 Execute primeiro: semgrep --config=auto --sarif --output=semgrep.sarif .")
        return 1
    
    # Converte SARIF para HTML
    convert_sarif_to_html(sarif_file, html_file)
    
    # Abre no navegador
    if os.path.exists(html_file):
        file_path = os.path.abspath(html_file)
        webbrowser.open(f"file://{file_path}")
        print(f"🌐 Relatório aberto no navegador: {file_path}")
    else:
        print("❌ Falha ao gerar relatório HTML")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 