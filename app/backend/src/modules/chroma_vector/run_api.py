"""
Script de inicialização para a API Chroma Vector.
Configura o ambiente e inicia o servidor uvicorn.
"""

import sys
from pathlib import Path

# Configura o path para resolver os imports do projeto
# O arquivo está em: app/backend/src/modules/chroma_vector_api/run_api.py
current_file = Path(__file__).resolve()
modules_path = current_file.parent  # chroma_vector_api
src_path = modules_path.parent      # modules
backend_src_path = src_path.parent   # src
backend_path = backend_src_path.parent  # backend
project_root = backend_path.parent    # app

# Adiciona os caminhos necessários ao sys.path
sys.path.insert(0, str(backend_src_path))  # src/
sys.path.insert(0, str(backend_path))      # app/backend/
sys.path.insert(0, str(project_root / "app" / "backend"))  # app/backend/ (para app.backend.src)

# Cria a estrutura de diretórios virtual se não existir
(app_path := backend_path / "app").mkdir(exist_ok=True)
(app_path / "__init__.py").touch(exist_ok=True)
(app_backend_path := app_path / "backend").mkdir(exist_ok=True)
(app_backend_path / "__init__.py").touch(exist_ok=True)

# Agora importa e executa o uvicorn
if __name__ == "__main__":
    import uvicorn
    from src.modules.chroma_vector.main import app
    
    print("Iniciando Chroma Vector API...")
    print("Acesse: http://127.0.0.1:8000/docs")
    print("Acesse: http://127.0.0.1:8000/normas")
    
    uvicorn.run(app, host="localhost", port=8000)