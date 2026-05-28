import json
import math
import ezdxf
from pathlib import Path
from ezdxf.filemanagement import readfile
from ezdxf.lldxf.const import DXFStructureError


# ==============================================================================
# CARREGADOR DINÂMICO DO DICIONÁRIO CONFIG
# ==============================================================================
def carregar_configuracao(nome_arquivo):
    """Carrega o banco de dados de componentes garantindo o caminho correto do script."""
    # Descobre automaticamente a pasta real onde o script Testecomjsonfora.py está salvo
    pasta_do_script = Path(__file__).parent
    caminho_absoluto = pasta_do_script / nome_arquivo

    try:
        with open(caminho_absoluto, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro crítico: Arquivo não encontrado em: {caminho_absoluto}")
        return {}
    except Exception as e:
        print(f"Erro ao carregar configuração: {e}")
        return {}


# ==============================================================================
# FUNÇÕES MATEMÁTICAS AUXILIARES
# ==============================================================================
def calcular_distancia_ponto_linha(ponto, linha_inicio, linha_fim):
    """Calcula a menor distância entre um ponto (X, Y) e um segmento de reta."""
    px, py = ponto[0], ponto[1]
    x1, y1 = linha_inicio[0], linha_inicio[1]
    x2, y2 = linha_fim[0], linha_fim[1]

    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)

    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))

    proj_x = x1 + t * dx
    proj_y = y1 + t * dy

    return math.hypot(px - proj_x, py - proj_y)


def extrair_valor_por_dicionario(texto, dicionario_mapeado, padrao_default=0.0):
    """Varre o texto procurando chaves registradas no dicionário do JSON."""
    for chave, valor in dicionario_mapeado.items():
        if chave.upper() in texto.upper():
            return valor
    return padrao_default


def calcular_area_poligono(vertices):
    """Calcula a área de um polígono usando a fórmula de Gauss (Shoelace)."""
    n = len(vertices)
    if n < 3:
        return 0.0
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    return abs(area) / 2.0


def pontos_proximos(p1, p2, tolerancia=1e-6):
    return abs(p1[0] - p2[0]) <= tolerancia and abs(p1[1] - p2[1]) <= tolerancia


def extrair_xy_vertice(vertice):
    """Normaliza vertices do ezdxf entre Vec3 e tuplas/listas."""
    if hasattr(vertice, "x") and hasattr(vertice, "y"):
        return (vertice.x, vertice.y)
    return (vertice[0], vertice[1])


def extrair_vertices_xy(entidade):
    if hasattr(entidade, "get_points"):
        vertices = entidade.get_points()
    else:
        vertices = entidade.vertices()
    return [extrair_xy_vertice(v) for v in vertices]


def calcular_comprimento_entidade(entidade):
    if entidade.dxftype() == "LINE":
        return math.hypot(
            entidade.dxf.end.x - entidade.dxf.start.x,
            entidade.dxf.end.y - entidade.dxf.start.y,
        )

    vertices = extrair_vertices_xy(entidade)
    comprimento = sum(
        math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        for p1, p2 in zip(vertices, vertices[1:])
    )
    if getattr(entidade, "closed", False) and len(vertices) > 2:
        comprimento += math.hypot(
            vertices[0][0] - vertices[-1][0],
            vertices[0][1] - vertices[-1][1],
        )
    return comprimento


def calcular_area_por_segmentos(segmentos, tolerancia=1e-6):
    """Tenta reconstruir um contorno fechado a partir de segmentos e calcular a área."""
    if len(segmentos) < 3:
        return 0.0

    usados = [False] * len(segmentos)
    inicio, fim = segmentos[0]
    usados[0] = True

    caminho = [inicio, fim]
    atual = fim

    while not pontos_proximos(atual, caminho[0], tolerancia):
        encontrou = False
        for i, (s, e) in enumerate(segmentos):
            if usados[i]:
                continue
            if pontos_proximos(s, atual, tolerancia):
                caminho.append(e)
                atual = e
                usados[i] = True
                encontrou = True
                break
            if pontos_proximos(e, atual, tolerancia):
                caminho.append(s)
                atual = s
                usados[i] = True
                encontrou = True
                break

        if not encontrou:
            return 0.0

        if len(caminho) > len(segmentos) + 2:
            return 0.0

    vertices = caminho[:-1]
    return calcular_area_poligono(vertices)


