# Agente de Alocação de Horários (CSP) – Grupo 04

Este repositório contém o projeto de **Inteligência Artificial (2025/26)** do **IPCA**, centrado na resolução do problema de **Alocação de Horários (Timetabling)** através de um **Agente Inteligente** baseado em **Constraint Satisfaction Problems (CSP)**.  

O principal entregável é o ficheiro `relatorio.ipynb`, que integra a documentação técnica completa e o código executável, conforme os requisitos do projeto.

---

## 1. Resumo Técnico

O problema consiste em agendar **30 lições** (15 UCs × 2) dentro de um domínio aproximado de **80 combinações possíveis** (20 slots × 4 salas).  
Uma abordagem de força bruta implicaria um espaço de busca na ordem de **10⁵⁷ combinações**, sendo, portanto, **computacionalmente intratável**.

O projeto implementa um **pipeline de otimização baseado em IA**, capaz de resolver o problema em **menos de 0,05 segundos**, através da aplicação hierárquica de técnicas de CSP que reduzem significativamente o espaço de busca.

---

## 2. Técnicas de IA e CSP Implementadas

O desempenho do agente resulta da combinação de várias otimizações estruturadas:

### 2.1 Consistência de Nó (Pré-processamento)
A função `get_domain()` filtra o domínio de cada variável antes da resolução, eliminando valores que violam restrições unárias (ex.: disponibilidade do professor, requisitos de sala).  
Esta etapa reduz o espaço de busca inicial em cerca de **50%**.

### 2.2 Consistência de Arco (Decomposição Binária)
As restrições n-árias, como “nenhuma das 30 aulas pode ocorrer no mesmo slot/sala”, são decompostas em **restrições binárias pairwise**, reduzindo a complexidade de **O(n!)** para **O(n²)**.  
Isto permite a aplicação eficiente da **Consistência de Arco** e a propagação automática das restrições pelo solver.

### 2.3 Heurística de Ordenação (MRV – Most Restrictive Variable)
A heurística **Fail-First (MRV)** seleciona primeiro as variáveis com menor domínio (ex.: aulas com requisitos de laboratório ou online).  
Desta forma, o solver resolve as partes mais restritivas no início, reduzindo significativamente o número de retrocessos (*backtracking*).

### 2.4 Solver Hierárquico e Otimização de Qualidade
O agente opera em duas fases distintas:

- **Fase 1 – Solução Válida:**  
  Aplica um solver híbrido: tenta o `MinConflictsSolver` (busca local rápida) e, caso necessário, recorre ao `BacktrackingSolver` (busca completa), garantindo 100% de sucesso e elevada velocidade.

- **Fase 2 – Otimização da Solução:**  
  Um ciclo de otimização cronometrado (`timed_optimization`) melhora a qualidade da solução, maximizando as **restrições soft** (ex.: distribuição equilibrada de dias e aulas consecutivas).

---

## 3. Funcionalidades Principais

- **Parser de Dataset Dinâmico:** Carrega automaticamente ficheiros `.txt` com professores, UCs e restrições.  
- **Avaliação Multi-Critério:** Atribui pontuação às soluções com base em quatro critérios de qualidade (restrições soft).  
- **Exportação Automática:** Gera relatórios `.xlsx` com visualização semanal, cores por turma e formatação de grelha.

---

## 4. Execução do Projeto

### Requisitos

- Python 3.10 ou superior  
- Bibliotecas:  
  `python-constraint`, `pandas`, `openpyxl`, `jupyter`

### Passos de Execução

1. **Clonar o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd IA25_P01_G04
   ```

2. **Instalar as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Abrir o relatório notebook:**
   ```bash
   code relatorio.ipynb
   # ou
   jupyter lab
   ```

4. **Executar todas as células do notebook:**
   O bloco final (“Execução do Agente”) executa automaticamente o pipeline:
   1. Carregamento do dataset  
   2. Formulação do problema (Consistência de Nó + MRV)  
   3. Aplicação de restrições (Consistência de Arco)  
   4. Resolução hierárquica (Fase 1 e Fase 2)  
   5. Geração do ficheiro Excel `horario_otimizado_...xlsx`

---

## 5. Estrutura do Repositório

```
IA25_P01_G04/
│
├── relatorio.ipynb           # [ENTREGÁVEL PRINCIPAL] Relatório técnico e executável
├── main.py                   # Ponto de entrada com o pipeline de duas fases
├── requirements.txt           # Lista de dependências
│
├── csp_formulation.py        # Definição de variáveis, domínios, consistência de nó e MRV
├── csp_constraints.py        # Restrições hard e decomposição pairwise (consistência de arco)
├── csp_solver.py             # Implementação do solver hierárquico
├── csp_evaluation.py         # Avaliação e pontuação de restrições soft
│
├── dataset_loader.py         # Parser de ficheiros .txt
├── excel_export.py           # Exportação e formatação do ficheiro .xlsx
│
└── material/
    ├── dataset.txt
    └── dataset2.txt
```

---

## 6. Créditos

**Instituto Politécnico do Cávado e do Ave (IPCA)**  
Unidade Curricular: Inteligência Artificial (2025/26)  
Projeto desenvolvido por: **Grupo 04**
