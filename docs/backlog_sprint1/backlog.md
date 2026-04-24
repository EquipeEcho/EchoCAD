# 🏁 Sprint Backlog 1

## User Stories Selecionadas

| Rank | Prioridade | User Story | Estimativa | Sprint |
|-----|------------|------------|------------|--------|
| US01 | Alta | Como usuário, quero enviar um arquivo CAD para que o sistema processe a planta automaticamente. | 5 | 1 |
| US02 | Alta | Como sistema, quero extrair entidades do arquivo CAD para transformar a planta em dados estruturados. | 8 | 1 |
| US03 | Alta | Como sistema, preciso validar o formato dos arquivos CAD enviados para garantir que apenas arquivos suportados sejam processados. | 3 | 1 |
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

### User Story 2 – Geração de Memorial de Cálculo
- **Dado** que o usuário finalizou o upload, **quando** o sistema gerar o memorial, **então** deve ser exibido um memorial simples automático baseado nos dados extraidos do arquivo.   

### User Story 3 – Validação de Formato de Arquivo
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

## 👥 <span id="authors">Autores</span>

<div align="center">
  <table>
    <tr>
      <th>Membro</th>
      <th>Função</th>
      <th>Github</th>
      <th>Linkedin</th>
    </tr>
    <tr>
      <td>Fábio Hiromitsu Nawa</td>
      <td>Scrum Master</td>
      <td><a href="https://github.com/TechSDW"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/f%C3%A1biohnawa/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Rafael Barbosa Candido</td>
      <td>Product Owner</td>
      <td><a href="https://github.com/Rafa2-bit"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/rafael-candido-155705317/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Taylor Henrique Marinho Silva</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/TaylorSilva2"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/taylor-silva-859300330/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Gustavo Felipe Morais</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/gutibrk74"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/gustavo-felipe-morais-a6517b327/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Ryan Araújo dos Santos</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/Ryan53132"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/ryan-araujo-dos-santos-8391b927b/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Nicolas Ferreira Fernandes</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/nicolasffe"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/nicolas-ferreira-fernandes/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Wesley Xavier</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/xvierdev"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/xvierbr/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Luiz Roberto Briz Quirino</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/HerrBriz"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/luiz-briz-15225b303/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Josué da Cunha Olopes</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/jo-olopes"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/josu%C3%A9-da-cunha-olopes-08b493212/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
  </table>
</div>

</div>
