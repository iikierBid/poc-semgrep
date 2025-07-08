#!/usr/bin/env python3
import json
import sys
from datetime import datetime
import os

def convert_sarif_to_html(sarif_file, output_file):
    """Converte um arquivo SARIF para HTML legível"""
    try:
        with open(sarif_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Segurança - Semgrep</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .header h1 {{ margin: 0; }}
        .summary {{ background: #e3f2fd; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #2196f3; }}
        .vulnerability {{ margin: 15px 0; padding: 20px; border-radius: 8px; border-left: 4px solid #ffc107; }}
        .vulnerability.error {{ background: #ffebee; border-left-color: #f44336; }}
        .vulnerability.warning {{ background: #fff3e0; border-left-color: #ff9800; }}
        .vulnerability.info {{ background: #e8f5e8; border-left-color: #4caf50; }}
        .vuln-title {{ color: #d32f2f; margin-top: 0; }}
        .vuln-meta {{ display: flex; gap: 20px; margin: 10px 0; }}
        .meta-item {{ background: #f5f5f5; padding: 5px 10px; border-radius: 4px; font-size: 0.9em; }}
        .severity {{ font-weight: bold; padding: 4px 8px; border-radius: 4px; color: white; text-transform: uppercase; }}
        .severity.error {{ background: #f44336; }}
        .severity.warning {{ background: #ff9800; }}
        .severity.info {{ background: #4caf50; }}
        .no-vulns {{ background: #e8f5e8; border-left-color: #4caf50; text-align: center; }}
        .footer {{ margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; }}
        .code-snippet {{ background: #f8f9fa; padding: 10px; border-radius: 4px; font-family: monospace; margin: 10px 0; border: 1px solid #e9ecef; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Relatório de Segurança - Semgrep</h1>
            <p>Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
        </div>
'''
        
        total_findings = 0
        all_results = []
        
        # Coleta todas as descobertas
        for run in data.get('runs', []):
            results = run.get('results', [])
            total_findings += len(results)
            all_results.extend(results)
        
        # Resumo
        if total_findings > 0:
            html += f'''
        <div class="summary">
            <h2>📊 Resumo da Análise</h2>
            <p><strong>{total_findings}</strong> vulnerabilidade(s) encontrada(s) que precisam de atenção.</p>
        </div>
'''
            
            # Lista as vulnerabilidades
            for i, result in enumerate(all_results, 1):
                rule_id = result.get('ruleId', 'Regra desconhecida')
                message = result.get('message', {}).get('text', 'Sem descrição disponível')
                level = result.get('level', 'warning')
                
                # Informações do arquivo
                locations = result.get('locations', [])
                file_info = 'Arquivo desconhecido'
                line_info = 'N/A'
                
                if locations:
                    physical_location = locations[0].get('physicalLocation', {})
                    artifact_location = physical_location.get('artifactLocation', {})
                    file_path = artifact_location.get('uri', 'Arquivo desconhecido')
                    region = physical_location.get('region', {})
                    start_line = region.get('startLine', 'N/A')
                    file_info = file_path
                    line_info = f"Linha {start_line}"
                
                html += f'''
        <div class="vulnerability {level}">
            <h3 class="vuln-title">🚨 Vulnerabilidade #{i}: {rule_id}</h3>
            <div class="vuln-meta">
                <span class="severity {level}">{level}</span>
                <span class="meta-item">📁 {file_info}</span>
                <span class="meta-item">📍 {line_info}</span>
            </div>
            <p><strong>Descrição:</strong> {message}</p>
        </div>
'''
        else:
            html += '''
        <div class="vulnerability no-vulns">
            <h3>✅ Parabéns! Nenhuma vulnerabilidade encontrada!</h3>
            <p>Seu código passou em todas as verificações de segurança.</p>
        </div>
'''
        
        html += '''
        <div class="footer">
            <h3>ℹ️ Próximos Passos</h3>
            <ul>
                <li>📋 Revise cada vulnerabilidade listada acima</li>
                <li>🔧 Corrija os problemas de segurança encontrados</li>
                <li>🔄 Execute o scan novamente para verificar as correções</li>
                <li>📚 Consulte a <a href="https://semgrep.dev/docs/" target="_blank">documentação do Semgrep</a> para mais informações</li>
            </ul>
            <p><small>Relatório gerado automaticamente pelo Semgrep via GitHub Actions</small></p>
        </div>
    </div>
</body>
</html>
'''
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Relatório HTML gerado com sucesso: {output_file}")
        print(f"📊 Total de vulnerabilidades: {total_findings}")
        
    except Exception as e:
        print(f"❌ Erro ao converter SARIF para HTML: {e}")
        sys.exit(1)

if __name__ == "__main__":
    sarif_file = "semgrep.sarif"
    output_file = "semgrep-report.html"
    
    if not os.path.exists(sarif_file):
        print(f"❌ Arquivo SARIF não encontrado: {sarif_file}")
        sys.exit(1)
    
    convert_sarif_to_html(sarif_file, output_file) 