# EchoCAD

## 📌 EchoCAD – Automatização de documentos técnicos

Sistema desenvolvido como parte do projeto **API – Aprendizagem por Projetos Integrados (FATEC – 2026-1º Semestre)**, em parceria com o **Exército - Guarnição de Caçapava**.

O objetivo é desenvolver um site para extrair informações de uma planta CAD e gerar automaticamente uma documentação técnica utilizando uma inteligência artificial para garantir a precisão dos dados obtidos.

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

Este projeto visa criar uma solução capaz de retirar dados de qualquer tipo de documento com precisão, interpretá-los e fornecer ao usuário informações diretas e precisas.

---

## 🎯 <span id="objective">Objetivo do Desafio</span>

- Dado um modelo qualquer inserido pelo usuário, absorver dados relevantes para uma documentação
- Realizar cálculos complexos juntamente com uma IA para verificar a veracidade dos resultados
- Retornar ao consumidor um documento que segue as normas ABNT com todas informações necessárias para que possa dar continuidade ao seu projeto

---

## 📚 <span id="documents">Manuais e Documentação</span>

- 📖 [Manual de Instalação](docs/manual-instalacao.md)  
- 👨‍💻 [Manual do Usuário](docs/manual-usuario.md)
- 🖥️ [Manual do Desenvolvedor](https://docs.google.com/document/d/16Qun6kh2kjLRQpp6ShXNLXjaFmUmkUgfRqPLsjNbvSs/edit?usp=sharing)
- 🔌 [Documentação da API](docs/api.md)  

---

# 📋 <span id="backlog">Backlog do Produto</span>

| Rank | Prioridade | User Story | Estimativa | Sprint |
|-----|------------|------------|------------|--------|
| US01 | Alta | Como usuário, quero enviar um arquivo CAD para que o sistema processe a planta automaticamente. | 5 | 1 |
| US02 | Alta | Como sistema, quero extrair entidades do arquivo CAD para transformar a planta em dados estruturados. | 8 | 1 |
| US03 | Alta | Como sistema, preciso validar o formato dos arquivos CAD enviados para garantir que apenas arquivos suportados sejam processados. | 3 | 1 |
| US04 | Alta | Como usuário, quero que o sistema aplique fórmulas  de engenharia para gerar dados do memorial de cálculo. | 8 | 1 |
| US05 | Alta | Como usuário, quero gerar automaticamente um memorial de cálculo estruturado para documentar o projeto técnico. | 5 | 1 |
| US06 | Alta | Como sistema quero classificar elementos CAD para identificar componentes da planta.  | 8 | 2 |
| US07 | Alta | Como usuário, quero gerar automaticamente especificações técnicas do projeto. | 5 | 2 |
| US08 | Média | Como usuário, quero utilizar um assistente baseado em IA para solicitar geração de documentos via linguagem natural. | 5 | 2 |
| US09 | Média | Como sistema, quero armazenar dados do projeto em banco relacional normalizado para garantir integridade e consulta eficiente. | 3 | 2 |
| US10 | Média | Como usuário, quero visualizar um dashboard com meus projetos e documentos gerados para acompanhar o progresso das análises. | 3 | 3 |
| US11 | Média | Como usuário, quero exportar documentos tecnicos em PDF ou DOCX. | 3 | 3 |
| US12 | Média |  Como usuário, quero acessar um histórico de documentos gerados para consultar análises anteriores. | 3 | 3 |
| US13 | Baixa | Como usuário, quero acessar um manual de uso do sistema. | 2 | 3 |
| US14 | Baixa | Como usuário, quero um manual de instalação da aplicação para facilitar a implantação. | 2 | 3 |

---
## 🚀 MVP - Mínimo Produto Viável

### 🟢 Sprint 1 - Questionário Geral - Em andamento
[![MVP SPRINT 1]()

### 📈 Backlog da Sprint 1 - [Detalhes](./docs/Sprint-1/sprint1.backlog.md)
| Rank | Prioridade | User Story                                                               | Estimativa |
| ---- | ---------- | ------------------------------------------------------------------------ | ---------- |


### 🟡 Sprint 2 - Geração de Diagnósticos Personalizados - Não iniciada
[![MVP SPRINT 2]()


### 📈 Backlog da Sprint 2- [Detalhes](./docs/Sprint-2/sprint2.backlog.md)
| Rank | Prioridade | User Story                                               | Estimativa |
| ---- | ---------- | -------------------------------------------------------- | ---------- |


### 🔵 Sprint 3 - Dashboard do Cliente - Não iniciada
[![MVP SPRINT 3]()

### 📈 Backlog da Sprint 3 - [Detalhes](./docs/Sprint-3/sprint3.backlog.md)
| Rank | Prioridade | User Story                                                                                      | Estimativa |
| ---- | ---------- | ----------------------------------------------------------------------------------------------- | ---------- |


## 🏃‍ DoR - Definition of Ready

- Problema proposto compreendido e discutido com a equipe
- User Stories com Critérios de Aceitação
- Subtarefas divididas a partir das US
- Projeto bem definido e acordado com o cliente
- Arquitetura MVC clara para toda a equipe
- Commits que seguem um modelo padrão

## 🏆 DoD - Definition of Done

- Manual do projeto
- Vídeos de cada etapa de entrega

## 📅 <span id="sprint">Cronograma de Sprints </span>

| Sprint          |    Período    |
| --------------- | :-----------: |
| 🔖 **SPRINT 1** | 16/03 - 05/04 |
| 🔖 **SPRINT 2** | 13/04 - 03/05 |
| 🔖 **SPRINT 3** | 11/05 - 31/05 |

---

## ⚙️ <span id="functionalities">Funcionalidades</span>

- Extração de dados através da planta CAD
- Cálculos complexos para tratação de dados
- Garantia de precisão com IA
- Entrega de resultados em PDF

---

## 🔧 <span id="requirements">Requisitos Não Funcionais</span>

- Manual de instalação (no repositório).  
- Manual do usuário
- Documentação técnica para desenvolvedores
- Documentação da API.

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
</h4>

---

## 👥 <span id="authors">Autores</span>

Projeto desenvolvido pelos alunos do **4º semestre de ADS – FATEC SJC (2025-2)** em parceria com o **Exército - Guarnição de Caçapava**.  

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
