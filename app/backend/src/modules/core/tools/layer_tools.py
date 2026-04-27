class LayerTools:
    """
    Gerencia operações de camadas em arquivos DXF.

    Esta classe encapsula a lógica de leitura, criação e validação de 
    camadas usando a biblioteca ezdxf.

    Attributes:
        doc: O objeto de documento ezdxf carregado.
    """

    def __init__(self, entity_dxf):
        """
        Inicializa o LayerTools carregando o arquivo DXF.

        Args:
            doc_path (Path | str): O caminho para o arquivo DXF.
        """
        # Converter para string caso venha como Path, pois alguns métodos preferem str
        self.doc = entity_dxf.doc
        self.msp = self.doc.modelspace()  # Aqui estão os desenhos
        self.names_sorted = sorted(
            [layer.dxf.name for layer in self.doc.layers])
        self.layer_dict = {i: name for i, name in enumerate(self.names_sorted)}

    def get_layers(self) -> dict[int, str]:
        """
        Retorna um dicionário de camadas onde a chave é um índice inteiro
        e o valor é o nome da camada, ordenados alfabeticamente.
        """

        return self.layer_dict

    def get_set_layers(self, indices: set[int]) -> dict[int, str]:
        """
        Filtra o dicionário de camadas para retornar apenas os nomes das camadas associados 
        aos índices numéricos fornecidos.

        Esta ferramenta é útil quando o usuário seleciona camadas específicas por número 
        (ex: após listar todas as camadas) e você precisa recuperar os nomes técnicos 
        delas para realizar cálculos ou leituras no arquivo DXF/CAD.

        Args:
            indices (set[int]): Um conjunto de números inteiros representando as chaves 
                            das camadas desejadas (obtidas anteriormente via get_layers).

        Returns:
            dict[int, str]: Um dicionário contendo apenas os pares {índice: nome_da_camada} 
                            que correspondem aos índices solicitados e existem no documento.
        """
        return {k: self.layer_dict[k] for k in indices if k in self.layer_dict}

    def check_exists(self, name: str) -> bool:
        """
        Check if a specific layer exists in the drawing.

        Args:
            name (str): The name of the layer to check.

        Returns:
            bool: True if the layer exists, False otherwise.
        """
        return name in self.doc.layers

    def get_entities_by_layer(self, layer_name: str):
        """
        Extrai todas as entidades (linhas, textos, etc) de uma camada específica.
        """
        # A query '*' pega tudo, e o filtro [layer=="..."] filtra pela camada.
        # O ezdxf ignora maiúsculas/minúsculas no nome da layer na query.
        return self.msp.query(f'*[layer=="{layer_name}"]')

    def get_text_from_layer(self, layer_name: str) -> list[str]:
        """
        Extrai especificamente apenas os conteúdos de texto de uma camada.
        Útil para cruzar com as palavras-chave do agente.
        """
        entities = self.msp.query(f'TEXT MTEXT[layer=="{layer_name}"]')
        return [e.plain_text() if e.dxftype() == 'MTEXT' else e.dxf.text for e in entities]
