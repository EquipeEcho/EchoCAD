"""Script opcional para popular a coleção 'normas' com dados de exemplo."""

from db import get_collection


def seed_example_data() -> None:
    """Insere documentos de exemplo na coleção vetorial.

    O uso de ids fixos permite reexecução segura com atualização dos itens.
    """
    collection = get_collection()

    ids = [
        "norma-001",
        "norma-002",
        "norma-003",
        "norma-004",
        "norma-005",
        "norma-006",
    ]

    documents = [
        "Norma de segurança para uso de equipamentos de proteção individual em obras.",
        "Procedimento para inspeção periódica de instalações elétricas prediais.",
        "Diretriz de acessibilidade para projetos arquitetônicos em edifícios públicos.",
        "Requisitos de ventilação mínima em ambientes industriais fechados.",
        "Especificação técnica para controle de qualidade de concreto estrutural.",
        "Boas práticas para gerenciamento de resíduos da construção civil.",
    ]

    metadatas = [
        {"categoria": "seguranca", "codigo": "NR-EPIs"},
        {"categoria": "eletrica", "codigo": "NBR-INSPECAO"},
        {"categoria": "acessibilidade", "codigo": "NBR-9050"},
        {"categoria": "ventilacao", "codigo": "NBR-VENT"},
        {"categoria": "estrutural", "codigo": "NBR-CONCRETO"},
        {"categoria": "ambiental", "codigo": "CONAMA-RCC"},
    ]

    # Usa upsert para inserir ou atualizar registros existentes pelos mesmos ids.
    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

    print("Dados de exemplo inseridos/atualizados com sucesso na coleção 'normas'.")


if __name__ == "__main__":
    seed_example_data()
