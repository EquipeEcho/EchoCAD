"""
🚀 QUICK START - Módulo Knowledge RAG para Normas ABNT

Este guia rápido mostra como começar a usar o módulo de normas.
"""

# ============================================================================
# PASSO 1: VERIFICAR AMBIENTE
# ============================================================================

# No terminal, execute:
# python -m src.modules.knowledge.demo

# Isto verificará:
# ✓ Dependências instaladas
# ✓ Ollama conectado
# ✓ Modelos disponíveis
# ✓ Módulo funcionando


# ============================================================================
# PASSO 2: CARREGAR NORMAS
# ============================================================================

# Opção A: Via CLI (batch)
# ========================
# 1. Coloque arquivos PDF em um diretório, ex: ./normas/
#
# 2. Execute:
#    python -m src.modules.knowledge.main ingest ./normas/
#
# 3. Aguarde conclusão


# Opção B: Via Python
# ===================
from results.knowledge import ingest_normas_batch, ingest_norma_file

# Carregar múltiplas normas
resultado = ingest_normas_batch("/caminho/das/normas/")
print(resultado)
# {
#   "total": 5,
#   "sucesso": 5,
#   "erro": 0,
#   "detalhes": [...]
# }

# Carregar arquivo individual
resultado = ingest_norma_file(
    "/caminho/nbr6118.pdf",
    norma_id="NBR 6118"
)
print(resultado)
# {
#   "status": "sucesso",
#   "arquivo": "nbr6118.pdf",
#   "norma_id": "NBR 6118",
#   "documentos": 45
# }


# ============================================================================
# PASSO 3: CONSULTAR NORMAS
# ============================================================================

# Opção A: Via CLI
# ================
# Pergunta simples:
#   python -m src.modules.knowledge.main query "Como dimensionar uma viga?"
#
# Com informações de fontes:
#   python -m src.modules.knowledge.main query "NBR 6118" --com-fontes


# Opção B: Via Python
# ===================
from results.knowledge import query_normas
from results.knowledge.normas_rag_agent import query_normas_com_fontes

# Resposta simples
resposta = query_normas("Como dimensionar uma viga de concreto armado?")
print(resposta)
# Output: Resposta longa baseada em normas técnicas...

# Com informações de fontes
resultado = query_normas_com_fontes("Espessura mínima de parede em alvenaria")
print(resultado)
# {
#   "pergunta": "...",
#   "resposta": "...",
#   "fontes_consultadas": 3,
#   "contexto_disponível": True
# }


# ============================================================================
# PASSO 4: INTEGRAR COM FASTAPI
# ============================================================================

# Em src/main.py ou equivalente:

from fastapi import FastAPI
from src.routes.normas_router import router as normas_router

app = FastAPI()

# Incluir router de normas
app.include_router(normas_router)

# Agora você tem endpoints:
# POST /api/normas/consultar
# POST /api/normas/consultar-com-fontes
# POST /api/normas/ingest-arquivo
# POST /api/normas/ingest-lote
# GET  /api/normas/status
# GET  /api/normas/health


# ============================================================================
# PASSO 5: PERGUNTAS DE TESTE
# ============================================================================

# Exemplos de perguntas para testar:

perguntas = [
    "Como dimensionar uma viga de concreto armado?",
    "Qual é a altura mínima de um ambiente residencial?",
    "Requisitos de segurança para trabalho em altura",
    "Como calcular a espessura mínima de parede?",
    "Diâmetro mínimo de tubulação de água",
    "Requisitos para impermeabilização de laje",
    "Acabamento de concreto aparente",
    "Proteção contra fogo em estruturas de aço",
]

for pergunta in perguntas:
    resposta = query_normas(pergunta)
    print(f"Q: {pergunta}")
    print(f"A: {resposta}\n")


# ============================================================================
# CONFIGURAÇÃO AVANÇADA
# ============================================================================

# Mudar modelo de embedding:
#   db.py: EMBED_MODEL = "mxbai-embed-large"

# Mudar modelo de inferência:
#   normas_rag_agent.py: NORMAS_MODEL = "qwen2.5:3b"

# Ajustar tamanho de chunks:
#   normas_ingestor.py: chunk_size=1500, chunk_overlap=300

# Limpar banco completamente:
#   python -m src.modules.knowledge.main clear --force


# ============================================================================
# TROUBLESHOOTING
# ============================================================================

# ❌ "Ollama connection refused"
#    → Inicie Ollama: ollama serve

# ❌ "Modelo não encontrado"
#    → Puxe modelos: ollama pull nomic-embed-text; ollama pull qwen2.5:7b

# ❌ "Pergunta não retorna resposta relevante"
#    → Verifique se normas foram carregadas com ingest_normas_batch

# ❌ "ChromaDB database corrupted"
#    → Limpe: rm -rf ./chroma_db/normas/
#    → Recarregue: python -m src.modules.knowledge.main ingest ./normas/


# ============================================================================
# DOCUMENTAÇÃO COMPLETA
# ============================================================================

# Ver README.md para:
# ✓ Arquitetura completa
# ✓ Estrutura de dados
# ✓ Performance
# ✓ Exemplos avançados
# ✓ Configurações
# ✓ Troubleshooting


# ============================================================================
# ESTRUTURA DE ARQUIVOS
# ============================================================================

"""
src/modules/knowledge/
├── __init__.py                    # Exports principais
├── db.py                          # ChromaDB config
├── normas_loader.py               # PDF loader
├── normas_ingestor.py             # Ingestão + chunking
├── normas_rag_agent.py            # Agente RAG (main)
├── main.py                        # CLI
├── demo.py                        # Teste e demo
└── README.md                      # Documentação

src/routes/
└── normas_router.py               # FastAPI endpoints

Dados:
└── chroma_db/
    └── normas/                    # Banco vetorial persistente
        ├── index/
        ├── collections/
        └── data/
"""


# ============================================================================
# PRÓXIMOS PASSOS
# ============================================================================

# 1. ✓ Estrutura criada
# 2. → Carregar normas ABNT em PDF
# 3. → Testar via CLI ou Python
# 4. → Integrar com API FastAPI
# 5. → Usar em especificações técnicas
# 6. → Otimizar prompt e modelos conforme necessário
