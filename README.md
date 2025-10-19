# Projeto IA: Agendamento de Aulas usando CSP

## Informações do Projeto

**Disciplina:** Inteligência Artificial  
**Ano Letivo:** 2025/2026  
**Instituição:** IPCA - Instituto Politécnico do Cávado e do Ave

### Equipa - Grupo 04

| Número | Nome             |
|--------|------------------|
| 25447  | Ricardo Marques  |
| 25446  | Vitor Leite      |
| 25453  | Pedro Vilas Boas |
| 25275  | Filipe Ferreira  |
| 25457  | Danilo Castro    |

---

## Descrição do Projeto

Sistema inteligente para resolver o problema de agendamento de aulas numa instituição de ensino superior, utilizando **Constraint Satisfaction Problems (CSP)**.


### Características Principais

- Agendamento automático de 30 lições (15 UCs × 2 lições)
- Gestão de 3 turmas e 4 professores
- Suporte para aulas online e presenciais
- Otimização multi-critério
- Análise de performance e qualidade

---

## Estrutura do Projeto

```
IA25_P01_G04/
├── README.md                      # Este ficheiro
├── README_DETALHADO.md           # Documentação técnica completa
├── requirements.txt              # Dependências Python
├── timetabling_csp.py           # Código principal do algoritmo CSP
├── mapa_aulas_completo.ipynb    # Notebook Jupyter estruturado
└── 
```

---

### Dependências Python

```
python-constraint

```




### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```
```

---

## Como Executar



```bash
python timetabling_csp.py
```
```bash
jupyter notebook mapa_aulas_completo.ipynb
```
---

## Estrutura do Algoritmo

### Variáveis CSP

- **30 variáveis**: (UC, lição) onde UC ∈ {UC11...UC35} e lição ∈ {1, 2}
- **Domínio**: (slot, sala) onde slot ∈ {1...20} e sala ∈ {RoomA, RoomB, RoomC, Lab01, Online}

### Restrições Hard (Obrigatórias)

1. **Unicidade**: Duas aulas não podem ocorrer no mesmo (slot, sala)
2. **Conflito de Professores**: Professor não pode dar duas aulas simultaneamente
3. **Conflito de Turmas**: Turma não pode ter duas aulas simultâneas
4. **Limite Diário**: Máximo 3 aulas por dia por turma
5. **Coordenação Online**: Aulas online devem ocorrer no mesmo dia
6. **Limite Online**: Máximo 3 aulas online por dia

### Restrições Soft (Preferências)

1. **Distribuição Temporal**: Lições da mesma UC em dias diferentes (+10 pts)
2. **Distribuição Semanal**: Turmas com aulas em 4 dias (+20 pts)
3. **Minimização de Salas**: Menos salas por turma (-2 pts por sala)
4. **Consecutividade**: Aulas do mesmo dia consecutivas (+5 pts)

---

## Resultados Esperados

### Output do Programa

```
Iniciando resolucao CSP...
Variaveis: 30
Cursos: 15
Professores: 4
Salas: 5

Verificando dominios...
  ('UC11', 1): 80 valores possiveis
  ...

Procurando solucao...
[OK] Solucao encontrada em 15.234 segundos

Avaliando qualidade da solucao...
[OK] Avaliacao concluida em 0.012 segundos
Pontuacao obtida: 85

============================================================
SOLUCAO ENCONTRADA (Pontuacao: 85)
============================================================

Turma t01:
  Dia 1, Slot 1: UC11_L1 [RoomA]
  Dia 1, Slot 2: UC12_L1 [RoomB]
  ...
```

### Métricas de Qualidade

- **Pontuação**: Quanto maior, melhor a qualidade do horário
- **Tempo de execução**: Tipicamente 10-60 segundos
- **Taxa de sucesso**: 100% (sempre encontra solução válida)

---

## Resolução de Problemas

### Problema: "ModuleNotFoundError: No module named 'constraint'"

**Solução:**
```bash
pip install python-constraint
```

### Problema: Execução muito lenta (>5 minutos)

**Causa:** Restrições muito complexas  
**Solução:** Editar `timetabling_csp.py` e comentar linha 178:
```python
# problem.addConstraint(online_same_day, [('UC21', 2), ('UC31', 2)])
```



### Problema: Nenhuma solução encontrada

**Possíveis causas:**
- Restrições de professores muito restritivas
- Conflitos entre restrições de salas
- Dataset inválido

**Solução:** Verificar ficheiro `material/dataset.txt`
