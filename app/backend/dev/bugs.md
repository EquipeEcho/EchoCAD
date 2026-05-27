# Relatório de Erros e Pontos de Atenção - Backend EchoCAD

Este documento lista os problemas identificados durante a análise detalhada do código, excetuando os itens de infraestrutura já corrigidos.

## 1. Erros Críticos de Código (Bugs de Execução)

*   **Ausência de `await` em Funções Assíncronas (`src/routes/router_project.py`):**
    *   Nas rotas `post_create_project` (linha 35) e `patch_update_project` (linha 105), as funções `create_projeto` e `update_project` são chamadas sem o prefixo `await`. Como ambas são `async`, a rota retornará um objeto *coroutine* em vez do resultado esperado, o que causará falha na resposta da API e impedirá a persistência correta no banco.
*   **Incompatibilidade de Parâmetro de Rota (`src/routes/router_standards.py`):**
    *   Na rota `toggle_standard` (linha 57), o decorador define `/{norma_id}/toggle`, mas a função recebe `standard_id: int`. O FastAPI retornará um erro `422 Unprocessable Entity` porque o nome do parâmetro no caminho não coincide com o argumento da função.

## 2. Falhas de Segurança e Validação

*   **Vulnerabilidade de Path Traversal (`src/routes/router_blueprints.py`):**
    *   A rota `extrair_dxf` (linha 63) recebe um parâmetro `caminho` (string) do usuário e o passa diretamente para `processar_dxf` após verificar apenas se o arquivo existe. Um usuário mal-intencionado poderia passar caminhos como `/etc/passwd` ou arquivos sensíveis do sistema.
*   **Inconsistência nos Caminhos de Upload:**
    *   `router_processing.py` e `router_upload.py` definem caminhos de upload baseados na raiz do projeto (`BACKEND_ROOT`). Já o `router_specification.py` (linha 19) usa `Path("uploads")`. Se o diretório de trabalho da aplicação mudar, os arquivos serão salvos em locais diferentes e não serão encontrados.

## 3. Inconsistências de Lógica e Qualidade de Código

*   **Duplicação de Lógica de Parsing DXF:**
    *   Os arquivos `src/modules/Memorial/dxf_extractor.py` e `src/modules/EspecificacoesTecnicas/dxf_context_extractor.py` implementam essencialmente o mesmo parser manual de DXF (`DXFParser`).
*   **Chamadas Bloqueantes em Rotas Assíncronas:**
    *   Diversas rotas `async` utilizam funções síncronas pesadas como `shutil.copyfileobj`, `SpecGenerator` (que usa a biblioteca `requests` síncrona) e o processamento de DXF/Excel. Isso bloqueia o *event loop* do FastAPI.
*   **Tratamento de Erros no `drill.py`:**
    *   A função `carregar_configuracao` em `src/modules/drill.py` apenas imprime um aviso se o arquivo `zconfig_sistema.json` não for encontrado, mas o código prossegue e falha logo em seguida.
*   **Uso de `datetime.utcnow()` (`src/auth.py`):**
    *   O uso de `utcnow()` está depreciado no Python 3.13. O recomendado é `datetime.now(timezone.utc)`.
*   **Constraint de Unicidade em `Blueprint.path`:**
    *   No modelo `projeto_db.py`, o campo `path` da tabela `blueprints` é `unique=True`, o que pode causar conflitos se o mesmo nome de arquivo for usado em projetos diferentes.

## 4. Observações Menores

*   **Variáveis não utilizadas:** Em `drill.py`, o operador walrus `entity_end_y := entidade.dxf.end.y` é usado, mas a variável nunca é lida.
*   **Configuração de API:** O `SpecGenerator` depende da `GROQ_API_KEY`, que está com valor de placeholder.