def estimar_comprimento_bloco(doc, nome_bloco, escala_x=1.0, escala_y=1.0):
    """Estima o comprimento de um bloco pela maior dimensão do seu envelope 2D."""
    try:
        bloco = doc.blocks.get(nome_bloco)
    except Exception:
        return 0.0

    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")
    encontrou = False

    for ent in bloco:
        tipo = ent.dxftype()
        if tipo == "LINE":
            pts = [ent.dxf.start, ent.dxf.end]
            for p in pts:
                min_x = min(min_x, p.x)
                min_y = min(min_y, p.y)
                max_x = max(max_x, p.x)
                max_y = max(max_y, p.y)
                encontrou = True
        elif tipo == "LWPOLYLINE":
            for x, y in extrair_vertices_xy(ent):
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
                encontrou = True

    if not encontrou:
        return 0.0

    dim_x = (max_x - min_x) * abs(escala_x)
    dim_y = (max_y - min_y) * abs(escala_y)
    return max(dim_x, dim_y)


# ==============================================================================
# PARSER PRINCIPAL
# ==============================================================================
def processar_dxf(caminho_arquivo):
    try:
        doc = readfile(caminho_arquivo)
    except IOError:
        return {"erro": f"Não foi possível abrir o arquivo: {caminho_arquivo}"}
    except DXFStructureError:
        return {"erro": f"Arquivo DXF corrompido ou inválido."}

    config = carregar_configuracao("zconfig_sistema.json")

    msp = doc.modelspace()

    dados_paredes = []
    dados_aberturas = []
    dados_eletrica = {}
    dados_encanamento = {}
    dados_escadas = []
    dados_vigas = []
    dados_colunas = []
    dados_laje = []

    laje_tipos = config.get("laje", {}).get("tipos", {})
    esp_laje_padrao = config.get("laje", {}).get("espessura_padrao", 0.12)
    prefixo_laje = config.get("laje", {}).get("prefixo_layer", "LAJE_").upper()
    segmentos_laje_por_layer = {}

    TOLERANCIA = 0.005  # 5 milímetros

    # --------------------------------------------------------------------------
    # PASSO 1: Varrer Entidades Primitivas (LINES e LWPOLYLINES)
    # --------------------------------------------------------------------------
    for entidade in msp.query("LINE LWPOLYLINE"):
        layer = entidade.dxf.layer.upper()

        # Processando Linhas de Fiação Elétrica
        if layer.startswith(config["eletrica"]["prefixo_layer"].upper()):
            bitola = extrair_valor_por_dicionario(
                layer, config["eletrica"]["bitolas_mapeadas"], 2.5
            )
            chave = f"fio_{bitola}mm2"

            comprimento = calcular_comprimento_entidade(entidade)

            dados_eletrica[chave] = dados_eletrica.get(chave, 0.0) + comprimento

        # Processando Linhas de Canos Hidráulicos
        elif layer.startswith(config["hidraulica"]["prefixo_layer"].upper()):
            diametro = extrair_valor_por_dicionario(
                layer, config["hidraulica"]["diametros_mapeados"], 25.0
            )
            chave = f"cano_{int(diametro)}mm"

            comprimento = calcular_comprimento_entidade(entidade)

            dados_encanamento[chave] = dados_encanamento.get(chave, 0.0) + comprimento

        # Processando Linhas de Escada
        elif layer.startswith(config["escada"]["prefixo_layer"].upper()):
            # Fallback seguro por string caso queira manter o cálculo dinâmico da escada via layer
            largura = 1.20
            match_larg = math.trunc(
                extrair_valor_por_dicionario(
                    layer, {"LARG-1-20": 1.20, "LARG-0-90": 0.90}, 1.20
                )
            )

            comp_horizontal = calcular_comprimento_entidade(entidade)

            dados_escadas.append(
                {
                    "comprimento_horizontal_h": round(comp_horizontal, 2),
                    "largura_l": 1.20,  # Valores fixados ou extraídos do padrão anterior
                    "altura_total_v": 3.00,
                    "numero_degraus": 18,
                }
            )

        # Processando Linhas de Paredes cadastrados no JSON
        elif layer in config["paredes"]:
            parede_config = config["paredes"][layer]

            if entidade.dxftype() == "LINE":
                p1 = (entidade.dxf.start.x, entidade.dxf.start.y)
                p2 = (entidade.dxf.end.x, entidade.dxf.end.y)
                segmentos = [(p1, p2)]
            else:
                vertices = extrair_vertices_xy(entidade)
                segmentos = list(zip(vertices, vertices[1:]))
                if getattr(entidade, "closed", False) and len(vertices) > 2:
                    segmentos.append((vertices[-1], vertices[0]))

            for idx, seg in enumerate(segmentos):
                comp_seg = math.hypot(seg[1][0] - seg[0][0], seg[1][1] - seg[0][1])
                dados_paredes.append(
                    {
                        "id_dxf": f"{entidade.dxf.handle}_{idx}",
                        "layer": layer,
                        "inicio": seg[0],
                        "fim": seg[1],
                        "comprimento_m": round(comp_seg, 2),
                        "espessura_m": parede_config["espessura"],
                        "altura_m": parede_config["altura"],
                        "area_externa_m2": round(comp_seg * parede_config["altura"], 2),
                        "volume_bruto_m3": round(
                            comp_seg
                            * parede_config["altura"]
                            * parede_config["espessura"],
                            3,
                        ),
                        "descontos_aberturas": [],
                        "volume_liquido_m3": 0.0,
                    }
                )

        # Processando Linhas de Vigas cadastradas no JSON
        elif layer in config.get("vigas", {}):
            viga_config = config["vigas"][layer]

            if entidade.dxftype() == "LINE":
                p1 = (entidade.dxf.start.x, entidade.dxf.start.y)
                p2 = (entidade.dxf.end.x, entidade.dxf.end.y)
                segmentos = [(p1, p2)]
            else:
                vertices = extrair_vertices_xy(entidade)
                segmentos = list(zip(vertices, vertices[1:]))
                if getattr(entidade, "closed", False) and len(vertices) > 2:
                    segmentos.append((vertices[-1], vertices[0]))

            for idx, seg in enumerate(segmentos):
                comp_seg = math.hypot(seg[1][0] - seg[0][0], seg[1][1] - seg[0][1])
                dados_vigas.append(
                    {
                        "id_dxf": f"{entidade.dxf.handle}_{idx}",
                        "layer": layer,
                        "inicio": seg[0],
                        "fim": seg[1],
                        "comprimento_m": round(comp_seg, 2),
                        "base_m": viga_config["base_m"],
                        "altura_m": viga_config["altura_m"],
                        "volume_m3": round(
                            comp_seg * viga_config["base_m"] * viga_config["altura_m"],
                            3,
                        ),
                        "colunas_associadas": [],
                    }
                )

        # Processando Lajes desenhadas por linhas/polilinhas em layers LAJE_*
        elif layer in laje_tipos or layer.startswith(prefixo_laje):
            laje_config = laje_tipos.get(layer, {"espessura_m": esp_laje_padrao})
            espessura = laje_config.get("espessura_m", esp_laje_padrao)

            if entidade.dxftype() == "LWPOLYLINE":
                vertices = extrair_vertices_xy(entidade)
                if len(vertices) >= 3:
                    if not entidade.closed and vertices[0] != vertices[-1]:
                        vertices.append(vertices[0])
                    area = calcular_area_poligono(vertices)
                    if area > 0:
                        dados_laje.append(
                            {
                                "layer": layer,
                                "origem": "LWPOLYLINE",
                                "area_m2": round(area, 3),
                                "espessura_m": espessura,
                                "volume_m3": round(area * espessura, 3),
                            }
                        )
            else:
                p1 = (entidade.dxf.start.x, entidade.dxf.start.y)
                p2 = (entidade.dxf.end.x, entidade.dxf.end.y)
                segmentos_laje_por_layer.setdefault(layer, []).append((p1, p2))

    # --------------------------------------------------------------------------
    # PASSO 1B: Varrer Entidades HATCH - Lajes
    # --------------------------------------------------------------------------
    for entidade in msp.query("HATCH"):
        layer = entidade.dxf.layer.upper()
        laje_config = laje_tipos.get(layer)
        if not laje_config and layer.startswith(prefixo_laje):
            laje_config = {"espessura_m": esp_laje_padrao}

        if laje_config:
            area_total = 0.0
            for path in entidade.paths:
                if hasattr(path, "vertices") and path.vertices:
                    verts = [(v[0], v[1]) for v in path.vertices]
                    area_total += calcular_area_poligono(verts)
            espessura = laje_config.get("espessura_m", esp_laje_padrao)
            dados_laje.append(
                {
                    "layer": layer,
                    "area_m2": round(area_total, 3),
                    "espessura_m": espessura,
                    "volume_m3": round(area_total * espessura, 3),
                }
            )

    # --------------------------------------------------------------------------
    # PASSO 1C: Reconstruir área de laje a partir de segmentos LINE
    # --------------------------------------------------------------------------
    for layer, segmentos in segmentos_laje_por_layer.items():
        laje_config = laje_tipos.get(layer, {"espessura_m": esp_laje_padrao})
        espessura = laje_config.get("espessura_m", esp_laje_padrao)
        area = calcular_area_por_segmentos(segmentos)
        if area > 0:
            dados_laje.append(
                {
                    "layer": layer,
                    "origem": "LINE",
                    "area_m2": round(area, 3),
                    "espessura_m": espessura,
                    "volume_m3": round(area * espessura, 3),
                }
            )

    # --------------------------------------------------------------------------
    # PASSO 2: Varrer Blocos (INSERT) - CRUZANDO DIRETO COM O CONFIG JSON
    # --------------------------------------------------------------------------
    for bloco in msp.query("INSERT"):
        nome_bloco = bloco.dxf.name.upper()
        layer_bloco = bloco.dxf.layer.upper()
        abertura_mapeada = None
        tipo_identificado = ""

        # Varre o banco de dados do JSON procurando se o nome do bloco contém a chave
        for chave, dados in config["aberturas"].items():
            if chave.upper() in nome_bloco:
                abertura_mapeada = dados
                tipo_identificado = chave
                break

        if abertura_mapeada:
            dados_aberturas.append(
                {
                    "categoria": abertura_mapeada["categoria"],
                    "tipo": tipo_identificado,
                    "coordenada": (bloco.dxf.insert.x, bloco.dxf.insert.y),
                    "largura": abertura_mapeada["largura"],
                    "altura": abertura_mapeada["altura"],
                }
            )

        # Varre vigas por nome do bloco e, como fallback, por nome da layer
        viga_mapeada = None
        tipo_viga = ""
        for chave, dados in config.get("vigas", {}).items():
            chave_upper = chave.upper()
            if chave_upper in nome_bloco or chave_upper in layer_bloco:
                viga_mapeada = dados
                tipo_viga = chave
                break

        if viga_mapeada:
            comprimento_estimado = estimar_comprimento_bloco(
                doc,
                bloco.dxf.name,
                getattr(bloco.dxf, "xscale", 1.0),
                getattr(bloco.dxf, "yscale", 1.0),
            )
            dados_vigas.append(
                {
                    "id_dxf": f"{bloco.dxf.handle}_ins",
                    "layer": layer_bloco,
                    "tipo": tipo_viga,
                    "origem": "INSERT",
                    "coordenada": (bloco.dxf.insert.x, bloco.dxf.insert.y),
                    "comprimento_m": round(comprimento_estimado, 2),
                    "base_m": viga_mapeada["base_m"],
                    "altura_m": viga_mapeada["altura_m"],
                    "volume_m3": round(
                        comprimento_estimado
                        * viga_mapeada["base_m"]
                        * viga_mapeada["altura_m"],
                        3,
                    ),
                    "colunas_associadas": [],
                }
            )

        # Varre o banco de dados procurando colunas (mesma lógica das aberturas)
        coluna_mapeada = None
        tipo_coluna = ""
        for chave, dados in config.get("colunas", {}).items():
            if chave.upper() in nome_bloco:
                coluna_mapeada = dados
                tipo_coluna = chave
                break

        if coluna_mapeada:
            dados_colunas.append(
                {
                    "tipo": tipo_coluna,
                    "coordenada": (bloco.dxf.insert.x, bloco.dxf.insert.y),
                    "largura_m": coluna_mapeada["largura_m"],
                    "profundidade_m": coluna_mapeada["profundidade_m"],
                    "altura_m": coluna_mapeada["altura_m"],
                    "volume_m3": round(
                        coluna_mapeada["largura_m"]
                        * coluna_mapeada["profundidade_m"]
                        * coluna_mapeada["altura_m"],
                        3,
                    ),
                }
            )

    # --------------------------------------------------------------------------
    # PASSO 3: Interseção Espacial (Vínculo de Proximidade Zero)
    # --------------------------------------------------------------------------
    for abertura in dados_aberturas:
        ponto_abertura = abertura["coordenada"]

        for parede in dados_paredes:
            distancia = calcular_distancia_ponto_linha(
                ponto_abertura, parede["inicio"], parede["fim"]
            )

            if distancia <= TOLERANCIA:
                vol_desconto = round(
                    abertura["largura"] * abertura["altura"] * parede["espessura_m"], 3
                )
                parede["descontos_aberturas"].append(
                    {
                        "tipo": abertura["categoria"],
                        "especificacao": abertura["tipo"],
                        "volume_descontado_m3": vol_desconto,
                    }
                )
                break

    # Cruzamento Colunas x Vigas (mesma lógica de aberturas x paredes)
    for coluna in dados_colunas:
        ponto_coluna = coluna["coordenada"]
        for viga in dados_vigas:
            if "inicio" not in viga or "fim" not in viga:
                continue
            distancia = calcular_distancia_ponto_linha(
                ponto_coluna, viga["inicio"], viga["fim"]
            )
            if distancia <= TOLERANCIA:
                viga["colunas_associadas"].append(coluna["tipo"])
                break

    # --------------------------------------------------------------------------
    # PASSO 4: Consolidação dos Relatórios
    # --------------------------------------------------------------------------
    total_volume_liquido_paredes = 0.0
    total_portas = 0
    total_janelas = 0
    volume_total_descontado_aberturas = 0.0

    for parede in dados_paredes:
        total_descontos = sum(
            ab["volume_descontado_m3"] for ab in parede["descontos_aberturas"]
        )
        parede["volume_liquido_m3"] = round(
            parede["volume_bruto_m3"] - total_descontos, 3
        )

        total_volume_liquido_paredes += parede["volume_liquido_m3"]
        volume_total_descontado_aberturas += total_descontos
        for ab in parede["descontos_aberturas"]:
            if ab["tipo"] == "porta":
                total_portas += 1
            if ab["tipo"] == "janela":
                total_janelas += 1

    processamento_escadas = []
    total_concreto_escadas = 0.0
    esp_laje_escada = config["escada"].get("espessura_laje_fundo_padrao", 0.12)

    for esc in dados_escadas:
        h = esc["comprimento_horizontal_h"]
        v = esc["altura_total_v"]
        l = esc["largura_l"]
        n = esc["numero_degraus"]

        espelho = v / n
        piso = h / n
        rampa = math.sqrt(h**2 + v**2)

        vol_degraus = n * ((piso * espelho) / 2) * l
        vol_laje = rampa * l * esp_laje_escada
        vol_escada_total = round(vol_degraus + vol_laje, 3)
        total_concreto_escadas += vol_escada_total

        processamento_escadas.append(
            {
                "largura_m": l,
                "altura_total_m": v,
                "degraus": n,
                "volume_concreto_m3": vol_escada_total,
            }
        )

    for p in dados_paredes:
        p.pop("inicio")
        p.pop("fim")

    for v in dados_vigas:
        v.pop("inicio", None)
        v.pop("fim", None)

    total_volume_vigas = round(sum(v["volume_m3"] for v in dados_vigas), 3)
    total_volume_colunas = round(sum(c["volume_m3"] for c in dados_colunas), 3)
    total_area_laje = round(sum(l["area_m2"] for l in dados_laje), 3)
    total_volume_laje = round(sum(l["volume_m3"] for l in dados_laje), 3)

    return {
        "paredes": dados_paredes,
        "vigas": dados_vigas,
        "colunas": dados_colunas,
        "laje": dados_laje,
        "infraestrutura": {
            "eletrica": [
                {"tipo": k, "comprimento_m": round(v, 2)}
                for k, v in dados_eletrica.items()
            ],
            "hidraulica": [
                {"tipo": k, "comprimento_m": round(v, 2)}
                for k, v in dados_encanamento.items()
            ],
        },
        "escadas": processamento_escadas,
        "resumo_global": {
            "quantidade_total_portas": total_portas,
            "quantidade_total_janelas": total_janelas,
            "volume_total_descontado_vãos_m3": round(
                volume_total_descontado_aberturas, 3
            ),
            "volume_final_liquido_alvenaria_m3": round(total_volume_liquido_paredes, 3),
            "volume_total_concreto_escadas_m3": round(total_concreto_escadas, 3),
            "quantidade_total_colunas": len(dados_colunas),
            "volume_total_vigas_m3": total_volume_vigas,
            "volume_total_colunas_m3": total_volume_colunas,
            "area_total_laje_m2": total_area_laje,
            "volume_total_laje_m3": total_volume_laje,
            "comprimento_total_fios_m": round(sum(dados_eletrica.values()), 2),
            "comprimento_total_canos_m": round(sum(dados_encanamento.values()), 2),
        },
    }


# ==============================================================================
# EXECUÇÃO DO PROGRAMA
# ==============================================================================

# 1. Carrega as configurações do dicionário JSON externo
if __name__ == "__main__":
    from pathlib import Path
    import os

    print("Diretório atual:", os.getcwd())
    print("Arquivos na pasta:", os.listdir())
    print("Arquivo existe?", Path("Teste.dxf").exists())

    resultado = processar_dxf(
        r"C:\Users\ADS_DSM\.projects\EchoCAD\app\backend\src\modules\core\build\Teste.dxf"
    )

    print(json.dumps(resultado, indent=4, ensure_ascii=False))
