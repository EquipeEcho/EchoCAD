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

    def get_layers(self) -> list[str]:
        """
        Returns a list of all existing layers in the DXF file.

        Returns:
            list[str]: A list containing the names of the layers.
        """

        layers = [layer.dxf.name for layer in self.doc.layers]

        return layers

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
