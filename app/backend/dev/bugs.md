# Relatório de Erros e Pontos de Atenção - Backend EchoCAD

Este documento lista os problemas identificados no código que ainda precisam de correção.

## 1. Erros Críticos e Segurança

*   **Vulnerabilidade de Path Traversal (`src/routes/router_blueprints.py`):**
    *   A rota `extrair_dxf` (linha 63) recebe um parâmetro `caminho` (string) do usuário e o utiliza diretamente para verificar a existência do arquivo e processá-lo. Um usuário mal-intencionado poderia acessar arquivos sensíveis do sistema fora da pasta de uploads.
*   **Tratamento de Erros Deficiente em `drill.py`:**
    *   A função `carregar_configuracao` em `src/modules/drill.py` apenas imprime um aviso se o arquivo `zconfig_sistema.json` não for encontrado, retornando `None`. O código subsequente tenta acessar chaves nesse retorno, o que causará um `TypeError`.

## 2. Qualidade de Código e Performance

*   **Chamadas Bloqueantes em Rotas Assíncronas:**
    *   Diversas rotas `async` executam operações síncronas pesadas que bloqueiam o *event loop* do FastAPI, prejudicando a escalabilidade:
        *   `shutil.copyfileobj` no `router_upload.py`.
        *   Processamento CPU-bound de DXF (`processar_dxf` e `run_integration`) no `router_processing.py`.
        *   Chamadas de rede síncronas via biblioteca `requests` no `SpecGenerator`.
*   **Duplicação de Lógica de Parsing DXF:**
    *   Os arquivos `src/modules/Memorial/dxf_extractor.py` e `src/modules/EspecificacoesTecnicas/dxf_context_extractor.py` implementam essencialmente o mesmo parser manual de DXF (`DXFParser`), dificultando a manutenção.

## 3. Configurações e Observações Menores

*   **Configuração de API com Placeholder:**
    *   O `settings.GROQ_API_KEY` em `src/config.py` está configurado com o valor de placeholder `"gsk_REPLACE_ME"`.

---
*Última atualização: 27 de maio de 2026*
