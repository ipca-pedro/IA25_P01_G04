# Sistema CSP Dinâmico - Agendamento de Aulas

## ✅ TRANSFORMAÇÃO CONCLUÍDA

O projeto foi **transformado com sucesso** de um sistema estático para um **sistema dinâmico** que pode processar qualquer dataset em formato `.txt`.

---

## 🔄 O Que Mudou

### ANTES (Sistema Estático)
- ❌ Apenas lia dados do `dataset.py`
- ❌ Configuração fixa e inflexível
- ❌ Necessário modificar código para novos datasets

### DEPOIS (Sistema Dinâmico)
- ✅ Lê qualquer dataset em formato `.txt`
- ✅ Seleção interativa de datasets
- ✅ Suporte via linha de comando
- ✅ Parser automático de diferentes formatos
- ✅ Compatível com UCs partilhadas entre turmas

---

## 🚀 Como Usar

### 1. Modo Interativo (Recomendado)
```bash
python main.py
```
O sistema mostra todos os datasets disponíveis e permite escolher.

### 2. Dataset Específico
```bash
python main.py "material\dataset.txt"
python main.py "material\dataset2.txt"
```

### 3. Demonstração Completa
```bash
python demo.py
```
Processa automaticamente todos os datasets e mostra estatísticas.

---

## 📁 Estrutura de Datasets

Os datasets devem estar na pasta `material/` com formato:

```
#cc — courses assigned to classes
t01         UC11 UC12 UC13 UC14 UC15
t02         UC21 UC22 UC23 UC24 UC25

#dsd — courses assigned to lecturers  
jo          UC11 UC21 UC22 UC31
mike        UC12 UC23 UC32

#tr — timeslot restrictions
mike        13 14 15 16 17 18 19 20
rob         1 2 3 4

#rr — room restrictions
UC14        Lab01
UC22        Lab01

#oc — online classes
UC21        2
UC31        2
```

---

## 🆕 Funcionalidades Adicionadas

### 1. **Dataset Loader Dinâmico** (`dataset_loader.py`)
- Parser automático de arquivos `.txt`
- Suporte a diferentes formatos de dados
- Tratamento de UCs partilhadas entre turmas
- Validação automática de dados

### 2. **Seleção Interativa** (modificado `main.py`)
- Lista automática de datasets disponíveis
- Interface de seleção numerada
- Suporte a argumentos de linha de comando
- Tratamento de erros robusto

### 3. **Sistema Modular Atualizado**
- Todos os módulos agora aceitam dataset como parâmetro
- Compatibilidade mantida com funcionalidades existentes
- Otimizações CSP preservadas

### 4. **Script de Demonstração** (`demo.py`)
- Processamento automático de todos os datasets
- Estatísticas detalhadas por dataset
- Medição de performance
- Relatório completo de funcionalidades

---

## 📊 Resultados dos Testes

### Dataset 1 (Original)
- **Turmas:** 3 (t01, t02, t03)
- **Professores:** 4 (jo, mike, rob, sue)  
- **UCs:** 15
- **Tempo:** ~0.03s
- **Pontuação:** 109-161

### Dataset 2 (Novo)
- **Turmas:** 4 (LESI, LEEC, LEIM, LDJG)
- **Professores:** 6 (João, Pedro, António, Manuel, Ana, Isabel)
- **UCs:** 19 (com UC 'IA' partilhada)
- **Tempo:** ~0.04s  
- **Pontuação:** 171-186

---

## 🔧 Arquivos Modificados

1. **`dataset_loader.py`** - NOVO: Parser dinâmico
2. **`main.py`** - Seleção interativa e argumentos CLI
3. **`csp_formulation.py`** - Aceita dataset como parâmetro
4. **`csp_constraints.py`** - Aceita dataset como parâmetro  
5. **`csp_evaluation.py`** - Aceita dataset como parâmetro
6. **`demo.py`** - NOVO: Script de demonstração

---

## ✨ Vantagens do Sistema Dinâmico

1. **Flexibilidade Total:** Qualquer dataset compatível funciona
2. **Facilidade de Uso:** Interface intuitiva para seleção
3. **Escalabilidade:** Suporta datasets de qualquer tamanho
4. **Robustez:** Tratamento de erros e validação automática
5. **Performance:** Mantém todas as otimizações CSP originais
6. **Compatibilidade:** Funciona com formatos de dados variados

---

## 🎯 Casos de Uso

- **Instituições Diferentes:** Cada uma com seu dataset
- **Semestres Diferentes:** Datasets sazonais
- **Testes e Simulações:** Múltiplos cenários rapidamente
- **Desenvolvimento:** Fácil adição de novos datasets
- **Demonstrações:** Sistema completo em funcionamento

O sistema agora é **verdadeiramente dinâmico** e pronto para uso em qualquer contexto educacional! 🎓