import logging
import re
import unicodedata

import pandas as pd

logger = logging.getLogger(__name__)


def _normalizar_texto(valor) -> str:
    """Remove quaisquer acentos do texto"""
    texto = "" if valor is None else str(valor)
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(ch for ch in texto if not unicodedata.combining(ch))
    texto = re.sub(r"\s+", " ", texto.replace("\n", " ").strip().lower())
    return texto


def _buscar_linha_cabecalho_sinapi(caminho) -> int | None:
    """Localizar a linha de início dos dados na planilha SINAPI"""
    bruto = pd.read_excel(caminho, header=None)
    for pos in range(len(bruto)):
        row = bruto.iloc[pos]
        for valor in row.tolist():
            if "descricao do insumo" in _normalizar_texto(valor):
                logger.debug(f'encontrado linha de dados na posição {pos}')
                return pos
    return None


def _preparar_preco_serie(serie):
    """Converter preços BRL para float"""
    if pd.api.types.is_numeric_dtype(serie):
        return pd.to_numeric(serie, errors="coerce")

    texto = serie.astype(str).str.strip()

    # Se vier com vírgula decimal (pt-BR), converte para ponto.
    mask_virgula_decimal = texto.str.contains(",", na=False)
    texto.loc[mask_virgula_decimal] = (
        texto.loc[mask_virgula_decimal]
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )

    return pd.to_numeric(texto, errors="coerce")


def _resolver_colunas_sinapi(tabela, uf_preferida="SP"):
    cols_norm = {col: _normalizar_texto(col) for col in tabela.columns}
    descricao_col = None

    for col, col_norm in cols_norm.items():
        if "descricao do insumo" in col_norm:
            descricao_col = col
            break

    estados_validos = {
        "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT",
        "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"
    }

    uf_col = None
    uf_preferida = (uf_preferida or "SP").upper()

    for col in tabela.columns:
        nome = str(col).strip().upper()
        if nome == uf_preferida:
            uf_col = col
            break

    if not uf_col:
        for col in tabela.columns:
            nome = str(col).strip().upper()
            if nome in estados_validos:
                uf_col = col
                break

    return descricao_col, uf_col


def carregar_sinapi(caminho, uf_preferida="SP"):
    linha_cabecalho = _buscar_linha_cabecalho_sinapi(caminho)

    if linha_cabecalho is None:
        logger.warning(
            "Cabeçalho SINAPI não identificado automaticamente. Usando leitura padrão.")
        tabela = pd.read_excel(caminho)
    else:
        tabela = pd.read_excel(caminho, header=linha_cabecalho)

    tabela = tabela.dropna(how="all").dropna(axis=1, how="all")

    descricao_col, preco_col = _resolver_colunas_sinapi(
        tabela, uf_preferida=uf_preferida)
    tabela.attrs["descricao_col"] = descricao_col
    tabela.attrs["preco_col"] = preco_col
    tabela.attrs["uf_preferida"] = uf_preferida

    logger.info(
        f"SINAPI carregada. Coluna descrição: {descricao_col} | Coluna preço: {preco_col}")
    return tabela


def buscar_preco_sinapi(descricao, tabela):
    if not descricao or tabela is None or tabela.empty:
        return None

    descricao_col = tabela.attrs.get("descricao_col")
    preco_col = tabela.attrs.get("preco_col")

    if not descricao_col or not preco_col:
        descricao_col, preco_col = _resolver_colunas_sinapi(
            tabela,
            uf_preferida=tabela.attrs.get("uf_preferida", "SP")
        )

    if not descricao_col or not preco_col:
        logger.warning(
            "Colunas da SINAPI não identificadas para busca de preços.")
        return None

    alvo = _normalizar_texto(descricao)
    descricoes_norm = tabela[descricao_col].astype(str).map(_normalizar_texto)
    precos_num = _preparar_preco_serie(tabela[preco_col])

    mask_direta = descricoes_norm.str.contains(alvo, na=False)
    candidatos = tabela[mask_direta & precos_num.notna()]

    if not candidatos.empty:
        return float(precos_num.loc[candidatos.index].iloc[0])

    tokens = [t for t in alvo.split() if t not in {
        "de", "da", "do", "e", "para"}]
    if not tokens:
        return None

    mask_tokens = descricoes_norm.map(
        lambda texto: all(tok in texto for tok in tokens))
    candidatos = tabela[mask_tokens & precos_num.notna()]

    if not candidatos.empty:
        return float(precos_num.loc[candidatos.index].iloc[0])

    return None
