# 🏁 Sprint Backlog 1

## User Stories Selecionadas

| Rank | Prioridade | User Story | Estimativa | Sprint |
|-----|------------|------------|------------|--------|
| US01 | Alta | Como usuário, quero enviar um arquivo CAD para que o sistema processe a planta automaticamente. | 5 | 1 |
| US02 | Alta | Como engenheiro, quero exportar o memorial de cálculo em planilha Excel e salvar os dados do memorial no sistema, para facilitar a análise, documentação e armazenamento das informações do projeto | 8 | 1 |
| US03 | Alta | Como engenheiro, preciso que o sistema valide o formato dos arquivos CAD enviados para garantir que apenas arquivos CAD sejam processados. | 3 | 1 |
| US04 | Alta | Como usuário, quero que o sistema aplique fórmulas  de engenharia para gerar dados do memorial de cálculo. | 8 | 1 |
| US05 | Alta | Como usuário, quero gerar automaticamente um memorial de cálculo estruturado para documentar o projeto técnico. | 5 | 1 |
| US06 | Alta | Como consumidor, quero uma interface limpa e direta para que eu não fique perdido ao tentar navegar pelo site. | 5 | 1 |
| US07 | Alta | Como cliente, quero uma IA dedicada para filtrar os dados extraídos da planta CAD corretamente de acordo com as layers. | 8 | 1 |
---

# 🏃 DoR - Definition of Ready

| Critério | Descrição |
|----------|-----------|
| Clareza na Descrição | A User Story está escrita no formato “Como [persona], quero [ação] para que [objetivo]”. |
| Critérios de Aceitação Definidos | A história possui objetivos claros que indicam o que é necessário para considerá-la concluída. |
| Cenários de Teste Especificados | A história tem pelo menos 1 cenário de teste estruturado (Dado, Quando, Então). |
| Independente | A história pode ser implementada sem depender de outra tarefa da mesma Sprint. |
| Compreensão Compartilhada | Toda a equipe (incluindo PO e devs) compreende o propósito da história. |
| Estimável | A história possui uma estimativa clara definida no planejamento. |

# 🏆 Definition of Done – Sprint 1

| Critério | Descrição |
|----------|-----------|
| Critérios de Aceitação Atendidos | Todos os cenários de teste da história foram executados e aprovados. |
| Código Revisado | O código foi revisado por pelo menos um colega de equipe. |
| Build/Testes Automatizados| A funcionalidade não quebrou a aplicação e passou nos testes. |
| Validação do PO | O Product Owner validou a entrega com base nos critérios definidos. |

---
## ✔ Critérios de Aceitação – Sprint 1

### User Story 1 – Upload de Arquivo CAD
- **Dado** que o usuário acessa a tela inicial, **quando** ele fizer o upload do arquivo CAD, **então** o sistema deve processar o arquivo e extrair as entidades para gerar dados estruturados.    

### User Story 2 – Exportação de Memorial de Cálculo e Armazenamento de Dados
- **Dado** que o usuário gerou o memorial de cálculo, **quando** ele solicitar a exportação, **então** o sistema deve permitir que ele baixe o memorial em formato Excel e deve armazenar os dados do memorial no sistema para futuras consultas e análises.   

### User Story 3 – Validação de Formato de Arquivo CAD
- **Dado** que os arquivos CAD forem enviados, **quando** o usuário fizer o upload do arquivo, **então** o sistema deve validar se o formato enviado é em .DXF.  

### User Story 4 – Aplicação de Fórmulas de Engenharia
- **Dado** o sistema obtiver os dados extraidos de cada layer, **quando** o sistema processar o arquivo CAD antes de gerar o memorial, **então** deve aplicar formulas de engenharia padrão para a melhor precisão dos cálculos.   

### User Story 5 – Geração Automática de Memorial de Cálculo
- **Dado** que o sistema processou o arquivo CAD, **quando** o memorial for gerado, **então** o memorial deve ser estruturado de forma clara e organizada para facilitar a compreensão do projeto técnico. 

### User Story 6 – Interface Limpa e Direta
- **Dado** que o usuário acessa a interface do sistema, **quando** ele navegar pelo site, **então** a interface deve ser limpa e direta, com uma navegação intuitiva para que o usuário não fique perdido.

### User Story 7 – IA para Filtrar Dados por Layers
- **Dado** que o sistema extraiu os dados do arquivo CAD, **quando** o sistema processar os dados, **então** a IA deve filtrar os dados corretamente de acordo com as layers para garantir a precisão dos dados extraídos.

---