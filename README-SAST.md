# 🔒 Relatórios de Segurança - Semgrep

Este projeto usa **Semgrep** para análise estática de segurança (SAST). Aqui está como visualizar e trabalhar com os relatórios.

## 📊 Como Visualizar Relatórios

### Opção 1: GitHub Actions (Automático)
Quando você cria um Pull Request, o Semgrep roda automaticamente e:
- ❌ **Bloqueia o PR** se encontrar vulnerabilidades
- 📄 **Gera relatórios** em formato SARIF e HTML
- 📎 **Anexa os relatórios** como artifacts

**Para acessar:**
1. Vá para seu PR no GitHub
2. Clique na aba **"Checks"** 
3. Clique no job **"Semgrep SAST Scan"**
4. Na seção **"Artifacts"**, baixe o `semgrep-report.zip`
5. Extraia e abra o `semgrep-report.html` no navegador

### Opção 2: Executar Localmente
```bash
# Instale o Semgrep
pip install semgrep

# Execute o scan e gere relatório
semgrep --config=auto --sarif --output=semgrep.sarif .

# Visualize o relatório no navegador
python view_report.py
```

### Opção 3: Apenas Converter SARIF Existente
```bash
# Se você já tem um arquivo .sarif
python convert_sarif_to_html.py

# Ou especifique um arquivo diferente
python -c "
from convert_sarif_to_html import convert_sarif_to_html
convert_sarif_to_html('meu-arquivo.sarif', 'relatorio.html')
"
```

## 🚨 Entendendo os Relatórios

### Níveis de Severidade
- 🔴 **ERROR**: Vulnerabilidades críticas que bloqueiam o PR
- 🟡 **WARNING**: Problemas importantes que devem ser revisados
- 🔵 **INFO**: Sugestões de melhoria

### Informações Incluídas
- **Regra**: Qual regra de segurança foi violada
- **Descrição**: Explicação do problema
- **Localização**: Arquivo e linha onde está o problema
- **Nível**: Severidade da vulnerabilidade

## 🔧 Corrigindo Vulnerabilidades

1. **Identifique** a vulnerabilidade no relatório
2. **Localize** o arquivo e linha mencionados
3. **Corrija** o código seguindo as boas práticas de segurança
4. **Teste** localmente com `semgrep --config=auto .`
5. **Commit** e push das correções

## 📚 Recursos Úteis

- [Documentação do Semgrep](https://semgrep.dev/docs/)
- [Regras de Segurança](https://semgrep.dev/r)
- [Playground do Semgrep](https://semgrep.dev/playground/)

## 🛠️ Arquivos do Projeto

- `.github/workflows/sast.yml` - Configuração do GitHub Actions
- `convert_sarif_to_html.py` - Conversor SARIF → HTML
- `view_report.py` - Visualizador local de relatórios
- `.semgrep.yml` - Regras customizadas de segurança
- `README-SAST.md` - Esta documentação

## 🔧 Regras Customizadas

O projeto inclui regras customizadas em `.semgrep.yml` que detectam:

### 🔑 **Secrets Hardcoded**
- **API Keys**: Detecta chaves com padrões como `API_KEY = "..."`
- **AWS Access Keys**: Detecta chaves AWS com prefixo `AKIA`
- **Stripe Keys**: Detecta chaves Stripe com prefixos `sk_live_` e `sk_test_`

### 📝 **Como Adicionar Novas Regras**
1. Edite o arquivo `.semgrep.yml`
2. Adicione uma nova regra seguindo o formato YAML
3. Teste localmente: `semgrep --config=.semgrep.yml .`
4. Commit e push para aplicar automaticamente

---

## ⚙️ **Diferença entre `semgrep ci` vs `semgrep scan`**

### **`semgrep ci` (Produção) - ✅ Em Uso**
- **Diff-aware**: Só reporta vulnerabilidades **novas** introduzidas no PR
- **Ideal para produção**: Não bloqueia por vulnerabilidades existentes na main
- **Foco**: Prevenir introdução de novas vulnerabilidades
- **Comparação**: Compara branch atual com branch main

### **`semgrep scan` (Auditoria Completa)**
- **Full scan**: Reporta **todas** as vulnerabilidades no código
- **Ideal para auditoria**: Mostra o estado atual completo de segurança
- **Foco**: Auditoria completa do código
- **Sem comparação**: Escaneia todo o código independente da branch

### **Configuração Atual**
- **✅ Usando `semgrep ci`**: Detecta vulnerabilidades novas em relação à main
- **Cenário**: Branch main limpa, branch de teste com vulnerabilidades
- **Resultado**: Deve detectar e bloquear as vulnerabilidades do `app.py`

💡 **Dica**: Para desenvolvimento local, use `semgrep --config=auto .` para verificar seu código antes de fazer commit! 