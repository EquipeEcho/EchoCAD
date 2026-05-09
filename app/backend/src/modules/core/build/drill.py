import math
from ezdxf.entities.lwpolyline import LWPolyline
from ezdxf.filemanagement import readfile
from ezdxf.math import Vec2
from pathlib import Path
import networkx as nx

root = Path(__file__).parent

file = readfile(root / 'circuit.dxf')

msp = file.modelspace()
psp = file.paperspace()

layers = [layer.dxf.name for layer in file.layers]

entities = list(msp)
for entity in entities:
    print(entity.dxftype())


def build_conn_gaph(msp):
    G = nx.Graph()
    for line in msp.query('LINE'):
        p1 = Vec2(line.dxf.start)
        p2 = Vec2(line.dxf.end)
        if (p1 == p2):
            continue
        G.add_edge(
            p1,
            p2,
            handle=line.dxf.handle,
            layer=line.dxf.layer,
            length=p1.distance(p2)
        )
    return G


graph = build_conn_gaph(msp)

def get_connected_lines(G, target_handle):
    connected = []
    # Procuramos a aresta que tem esse handle
    for u, v, data in G.edges(data=True):
        if data['handle'] == target_handle:
            # Pegamos todas as outras arestas que tocam os nós u ou v
            for neighbor in G.edges(u, data=True):
                if neighbor[2]['handle'] != target_handle:
                    connected.append(neighbor[2]['handle'])
            for neighbor in G.edges(v, data=True):
                if neighbor[2]['handle'] != target_handle:
                    connected.append(neighbor[2]['handle'])
    return list(set(connected))

print(get_connected_lines(graph, 'A'))


pontas_soltas = [node for node, degree in graph.degree() if degree == 1]

for pto in pontas_soltas:
    print(f"Atenção: Possível erro de fechamento no ponto {pto}")


# Separa o desenho em listas de grupos conectados
subgrafos = [graph.subgraph(c).copy() for c in nx.connected_components(graph)]

print(f"O sistema detectou {len(subgrafos)} grupos de objetos independentes.")

for i, sub in enumerate(subgrafos):
    # Aqui você aplica a lógica da resposta anterior:
    # Se sub tem muitos ciclos -> Provavelmente Vista Superior
    # Se sub é muito largo e baixo -> Provavelmente Vista Frontal
    print(f"Grupo {i} tem {sub.number_of_edges()} linhas.")



def calcular_perimetro_ciclo(G, ciclo):
    perimetro = 0
    # O ciclo é uma lista de nós [(x1,y1), (x2,y2)...]
    for i in range(len(ciclo)):
        u = ciclo[i]
        v = ciclo[(i + 1) % len(ciclo)] # Fecha o laço voltando ao início
        # Pegamos o comprimento guardado na aresta do grafo
        perimetro += G[u][v]['length']
    return perimetro

print(calcular_perimetro_ciclo(graph, nx.cycle_basis(graph)[0]))

for circle in msp.query('CIRCLE'):
    center = Vec2(circle.dxf.center)
    radius = circle.dxf.radius
    area = math.pi * radius ** 2
    print(f"Círculo encontrado: Centro={center}, Raio={radius}, Área={area}")

for pline in msp.query('LWPOLYLINE'):
    x = type(pline)
    pontos = pline.get_points() # type: ignore
        
    for idx, p in enumerate(pontos):
        x, y = p[0], p[1] # Pegamos apenas os dois primeiros valores
        print(f"Vértice {idx}: X={x:.4f}, Y={y:.4f}")


# for entity in msp.query('*[layer==\'0\']'):
#     print(entity.dxftype())
#     if entity.dxftype() == 'LINE':
#         p1 = Vec2(entity.dxf.start)
#         p2 = Vec2(entity.dxf.end)
#         dist = p1.distance(p2)
#         ltype = entity.dxf.linetype
#         cor = entity.dxf.color
#         layer_color = file.layers.get(entity.dxf.layer).get_color()
