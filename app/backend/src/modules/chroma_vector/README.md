# Sistema RAG Local — agno + ChromaDB + Ollama

Carregue documentos PDF/DOCX, armazene no ChromaDB e faça perguntas respondidas com IA local (Ollama llama3). Construído com **agno**: Agentic RAG nativo, chunking semantico com LLM e embeddings locais.

## Como funciona

```
PDF/DOCX → agno PDFReader/DocxReader → AgenticChunking (llama3)
         → OllamaEmbedder (nomic-embed-text) → ChromaDB (./chroma_db)
                                                      ↓
pergunta → agno Agent (search_knowledge=True) → llama3 → resposta
```

O `Agent` com `search_knowledge=True` implementa **Agentic RAG**: o proprio agente decide quando e o que buscar no banco vetorial, sem injetar contexto cego em todas as queries.

---

## Estrutura

| Arquivo              | Responsabilidade                                               |
| -------------------- | -------------------------------------------------------------- |
| `db.py`              | `ChromaDb` + `OllamaEmbedder` (nomic-embed-text)               |
| `document_loader.py` | `PDFReader` e `DocxReader` do agno                             |
| `chunking.py`        | `AgenticChunking` (llama3) + `RecursiveChunking` como fallback |
| `ingest_agent.py`    | `Knowledge.insert()` com chunker e metadata                    |
| `rag_agent.py`       | `Agent(knowledge=..., search_knowledge=True)`                  |
| `main.py`            | API FastAPI `/upload` e `/perguntar`, mais modo CLI            |
| `chroma_db/`         | Pasta de persistencia local (criada automaticamente)           |

---

## Requisitos

- Python 3.10+
- [Ollama](https://ollama.com) instalado e rodando localmente
- `agno>=2.5.12`, `chromadb`, `pypdf`, `python-docx` instalados

---

## 1. Instalar dependencias

A partir de `app/backend/`:

```powershell
# Com uv (recomendado — ja configurado no projeto)
uv sync

# Ou com pip
pip install agno chromadb pypdf python-docx fastapi uvicorn python-multipart
```

---

## 2. Baixar os modelos no Ollama

Em um terminal separado, antes de qualquer coisa:

```bash
# Modelo de inferencia (respostas)
ollama pull llama3

# Modelo de embeddings (vetorizacao dos documentos)
ollama pull nomic-embed-text

# Iniciar o servidor Ollama (se nao estiver rodando)
ollama serve
```

Ollama fica disponivel em `http://localhost:11434`. Mantenha-o rodando enquanto usa o sistema.

---

## 3. Iniciar a API

A partir de `app/backend/`:

```powershell
python -m src.modules.chroma_vector.main --serve
```

- API: `http://localhost:8010`
- Documentacao interativa (Swagger): `http://localhost:8010/docs`

---

## 4. Carregar um documento

> **Atencao:** `/upload` aceita apenas `POST`. Acessar a URL direto no navegador retorna `405 Method Not Allowed` — isso e normal. Use o Swagger ou curl como mostrado abaixo.

### Via curl

```bash
curl -X POST "http://localhost:8010/upload" \
  -F "file=@C:/caminho/seu_arquivo.pdf"
```

### Via Swagger

1. Acesse `http://localhost:8010/docs`
2. Clique em `POST /upload` → **Try it out**
3. Selecione o arquivo PDF ou DOCX
4. Clique em **Execute**

Formatos aceitos: `.pdf` e `.docx`.

Resposta esperada:

```json
{
  "arquivo": "norma_abnt.pdf",
  "status": "ok"
}
```

> O agno processa o arquivo em background: leitura → chunking semantico com llama3 → embedding com nomic-embed-text → persistencia no ChromaDB.

---

## 5. Fazer uma pergunta

### Via curl

```bash
curl "http://localhost:8010/perguntar?pergunta=Qual+o+escopo+desta+norma?"
```

### Via Swagger

1. Clique em `GET /perguntar` → **Try it out**
2. Preencha o campo `pergunta`
3. Clique em **Execute**

Resposta esperada:

```json
{
  "resposta": "De acordo com o documento norma_abnt.pdf, o escopo desta norma abrange..."
}
```

Se nenhum documento relevante for encontrado, o agente informa explicitamente que nao localizou a informacao.

---

## 6. Usar via linha de comando (sem API)

```powershell
# Ingerir um arquivo
python -m src.modules.chroma_vector.main --ingest C:/docs/norma.pdf

# Ingerir varios arquivos
python -m src.modules.chroma_vector.main --ingest C:/docs/norma.pdf C:/docs/manual.docx

# Fazer uma pergunta (apos ingestao previa)
python -m src.modules.chroma_vector.main --ask "Quais sao os requisitos minimos?"

# Ingerir e perguntar na mesma execucao
python -m src.modules.chroma_vector.main --ingest C:/docs/norma.pdf --ask "Qual o objetivo do documento?"
```

---

## Endpoints

| Metodo | Endpoint                  | Descricao                                     |
| ------ | ------------------------- | --------------------------------------------- |
| `GET`  | `/`                       | Health check                                  |
| `POST` | `/upload`                 | Carrega PDF/DOCX, ingere no ChromaDB via agno |
| `GET`  | `/perguntar?pergunta=...` | Pergunta ao agente RAG agentico               |

---

## Solucao de problemas

| Sintoma                          | Causa provavel                   | Solucao                                                   |
| -------------------------------- | -------------------------------- | --------------------------------------------------------- |
| `ImportError: chromadb`          | Pacote nao instalado             | `pip install chromadb`                                    |
| `ImportError: pypdf`             | Pacote nao instalado             | `pip install pypdf`                                       |
| `ImportError: python-docx`       | Pacote nao instalado             | `pip install python-docx`                                 |
| Timeout na ingestao              | llama3 lento no chunking         | Normal em CPUs. Aguarde ou use `RecursiveChunking` direto |
| Resposta vazia / "nao encontrei" | Documento nao ingerido ainda     | Execute `/upload` antes de perguntar                      |
| `nomic-embed-text not found`     | Modelo de embedding ausente      | `ollama pull nomic-embed-text`                            |
| Banco vazio apos reinicio        | `chroma_db/` em diretorio errado | Execute sempre a partir de `app/backend/`                 |

---

## Observacoes

- O banco vetorial e salvo em `./chroma_db/` relativo ao diretorio de execucao. **Execute sempre a partir de `app/backend/`**.
- O `AgenticChunking` envia cada bloco ao llama3 para divisao semantica. Se o modelo nao estiver disponivel ou falhar, o sistema cai automaticamente para `RecursiveChunking` sem interromper a ingestao.
- Embeddings sao gerados localmente pelo `nomic-embed-text` via Ollama — nenhum dado sai da maquina.
- Quanto maior o texto, melhor a busca por similaridade
- Os arquivos temporarios de upload sao deletados automaticamente

```

```
