# Sistema CSP para Agendamento de Aulas

Sistema inteligente para resolução automática de problemas de agendamento académico utilizando Constraint Satisfaction Problems (CSP).

## Características

- **Performance:** Soluções em < 0.05 segundos
- **Flexibilidade:** Parser dinâmico para múltiplos datasets
- **Qualidade:** Sistema de avaliação multi-critério
- **Exportação:** Relatórios Excel profissionais com cores por turma

## Instalação

```bash
git clone <repository>
cd sistema-csp
pip install -r requirements.txt
```

## Uso Rápido

```bash
# Modo interativo
python main.py

# Dataset específico
python main.py "material/dataset.txt"

# Demonstração completa
python demo.py
```

## Estrutura do Projeto

```
├── dataset_loader.py      # Parser dinâmico de datasets
├── csp_formulation.py     # Formulação CSP otimizada
├── csp_constraints.py     # Restrições hard decompostas
├── csp_solver.py          # Solver hierárquico
├── csp_evaluation.py      # Avaliação de qualidade
├── excel_export.py        # Exportação Excel
├── main.py               # Interface principal
└── material/             # Datasets de exemplo
    ├── dataset.txt
    └── dataset2.txt
```

## Formato de Dataset

```
#cc — courses assigned to classes
LESI       PDM ISI IA SETR PA
LEEC       PS IM R IE RCSD

#dsd — courses assigned to lecturers
João       PDM PS IM
Pedro      ISI R IA

#tr — timeslot restrictions
João       9 10 11 12
Pedro      17 18 19 20

#rr — room restrictions
SETR       Lab01
IM         Lab01

#oc — online classes
PS         2
GSI        2
```

## Otimizações CSP

### Redução de Domínios
- Filtros preventivos por disponibilidade de professores
- Restrições de salas específicas
- Redução de 50% no espaço de busca

### Decomposição Pairwise
- Restrições N-árias → restrições binárias
- Complexidade O(n!) → O(n²)
- 435 restrições binárias para 30 variáveis

### Solver Hierárquico
1. **MinConflictsSolver:** Busca local rápida
2. **BacktrackingSolver:** Busca completa (fallback)

## Resultados

| Dataset | Turmas | UCs | Tempo | Pontuação |
|---------|--------|-----|-------|-----------|
| Dataset 1 | 3 | 15 | 0.030s | 135 pts |
| Dataset 2 | 4 | 19 | 0.040s | 178 pts |

## Exportação Excel

- Uma tabela por turma com cores específicas
- Layout semanal (Segunda a Sexta, 9h-18h)
- Informação completa: UC, Professor, Sala

## Dependências

```
python-constraint
pandas
openpyxl
```

## Licença

MIT License