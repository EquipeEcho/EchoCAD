# Exemplos DXF para o memorial de calculo

Esta pasta contem arquivos `.dxf` preparados para o extrator atual do memorial.

Arquivos gerados:

- `exemplo_memorial_simples.dxf`: cenario pequeno com 3 ambientes.
- `exemplo_memorial_completo.dxf`: cenario maior com 6 ambientes.

Padrao esperado pelo parser:

- Textos dos ambientes no layer `arq - textos`.
- Cada ambiente deve conter nome, area, perimetro e pe-direito.
- A area deve estar no formato `12,00 m2`, usando o caractere sobrescrito em `m²` dentro do DXF.
- O perimetro deve iniciar com `P =`.
- O pe-direito deve iniciar com `PD =`.
- Linhas de parede podem ficar no layer `arq - alvenaria alta`.
- Vaos podem ficar no layer `arq - esquadrias`.

Os DXFs sao gravados em `windows-1252`, que e o encoding usado atualmente pelo parser.

Para regenerar os arquivos:

```powershell
cd app/backend/src/modules/Memorial/examples
python generate_examples.py
```
