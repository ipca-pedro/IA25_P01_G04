# Sistema Inteligente de Agendamento Académico (CSP)

**Disciplina:** Inteligência Artificial (2025/26)  
**Instituição:** IPCA - Instituto Politécnico do Cávado e do Ave  
**Curso:** Engenharia de Sistemas Informáticos

## Grupo 04

- Ricardo Marques (25447)
- Vitor Leite (25446)
- Pedro Vilas Boas (25453)
- Filipe Ferreira (25275)
- Danilo Castro (25457)

## Resumo do Projeto

Este projeto implementa um sistema inteligente para resolver o problema de **Alocação de Horários (Timetabling)**, utilizando uma abordagem baseada em **Constraint Satisfaction Problems (CSP)**.

O objetivo é automatizar a criação de horários académicos, respeitando restrições obrigatórias (Hard Constraints) e otimizando preferências desejáveis (Soft Constraints).

**Entregável principal:** `relatorio.ipynb` - Notebook que consolida análise técnica, documentação e código executável.

## Desafio Computacional

O problema de agendamento de horários é um desafio clássico de otimização combinatória. Uma formulação ingénua é computacionalmente intratável:

- **Variáveis:** 30 lições (15 UCs × 2 lições cada)
- **Domínio base:** ~80 combinações (slot, sala) por lição
- **Espaço de busca:** ~80^30 ≈ 10^57 combinações possíveis

Este espaço de busca astronómico exige otimizações de IA para encontrar soluções válidas em tempo útil.

## Solução: Pipeline de Otimização CSP

Sistema modular que aplica técnicas de IA para decompor, restringir e resolver o problema eficientemente. Opera em processo de duas fases:

### Fase 1: Solução Válida
Utiliza solver hierárquico para encontrar rapidamente qualquer solução que satisfaça todas as Hard Constraints. Garante solução funcional em <1 segundo.

### Fase 2: Otimização de Qualidade
Após encontrar solução válida, executa ciclo de otimização durante 60 segundos usando busca local (MinConflictsSolver) para maximizar pontuação das Soft Constraints.

## Técnicas de IA Implementadas

Performance alcançada através de quatro otimizações fundamentais:

### 1. Consistência de Nó
- **Localização:** `csp_formulation.py` (função `get_domain`)
- **Método:** Filtragem preventiva de domínios antes da busca
- **Aplicações:**
  - Filtra slots indisponíveis de professores
  - Restringe domínio para aulas online
  - Restringe domínio para laboratórios específicos
- **Resultado:** Redução ~50% do espaço de busca inicial

### 2. Heurística MRV (Minimum Remaining Values)
- **Localização:** `csp_formulation.py` (função `create_csp_problem`)
- **Método:** Ordenação estratégica de variáveis (Fail-First)
- **Implementação:** Variáveis com domínios menores processadas primeiro
- **Resultado:** Redução drástica de backtracking

### 3. Decomposição Pairwise
- **Localização:** `csp_constraints.py`
- **Método:** Transformação de restrições N-árias em binárias
- **Complexidade:** O(n!) → O(n²)
- **Funções principais:**
  - `no_room_conflict`: Garante unicidade de (slot, sala)
  - `different_slots`: Evita conflitos de professores/turmas
- **Resultado:** Propagação eficiente de restrições

### 4. Solver Hierárquico
- **Localização:** Integrado no `main.py`
- **Estratégia:** Combinação de dois algoritmos
  - **Tentativa 1:** MinConflictsSolver (busca local rápida)
  - **Tentativa 2:** BacktrackingSolver (busca completa)
- **Resultado:** Velocidade + garantia de completude

## Arquitetura do Sistema

| Módulo | Responsabilidade |
|--------|------------------|
| `relatorio.ipynb` | **ENTREGÁVEL PRINCIPAL** - Documentação e código executável |
| `main.py` | Orquestrador principal (pipeline 2 fases) |
| `dataset_loader.py` | Parser dinâmico de ficheiros de dados |
| `csp_formulation.py` | Definição de variáveis, domínios, MRV |
| `csp_constraints.py` | Restrições Hard e decomposição Pairwise |
| `csp_evaluation.py` | Sistema de pontuação (Soft Constraints) |
| `excel_export.py` | Geração de relatórios Excel formatados |
| `requirements.txt` | Dependências Python |
| `material/` | Datasets (dataset.txt, dataset2.txt) |

## Execução

### Requisitos
- Python 3.10+
- Bibliotecas: `python-constraint`, `pandas`, `openpyxl`, `jupyter`

### Instalação


# Instalar dependências
pip install -r requirements.txt
```

### Execução Recomendada

Abrir `relatorio.ipynb` num editor compatível (Jupyter Lab, VS Code) e executar todas as células. O notebook guia através de toda a análise e executa o pipeline completo.

### Execução Alternativa

```bash
python main.py
```

O script solicita seleção de dataset e executa pipeline de duas fases.

### Resultados

Após execução, são gerados:
- `Horario_Academico_Inicial.xlsx` - Primeira solução válida
- `Horario_Academico_Otimizado.xlsx` - Melhor solução após otimização

## Resultados Alcançados

- **Performance:** Soluções em <0.05 segundos
- **Qualidade:** Sistema multi-critério (50-200 pontos)
- **Redução de complexidade:** ~10^21x menor espaço de busca
- **Taxa de sucesso:** 100% (sempre encontra solução válida)
- **Exportação:** Relatórios Excel profissionais