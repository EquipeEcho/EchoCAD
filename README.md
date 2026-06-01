# Equipe Echo

## 📌 EchoCAD – Automatização de documentos técnicos

Sistema desenvolvido como parte do projeto do 4º Semestre da **API – Aprendizagem por Projetos Integrados (FATEC – 2026-1º Semestre)**, em parceria com o **Exército - Guarnição de Caçapava**.

O objetivo é desenvolver um site para extrair informações de uma planta CAD e gerar automaticamente uma documentação técnica utilizando inteligência artificial para auxiliar nas etapas necessárias para criação desse documento.

---

## 📖 Sumário

- [Sobre o Projeto](#about)
- [Objetivo do Desafio](#objective)
- [Manuais e Documentação](#documents)
- [Backlog do Produto](#backlog)
- [Cronograma de Sprints](#sprint)
- [Funcionalidades](#functionalities)
- [Requisitos não Funcionais](#requirements)
- [Tecnologias Utilizadas](#tecnologies)
- [Autores](#authors)

---

## 📌 <span id="about">Sobre o Projeto</span>

Este projeto visa criar uma solução capaz de retirar dados de uma planta CAD com precisão, interpretá-los e fornecer ao usuário informações diretas e precisas. Com isso é possivel agilizar a criação de um memorial de cálculo.

---

## 🎯 <span id="objective">Objetivo do Desafio</span>

- Dado um modelo de uma planta CAD inserido pelo usuário, absorver dados relevantes para gerar uma documentação
- Realizar cálculos complexos juntamente com uma IA para verificar a veracidade dos resultados
- Retornar ao consumidor um documento que segue as normas ABNT com informações pertinentes e uma planilha com os gastos necessários
- Desenvolver uma interface direta para que não haja confusão ao navegar pelo site

---

## 📚 <span id="documents">Manuais e Documentação</span>

- 📖 [Manual de Instalação](docs/manual-instalacao.md)  
- 👨‍💻 [Manual do Usuário](docs/Manual%20do%20Usuário%20-%20EchoCAD.pdf)

---

# 📋 <span id="backlog">Backlog do Produto</span>

| Rank | Prioridade | User Story | Estimativa | Sprint |
|-----|------------|------------|------------|--------|
| US01 | Altíssima | Como engenheiro, quero enviar um arquivo CAD para que o sistema processe a planta automaticamente. | 5 | 1 |
| US02 | Altíssima | Como engenheiro, quero exportar o memorial de cálculo em planilha Excel e salvar os dados do memorial no sistema, para facilitar a análise, documentação e armazenamento das informações do projeto | 8 | 1 |
| US03 | Alta | Como engenheiro, preciso que o sistema valide o formato dos arquivos CAD enviados para garantir que apenas arquivos CAD sejam processados. | 3 | 1 |
| US04 | Alta | Como engenheiro, quero que o sistema aplique fórmulas  de engenharia para gerar dados do memorial de cálculo. | 8 | 1 |
| US05 | Alta | Como engenheiro, quero gerar automaticamente um memorial de cálculo estruturado para documentar o projeto técnico. | 5 | 1 |
| US06 | Alta | Como engenheiro, quero uma interface limpa e direta para que eu não fique perdido ao tentar navegar pelo site. | 5 | 1 |
| US07 | Alta | Como engenheiro, quero uma IA dedicada para filtrar os dados extraídos da planta CAD corretamente de acordo com as layers. | 8 | 1 |
| US08 | Alta | Como engenheiro, quero ter uma tela de login e cadastro para acessar minhas análises anteriores. | 5 | 3 |
| US09 | Alta | Como engenheiro, quero preencher um formulário com as informações do projeto e do levantamento de campo para melhor precisão e efetividade na geração dos documentos.  | 8 | 3 |
| US10 | Alta | Como engenheiro, quero gerar automaticamente especificações técnicas do projeto. | 5 | 3 |
| US11 | Alta | Como engenheiro, quero que as especificações técnicas sejam geradas com base nas normas NBR. |5 | 3 |
| US12 | Média | Como engenheiro, quero visualizar um dashboard com meus projetos e documentos gerados para acompanhar o progresso das análises. | 3 | 3 |
| US13 | Média | Como engenheiro, quero exportar especificações técnicas em DOCX. | 3 | 3 |
| US14 | Média |  Como engenheiro, quero acessar um histórico de documentos gerados para consultar análises anteriores. | 3 | 3 |
| US15 | Baixa | Como engenheiro, quero acessar um manual de uso do sistema. | 2 | 3 |
| US16 | Baixa | Como engenheiro, quero um manual de instalação da aplicação para facilitar a implantação. | 2 | 3 |

---
## 🚀 MVP - Mínimo Produto Viável

### 🟢 Sprint 1 - Geração do memorial de cálculo básico - Concluído - <a href="./docs/backlog_sprint1/backlog.md"> Detalhes</a>
[![MVP SPRINT](./docs/img/sprint1_mvp.png)](https://youtu.be/TYSAJDFz9T0?si=gq7HXaN9i9bD9JgZ)



### 🟡 Sprint 2 - Assitente IA e geração de especificações técnicas  - Não Concluído - <a href="./docs/backlog_sprint2/backlog.md"> Detalhes </a>


### 🔵 Sprint 3 - Documentação e exportação de documentos - Concluído - <a href="./docs/backlog_sprint3/backlog.md"> Detalhes </a>

#### Assista o vídeo de apresentação da Sprint
[![VIDEO DA SPRINT](https://img.youtube.com/vi/uGvk_viRp7I/maxresdefault.jpg)](https://www.youtube.com/watch?v=uGvk_viRp7I)

## 🏃‍ DoR - Definition of Ready

- Regras de negócio definidas juntamente com o cliente
- Problema proposto compreendido e discutido com a equipe
- User Stories com Critérios de Aceitação
- Subtarefas divididas a partir das US
- Projeto bem definido e acordado com o cliente
- Arquitetura MVC clara para toda a equipe

## 🏆 DoD - Definition of Done

- Manual do projeto
- Vídeos de cada etapa de entrega
- Documentação informando a funcionalidade implementada
- Descrição de commits que seguem o padrão

## 📅 <span id="sprint">Cronograma de Sprints </span>

| Sprint          |    Período    |
| --------------- | :-----------: |
| 🔖 **SPRINT 1** | 16/03 - 05/04 |
| 🔖 **SPRINT 2** | 13/04 - 03/05 |
| 🔖 **SPRINT 3** | 11/05 - 31/05 |

---

## ⚙️ <span id="functionalities">Funcionalidades</span>

- Extração de dados através da planta CAD
- Filtro das layers da planta utilizando IA
- Cálculos complexos para tratação de dados
- Consultas de preços dos materiais utilizados
- Entrega de resultados em PDF e XLSX

---

## 🔧 <span id="requirements">Requisitos Não Funcionais</span>

- Manual de instalação (no repositório).  
- Manual do usuário

---

## 💻 <span id="tecnologies">Tecnologias</span>

<h4 align="center">
 <a href="https://developer.mozilla.org/pt-BR/docs/Web/JavaScript"><img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"></a>
 <a href="https://www.typescriptlang.org/"><img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white"></a>
 <a href="https://react.dev/"><img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB"></a>
 <a href="https://nodejs.org/"><img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoColor=white"></a>
 <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"></a>
 <a href="https://ollama.com/"><img src="https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white"></a>
 <a href="https://code.visualstudio.com/"><img src="https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white"></a>
 <a href="https://www.atlassian.com/software/jira"><img src="https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=jira&logoColor=white"/></a>
 <a href="https://github.com/"><img src="https://img.shields.io/badge/GitHub-121011?style=for-the-badge&logo=github&logoColor=white"/></a>
 <a href="https://www.mysql.com/"><img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white"/></a>
</h4>

---

## 👥 <span id="authors">Autores</span>

Projeto desenvolvido pelos alunos do **4º semestre de ADS – FATEC SJC (2026-1)** em parceria com o **Exército - Guarnição de Caçapava**.  

<div align="center">
  <table>
    <tr>
      <th>Membro</th>
      <th>Função</th>
      <th>Github</th>
      <th>Linkedin</th>
    </tr>
    <tr>
      <td>Rafael Barbosa Candido</td>
      <td>Product Owner</td>
      <td><a href="https://github.com/Rafa2-bit"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/rafael-candido-155705317/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Fábio Hiromitsu Nawa</td>
      <td>Scrum Master</td>
      <td><a href="https://github.com/TechSDW"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/f%C3%A1biohnawa/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Gustavo Felipe Morais</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/gutibrk74"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/gustavo-felipe-morais-a6517b327/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Luiz Roberto Briz Quirino</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/HerrBriz"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/luiz-briz-15225b303/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Nicolas Ferreira Fernandes</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/nicolasffe"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/nicolas-ferreira-fernandes/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Ryan Araújo dos Santos</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/Ryan53132"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/ryan-araujo-dos-santos-8391b927b/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Taylor Henrique Marinho Silva</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/TaylorSilva2"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/taylor-silva-859300330/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Wesley Xavier</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/xvierdev"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/xvierbr/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
  </table>
</div>
