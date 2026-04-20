from pathlib import Path
from ezdxf import filemanagement


class LayerTools:
    """
    Gerencia operações de camadas em arquivos DXF.

    Esta classe encapsula a lógica de leitura, criação e validação de 
    camadas usando a biblioteca ezdxf.

    Attributes:
        doc: O objeto de documento ezdxf carregado.
    """

    def __init__(self, doc_path: Path | str):
        """
        Inicializa o LayerTools carregando o arquivo DXF.

        Args:
            doc_path (Path | str): O caminho para o arquivo DXF.
        """
        # Converter para string caso venha como Path, pois alguns métodos preferem str
        self.doc = filemanagement.readfile(str(doc_path))

    def get_layers(self) -> list[str]:
        """
        Get all layer names from the drawing.

        Returns:
            list[str]: A list of all layer names found in the document.
        """
        return [layer.dxf.name for layer in self.doc.layers]

    def check_exists(self, name: str) -> bool:
        """
        Check if a specific layer exists in the drawing.

        Args:
            name (str): The name of the layer to check.

        Returns:
            bool: True if the layer exists, False otherwise.
        """
        return name in self.doc.layers


if __name__ == '__main__':
    # Uso do Path de forma segura
    base_path = Path(__file__).parent.parent
    dxf_file = base_path / 'teste.dxf'

    layer_test = LayerTools(doc_path=dxf_file)

    layers = layer_test.get_layers()
    print(f"Camadas encontradas: {layers}")

    search_name = 'arvore'
    exists = layer_test.check_exists(search_name)
    print(f"A camada '{search_name}' existe? {exists}")
