# 🏁 Sprint Backlog 2

## User Stories Selecionadas

| Rank | Prioridade | User Story | Estimativa | Sprint |
|-----|------------|------------|------------|--------|
| US08 | Alta | Como usuário, quero ter uma tela de login e cadastro para acessar minhas análises anteriores. | 5 | 2 |
| US09 | Alta | Como engenheiro, quero classificar elementos CAD para identificar componentes da planta.  | 8 | 2 |
| US10 | Alta | Como engenheiro, quero gerar automaticamente especificações técnicas do projeto. | 5 | 2 |
| US11 | Média | Como engenheiro, quero utilizar um assistente para solicitar geração de documentações específicas sobre a planta CAD | 5 | 2 |
| US12 | Média | Como engenheiro, quero visualizar um dashboard com meus projetos e documentos gerados para acompanhar o progresso das análises. | 3 | 2 |
| US13 | Média | Como engenheiro, quero exportar especificações técnicas em PDF ou DOCX. | 3 | 2 |
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

# 🏆 Definition of Done – Sprint 2

| Critério | Descrição |
|----------|-----------|
| Critérios de Aceitação Atendidos | Todos os cenários de teste da história foram executados e aprovados. |
| Código Revisado | O código foi revisado por pelo menos um colega de equipe. |
| Build/Testes Automatizados| A funcionalidade não quebrou a aplicação e passou nos testes. |
| Validação do PO | O Product Owner validou a entrega com base nos critérios definidos. |

---
## ✔ Critérios de Aceitação – Sprint 2

### User Story 8 – Tela de Login e Cadastro
- **Dado** que o usuário acessou a tela de login, **quando** ele inserir suas credenciais, **então** o sistema deve autenticá-lo e redirecioná-lo para a página principal.
- **Dado** que o usuário acessou a tela de cadastro, **quando** ele preencher o formulário de registro, **então** o sistema deve criar uma nova conta e permitir que ele faça login.

### User Story 9 – Classificação de Elementos CAD
- **Dado** que o sistema recebeu o arquivo CAD, **quando** o sistema processar os dados extraídos, **então** o sistema deve classificar os elementos CAD corretamente para identificar os componentes da planta.  

### User Story 10 – Geração Automática de Especificações Técnicas
- **Dado** que o sistema processou o arquivo CAD, **quando** o sistema gerar as especificações técnicas, **então** as especificações devem ser precisas e detalhadas para garantir a qualidade do projeto técnico.
- **Dado** que o sistema gerou as especificações técnicas, **quando** o usuário revisar as especificações, **então** o usuário deve ser capaz de entender claramente os detalhes técnicos do projeto.

### User Story 11 – Assistente para Geração de Documentações Específicas
- **Dado** que o usuário acessou o assistente, **quando** ele solicitar a geração de um documento específico, **então** o assistente deve processar a solicitação e gerar o documento solicitado com base nos dados extraídos do arquivo CAD. 

### User Story 12 – Dashboard de Projetos e Documentos
- **Dado** que o usuário acessou o dashboard, **quando** ele visualizar seus projetos e documentos, **então** o dashboard deve exibir uma visão geral clara e organizada do progresso das análises.

### User Story 13 – Exportação de Especificações Técnicas
- **Dado** que o usuário gerou as especificações técnicas, **quando** ele solicitar a exportação, **então** o sistema deve permitir que ele baixe as especificações em formato PDF ou DOCX.

---