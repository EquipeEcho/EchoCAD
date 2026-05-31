# Relatório de Erros e Pontos de Atenção - Backend EchoCAD

Este documento lista os problemas identificados no código que ainda precisam de correção.

## 1. Erros Críticos e Segurança

*   **Vulnerabilidade de Path Traversal (`src/routes/router_blueprints.py`):**
    *   A rota `extrair_dxf` (linha 63) recebe um parâmetro `caminho` (string) do usuário e o utiliza diretamente para verificar a existência do arquivo e processá-lo. Um usuário mal-intencionado poderia acessar arquivos sensíveis do sistema fora da pasta de uploads.

## 2. Qualidade de Código e Performance

*   **Chamadas Bloqueantes em Rotas Assíncronas:**
    *   Diversas rotas `async` executam operações síncronas pesadas que bloqueiam o *event loop* do FastAPI, prejudicando a escalabilidade:
        *   Processamento CPU-bound de DXF (`processar_dxf` e `run_integration`) no `router_processing.py`.
*   **Duplicação de Lógica de Parsing DXF:**
    *   `src/modules/Memorial/dxf_extractor.py` e `src/modules/EspecificacoesTecnicas/dxf_context_extractor.py` ainda implementam o seu próprio `DXFParser` manual, o que deve ser consolidado em um utilitário comum.

---
*Última atualização: 30 de maio de 2026*
