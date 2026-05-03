import math
from pathlib import Path
from ezdxf.filemanagement import readfile
from collections import defaultdict
from typing import List, Dict, Any


class EntityDxf:
    """
    Gerencia operações avançadas de extração e análise espacial em arquivos DXF.
    """

    def __init__(self, dxf_file_path: str | Path):
        self.doc = readfile(dxf_file_path)
        self.msp = self.doc.modelspace()
        self.layers = [layer.dxf.name for layer in self.doc.layers]

    def get_layers(self) -> list[str]:
        """
        Retorna a lista de todos os layers existentes no arquivo dxf.
        Return:
            list(str): A lista com os nomes de todos os layers existentes.
        """
        return self.layers

    def check_exists(self, layer_name: str) -> bool:
        """
        Verifica se um nome de layer existe nos layers disponíveis.
        Args:
            layer_name(str): Nome do layer a ser consultado.
        Return:
            bool: verdadeiro se o layer existe, falso caso contrário.
        """
        return layer_name in self.layers

    def get_grouped_entities_summary(self, layers: List[str]) -> Dict[str, Any]:
        """
        Agrupa entidades por layer e tipo, calculando métricas básicas (contagem, comprimento).
        """
        summary = {}
        if not layers:
            return {"error": "Nenhum layer fornecido"}

        for layer in layers:
            try:
                entities = self.msp.query(f'*[layer=="{layer}"]')
            except Exception:
                continue

            layer_data = defaultdict(lambda: {"count": 0, "total_length": 0.0})

            for e in entities:
                etype = e.dxftype()
                layer_data[etype]["count"] += 1

                # Cálculo de comprimento para tipos lineares
                length = 0.0
                if etype == 'LINE':
                    length = math.dist(e.dxf.start, e.dxf.end)
                elif etype == 'LWPOLYLINE':
                    vertices = list(e.get_points(format="xy"))
                    length = sum(
                        math.dist(vertices[i], vertices[i+1]) for i in range(len(vertices)-1))
                elif etype in ('ARC', 'CIRCLE'):
                    # Simplificação para resumo; detalhamento virá em outra função
                    length = e.dxf.radius * \
                        (e.dxf.end_angle - e.dxf.start_angle if etype ==
                         'ARC' else 2 * math.pi)

                layer_data[etype]["total_length"] += length

            summary[layer] = layer_data
        return summary

    def get_detailed_entities(self, layers: List[str], max_entities: int = 100) -> List[Dict[str, Any]]:
        """
        Retorna uma lista detalhada de entidades. Se houver muitas, retorna um resumo para evitar estouro de contexto.
        """
        detailed = []
        for layer in layers:
            entities = self.msp.query(f'*[layer=="{layer}"]')
            count = len(entities)

            # Se houver muitas entidades, processamos apenas as primeiras e avisamos a IA
            processed_entities = entities[:max_entities]
            for e in processed_entities:
                data = {
                    "id": e.dxf.handle,
                    "type": e.dxftype(),
                    "layer": e.dxf.layer,
                }

                if e.dxftype() == 'LINE':
                    data["length"] = math.dist(
                        (e.dxf.start.x, e.dxf.start.y),
                        (e.dxf.end.x, e.dxf.end.y)
                    )
                    data["coords"] = (
                        (e.dxf.start.x, e.dxf.start.y),
                        (e.dxf.end.x, e.dxf.end.y),
                    )

                elif e.dxftype() == 'LWPOLYLINE':
                    data["vertices"] = list(e.get_points(format="xy"))

                elif e.dxftype() == 'INSERT':
                    data["name"] = e.dxf.name
                    data["pos"] = (e.dxf.insert.x, e.dxf.insert.y)

                elif e.dxftype() in ('TEXT', 'MTEXT'):
                    data["text"] = e.plain_text(
                    ) if e.dxftype() == 'MTEXT' else e.dxf.text

                detailed.append(data)

            if count > max_entities:
                detailed.append(
                    {"info": f"Tratados {max_entities} de {count} itens no layer {layer}. O resumo quantitativo já contém o total."})

        return detailed

    def get_connectivity_graph(self, layers: List[str], epsilon: float = 0.1) -> Dict[str, Any]:
        """
        Mapeia a conectividade entre entidades (fios, tubos, paredes) criando um grafo.
        Retorna grupos de entidades conectadas e suas somas totais.
        """
        detailed = self.get_detailed_entities(layers, max_entities=200)
        nodes = []

        # Extrair pontos de conexão
        for ent in detailed:
            if "info" in ent:
                continue
            points = []
            if ent["type"] == 'LINE':
                points = ent["coords"]
            elif ent["type"] == 'LWPOLYLINE':
                points = ent["vertices"]
            elif ent["type"] == 'INSERT':
                points = [ent["pos"]]

            ent["connection_points"] = points
            nodes.append(ent)

        # Algoritmo de busca de componentes conectados (simplificado)
        connections = []
        visited = set()
        clusters = []

        def are_connected(ent1, ent2):
            for p1 in ent1["connection_points"]:
                for p2 in ent2["connection_points"]:
                    if math.dist(p1[:2], p2[:2]) < epsilon:
                        return True
            return False

        for i, ent1 in enumerate(nodes):
            if i in visited:
                continue

            current_cluster = [ent1]
            visited.add(i)

            # Busca em largura para encontrar todos os conectados
            queue = [ent1]
            while queue:
                current = queue.pop(0)
                for j, ent2 in enumerate(nodes):
                    if j not in visited and are_connected(current, ent2):
                        visited.add(j)
                        current_cluster.append(ent2)
                        queue.append(ent2)

            clusters.append(current_cluster)

        # Sintetizar resultados por cluster
        synthesis = []
        for cluster in clusters:
            total_length = sum(e.get("length", 0) for e in cluster)
            # Para polilinhas, calcular comprimento
            for e in cluster:
                if e["type"] == 'LWPOLYLINE':
                    v = e["vertices"]
                    total_length += sum(math.dist(v[k], v[k+1])
                                        for k in range(len(v)-1))

            types = defaultdict(int)
            names = set()
            for e in cluster:
                types[e["type"]] += 1
                if "name" in e:
                    names.add(e["name"])
                if "text" in e:
                    names.add(e["text"])

            synthesis.append({
                "entities_count": len(cluster),
                "total_length": round(total_length, 3),
                "types": dict(types),
                "identifiers": list(names),
                "entities_ids": [e["id"] for e in cluster]
            })

        return {"clusters": synthesis}

    def find_text_near_entities(self, entity_ids: List[str], search_radius: float = 1.0) -> Dict[str, str]:
        """
        Busca textos próximos a determinadas entidades para capturar metadados (ex: bitola, material).
        """
        # Implementação de busca espacial rápida (pode ser otimizada com R-tree se necessário)
        all_texts = []
        for e in self.msp.query('TEXT MTEXT'):
            all_texts.append({
                "text": e.plain_text() if e.dxftype() == 'MTEXT' else e.dxf.text,
                "pos": (e.dxf.insert.x, e.dxf.insert.y)
            })

        results = {}
        for hid in entity_ids:
            ent = self.doc.entitydb.get(hid)
            if not ent:
                continue

            # Posição aproximada da entidade
            pos = (0, 0)
            if ent.dxftype() == 'INSERT':
                pos = (ent.dxf.insert.x, ent.dxf.insert.y)
            elif ent.dxftype() == 'LINE':
                pos = ((ent.dxf.start.x + ent.dxf.end.x)/2,
                       (ent.dxf.start.y + ent.dxf.end.y)/2)
            # ... mais tipos ...

            nearby = [t["text"] for t in all_texts if math.dist(
                pos, t["pos"]) < search_radius]
            if nearby:
                results[hid] = " | ".join(nearby)

        return results
