# 4ADS

## 📌 4ADS – Automatização de documentos técnicos

Sistema desenvolvido como parte do projeto **API – Aprendizagem por Projetos Integrados (FATEC – 2026-1)**, em parceria com o **Exército - Guarnição de Caçapava**.

O objetivo é desenvolver um site para extrair informações de uma planta CAD e gerar automaticamente uma documentação técnica utilizando uma inteligência artificial para garantir a precisão dos dados obtidos.

---

## 📖 Sumário

- [Sobre o Projeto](#about)
- [Objetivo do Desafio](#objetivo-do-desafio)
- [Backlog do Produto](#backlog-do-produto)
- [Cronograma de Sprints](#sprint)
- [Funcionalidades](#funcionalidades)
- [Requisitos não Funcionais](#requisitos-não-funcionais)
- [Tecnologias Utilizadas](#tecnologias)
- [Manuais e Documentação](#manuais-e-docs)
- [Autores](#authors)

---

## 📌 <span id="about">Sobre o Projeto</span>

Este projeto visa criar uma solução capaz de retirar dados de qualquer documento com precisão, interpretá-los e fornecer ao usuário informações diretas e precisas.

---

## 🎯 <span id="objetivo-do-desafio">Objetivo do Desafio</span>

- Dado um modelo qualquer inserido pelo usuário, absorver dados relevantes para uma documentação
- Realizar cálculos complexos juntamente com uma IA para verificar a veracidade dos resultados
- Retornar ao consumidor um documento com todas informações necessárias para que possa dar continuidade ao seu projeto

---

## <span id="tutorial">Tutorial de Instalação</span>

---

# 📋 Backlog do Produto
| Rank | Prioridade | User Story | Estimativa | Sprint |
| ---- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------ |
| 1    | Alta       | Como usuário, quero fazer upload de uma planta CAD para que o sistema possa iniciar a análise técnica do arquivo.                       | 5          | 1      |
| 2    | Alta       | Como usuário, quero visualizar uma lista das plantas enviadas para acompanhar o status do processamento.                                | 3          | 1      |
| 3    | Alta       | Como sistema, preciso validar o formato dos arquivos CAD enviados para garantir que apenas arquivos suportados sejam processados.       | 3          | 1      |
| 4    | Alta       | Como sistema, preciso extrair dados estruturais da planta CAD para permitir análise automática das informações.                         | 8          | 1      |
| 5    | Média       | Como usuário, quero gerar especificações técnicas automaticamente para documentar os detalhes do projeto. | 5          | 2      |
| 6    | Média       | Como usuário, quero visualizar os dados técnicos extraídos da planta antes da geração do documento para validar as informações.             | 5          | 2      |
| 7    | Alta       | Como usuário, quero gerar automaticamente um memorial de cálculo baseado nos dados extraídos da planta.          | 5         | 2      |
| 8    | Média       | Como usuário, quero exportar a documentação gerada em formato PDF para utilização em relatórios e processos técnicos.      | 3          | 3      |
| 9   | Média       |  Como usuário, quero acessar um histórico de documentos gerados para consultar análises anteriores.                               | 3          | 3      |
| 10   | Média      | Como usuário, quero visualizar um dashboard com meus projetos e documentos gerados para acompanhar o progresso das análises.                  | 3          | 3      |

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

## 🏆 DoD - Definition of Done

- Manual do projeto
- Vídeos de cada etapa de entrega

## 📅 <span id="sprint">Cronograma de Sprints </span>

| Sprint          |    Período    |
| --------------- | :-----------: |
| 🔖 **SPRINT 1** | 16/03 - 05/01 |
| 🔖 **SPRINT 2** | 13/04 - 03/05 |
| 🔖 **SPRINT 3** | 11/05 - 31/05 |

---

## ⚙️ <span id="funcionalidades">Funcionalidades</span>

- Extração de dados através da planta CAD
- Cálculos complexos para tratação de dados
- Garantia de precisão com IA
- Entrega de resultados em PDF

---

## 🔧 <span id="requisitos-não-funcionais">Requisitos Não Funcionais</span>

- Manual de instalação (no repositório).  
- Manual do usuário (no repositório).  
- Documentação da API.  

---

## 💻 <span id="tecnologias">Tecnologias</span>

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

## 📚 <span id="manuais-e-docs">Manuais e Documentação</span>

- 📖 [Manual de Instalação](docs/manual-instalacao.md)  
- 👨‍💻 [Manual do Usuário](docs/manual-usuario.md)  
- 🔌 [Documentação da API](docs/api.md)  

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
      <td><a href="https://github.com/TaylorSilva2"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/taylor-silva-859300330/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
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
