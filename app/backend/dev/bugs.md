# Relatório de Erros e Pontos de Atenção - Backend EchoCAD

Este documento lista os problemas identificados no código que ainda precisam de correção.

## 1. Qualidade de Código

*   **Duplicação de Lógica de Parsing DXF:**
    *   `src/modules/Memorial/dxf_extractor.py` e `src/modules/EspecificacoesTecnicas/dxf_context_extractor.py` ainda implementam o seu próprio `DXFParser` manual, o que deve ser consolidado em um utilitário comum.
    *   **Atenção:** requer análise semântica comparativa das duas estruturas de saída antes de consolidar, para evitar regressões.

---
*Última atualização: 31 de maio de 2026*
