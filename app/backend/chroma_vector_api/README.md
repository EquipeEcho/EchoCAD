# API FastAPI + ChromaDB (colecao normas)

Projeto simples para leitura e busca por similaridade em uma colecao vetorial local usando ChromaDB.

## Estrutura

- `main.py`: API FastAPI e endpoints (GET e POST)
- `db.py`: conexao com ChromaDB e acesso a colecao `normas`
- `seed_data.py`: script opcional para inserir dados de exemplo
- `document_processor.py`: funcoes para extrair texto de DOCX e PDF
- `batch_process.py`: script para processar multiplos arquivos em lote
- `chroma_db/`: pasta de persistencia local do ChromaDB

## Como executar

1. Criar ambiente virtual (opcional, recomendado):

```bash
python -m venv .venv
```

2. Ativar ambiente virtual:

- Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. (Opcional) Inserir dados de exemplo:

```bash
python seed_data.py
```

5. Iniciar API com uvicorn:

```bash
uvicorn main:app --reload
```

6. Testar endpoints:

- Lista completa: `GET http://127.0.0.1:8000/normas`
- Busca semantica: `GET http://127.0.0.1:8000/buscar?query=seguranca`
- Docs interativa: `http://127.0.0.1:8000/docs`

## Adicionar Normas via Arquivo (DOCX/PDF)

### Opcao 1: Upload individual via API

Use o endpoint `/upload-documento` para fazer upload de um arquivo DOCX ou PDF:

```bash
curl -X POST "http://127.0.0.1:8000/upload-documento" \
  -F "file=@seu_arquivo.pdf"
```

Ou via a interface Swagger em `http://127.0.0.1:8000/docs`:

- Clique em `/upload-documento`
- Clique em "Try it out"
- Selecione seu arquivo DOCX ou PDF
- Clique em "Execute"

### Opcao 2: Processar multiplos arquivos em lote

Coloque todos os seus arquivos DOCX e PDF em uma pasta, depois execute:

```bash
python batch_process.py ./caminho_da_pasta_com_documentos
```

Exemplo:

```bash
python batch_process.py ./documentos
```

O script vai:

1. Procurar por todos os arquivos `.docx` e `.pdf`
2. Extrair o texto completo de cada um
3. Adicionar automaticamente ao ChromaDB com ID único

### Opcao 3: Criar norma manualmente

```bash
curl -X POST "http://127.0.0.1:8000/normas" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "norma-custom-001",
    "document": "Seu texto de norma aqui...",
    "metadata": {"categoria": "seguranca", "codigo": "NBR-12345"}
  }'
```

## Tipos Suportados

- **PDF**: Extrai texto de todas as paginas (incluindo numero da pagina)
- **DOCX**: Extrai texto de parágrafos

## Notas

- ChromaDB usa embedding automatico (modelo padrão)
- Quanto maior o texto, melhor a busca por similaridade
- Os arquivos temporarios de upload sao deletados automaticamente
