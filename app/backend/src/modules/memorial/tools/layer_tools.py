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
        self.msp = self.doc.modelspace() # Aqui estão os desenhos

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