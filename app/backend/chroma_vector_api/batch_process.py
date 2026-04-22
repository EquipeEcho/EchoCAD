"""Script para processar múltiplos arquivos (DOCX/PDF) e adicionar ao ChromaDB em lote."""

import uuid
from pathlib import Path

from db import get_collection
from document_processor import extract_text_from_file


def process_documents_folder(folder_path: str) -> None:
    """Processa todos os arquivos DOCX e PDF de uma pasta e adiciona ao ChromaDB.

    Args:
        folder_path: Caminho da pasta contendo os documentos.
    """
    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        print(f"Erro: A pasta '{folder_path}' não existe ou não é uma pasta válida.")
        return

    # Busca todos os arquivos DOCX e PDF
    doc_files = list(folder.glob("*.docx")) + list(folder.glob("*.pdf"))

    if not doc_files:
        print(f"Nenhum arquivo .docx ou .pdf encontrado em '{folder_path}'")
        return

    collection = get_collection()
    added_count = 0
    errors = []

    print(f"Encontrados {len(doc_files)} arquivo(s). Processando...\n")

    for file_path in doc_files:
        try:
            print(f"  Processando: {file_path.name}...", end=" ")

            # Extrai o texto
            extracted_text = extract_text_from_file(str(file_path))

            if not extracted_text:
                print("IGNORADO (texto vazio)")
                continue

            # Gera ID único
            norma_id = f"norma-{uuid.uuid4().hex[:8]}"

            # Adiciona à coleção
            collection.add(
                ids=[norma_id],
                documents=[extracted_text],
                metadatas=[
                    {
                        "filename": file_path.name,
                        "file_type": file_path.suffix[1:].upper(),
                    }
                ],
            )

            print(f"OK (id: {norma_id})")
            added_count += 1

        except Exception as e:
            error_msg = f"{file_path.name}: {str(e)}"
            print(f"ERRO")
            errors.append(error_msg)

    # Resumo
    print(f"\n--- Resumo ---")
    print(f"Total processado: {len(doc_files)}")
    print(f"Adicionados: {added_count}")
    if errors:
        print(f"Erros: {len(errors)}")
        for err in errors:
            print(f"  - {err}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python batch_process.py <caminho_da_pasta>")
        print("Exemplo: python batch_process.py ./documentos")
        sys.exit(1)

    folder = sys.argv[1]
    process_documents_folder(folder)
