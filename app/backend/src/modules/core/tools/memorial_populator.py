import openpyxl
from pathlib import Path
import json

class MemorialPopulator:
    """
    Popula o arquivo Excel de memorial com os dados extraídos do DXF.
    Utiliza coordenadas de células baseadas na análise do modelo.
    """
    def __init__(self, template_path: str, output_path: str):
        self.template_path = template_path
        self.output_path = output_path
        if not Path(template_path).exists():
            raise FileNotFoundError(f"Template não encontrado: {template_path}")
        self.wb = openpyxl.load_workbook(template_path)

    def populate_alvenaria(self, summary_data: dict):
        """
        Popula a planilha 'Alvenarias' com comprimentos de paredes.
        summary_data esperado: { "layer_name": { "LINE": {"total_length": 10.5}, ... } }
        """
        ws = self.wb['Alvenarias']
        # No modelo, a descrição costuma começar na coluna B ou C
        # Vamos inserir um resumo nas primeiras linhas livres (ex: a partir da linha 6)
        row = 6
        for layer, data in summary_data.items():
            if 'alv' in layer.lower() or 'parede' in layer.lower() or 'arq' in layer.lower():
                ws.cell(row=row, column=2).value = f"Layer: {layer}"
                total_len = 0
                for etype, metrics in data.items():
                    total_len += metrics.get("total_length", 0)
                ws.cell(row=row, column=6).value = round(total_len, 2) # Coluna de quantidade/medida
                row += 1

    def populate_eletrica(self, synthesis_data: dict):
        """
        Popula a planilha 'Inst Elétricas'.
        synthesis_data: dados processados pelo Surveyor/Spatial Analyst
        """
        ws = self.wb['Inst Elétricas']
        row = 6
        # Exemplo simples de inserção de circuitos
        if "clusters" in synthesis_data:
            for i, cluster in enumerate(synthesis_data["clusters"]):
                ws.cell(row=row + i, column=2).value = f"Circuito {i+1}"
                ws.cell(row=row + i, column=6).value = cluster.get("total_length", 0)
                ws.cell(row=row + i, column=5).value = ", ".join(cluster.get("identifiers", []))

    def save(self):
        self.wb.save(self.output_path)
        print(f"Memorial populado com sucesso em: {self.output_path}")

def run_population(data_json: str, discipline: str, template: str, output: str):
    """
    Função auxiliar para ser chamada como Tool.
    """
    try:
        data = json.loads(data_json)
        pop = MemorialPopulator(template, output)
        if "alvenaria" in discipline.lower():
            pop.populate_alvenaria(data)
        elif "eletrica" in discipline.lower() or "elétrica" in discipline.lower():
            pop.populate_eletrica(data)
        # Adicionar outras disciplinas conforme necessário
        pop.save()
        return f"Sucesso: Dados de {discipline} gravados no Excel."
    except Exception as e:
        return f"Erro na população: {str(e)}"
