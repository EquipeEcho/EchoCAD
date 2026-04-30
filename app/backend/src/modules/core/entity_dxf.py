import json
from pathlib import Path
from ezdxf.filemanagement import readfile
from ezdxf.query import EntityQuery
from collections import defaultdict
from deprecated import deprecated


class EntityDxf:
    """
    Gerencia operações de camadas em arquivos DXF.

    Esta classe encapsula a lógica de leitura e validação de 
    camadas usando a biblioteca ezdxf.

    Attributes:
        doc: O objeto de documento ezdxf carregado.
        msp: O modelspace extraído de doc.
    """

    def __init__(self, dxf_file_path: str | Path):
        """
        Inicializa o EntityDxf carregando o arquivo DXF.

        Args:
            dxf_file_path (Path | str): O caminho para o arquivo DXF.
        """
        self.doc = readfile(dxf_file_path)
        self.msp = self.doc.modelspace()
        self.psp = self.doc.layout()

    def get_layers(self) -> list[str]:
        """
        Retorna uma lista de todas as camadas (layers) existentes no arquivo DXF.

        Returns:
            list[str]: Uma lista contendo os nomes das camadas.
        """
        layers = [layer.dxf.name for layer in self.doc.layers]

        return layers

    def check_exists(self, name: str) -> bool:
        """
        Verifica se uma camada específica existe no desenho.

        Args:
            name (str): O nome da camada a ser verificada.

        Returns:
            bool: True se a camada existir, False caso contrário.
        """
        return name in self.doc.layers

    def get_entities_by_layer(self, layer_name: str) -> EntityQuery:
        """
        Recupera todas as entidades gráficas pertencentes a uma camada específica.

        Utiliza o sistema de busca (query) do ezdxf para filtrar elementos como 
        LINE, ARC, TEXT, CIRCLE, entre outros, que estejam atribuídos ao 
        layer informado.

        Args:
            layer_name (str): O nome da camada (layer) a ser filtrada. 
                Nota: O ezdxf geralmente trata nomes de camadas como 
                case-insensitive nesta consulta.

        Returns:
            EntityQuery: Uma coleção (objeto de consulta) contendo todas as 
                entidades encontradas na camada. Se a camada não existir ou 
                estiver vazia, retorna uma consulta vazia.

        Example:
            >>> entities = dxf_handler.get_entities_by_layer("ELE-TOMADAS")
            >>> print(len(entities))
            15
        """
        # A query '*' seleciona todos os tipos de entidades.
        # O filtro [layer=="..."] restringe a busca à camada especificada.
        return self.msp.query(f'*[layer=="{layer_name}"]')

    def get_types_in_layers(self, layers: list[str]) -> str:
        """
        ### Retorna todos as entidades nos layers selecionados.

        Args:
            layers: uma lista com os layers a serem inspecionados.

        Returns:
            str: Um json contendo os layers selecionados e seus entidades com
            suas respectivas contagens.
        """
        tipos_por_layer = defaultdict(lambda: defaultdict(int))
        selected = [e for e in self.msp if e.dxf.layer in layers]
        for e in selected:
            layer = e.dxf.layer
            tipo = e.dxftype()
            tipos_por_layer[layer][tipo] += 1
        return json.dumps(tipos_por_layer)

    @deprecated(reason='Esse método precisa de revisão pois pode retornar texto sujo')
    def get_text_from_layer(self, layer_name: str) -> list[str]:
        """
        Extrai especificamente apenas os conteúdos de texto de uma camada.
        Útil para cruzar com as palavras-chave do agente.
        """
        entities = self.msp.query(f'TEXT MTEXT[layer=="{layer_name}"]')
        return [e.dxf.plain_text() if e.dxftype() == 'MTEXT' else e.dxf.text for e in entities]
