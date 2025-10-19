"""
Sistema de Agendamento de Aulas usando Constraint Satisfaction Problems (CSP)

Este módulo implementa um sistema inteligente para resolver o problema de agendamento
de aulas numa instituição de ensino superior, utilizando a biblioteca python-constraint.

Autores: Equipa IA25_P04
Data: 2025
"""

from constraint import *
import time
import sys
import traceback


# =============================================================================
# CONFIGURAÇÃO DO DATASET
# =============================================================================

# Mapeamento de turmas para unidades curriculares
# Cada turma tem 5 UCs atribuídas, resultando em 10 lições por semana (2 por UC)
cc = {
    't01': ['UC11', 'UC12', 'UC13', 'UC14', 'UC15'],
    't02': ['UC21', 'UC22', 'UC23', 'UC24', 'UC25'],
    't03': ['UC31', 'UC32', 'UC33', 'UC34', 'UC35']
}

# Atribuição de UCs aos professores
# Define qual professor leciona cada unidade curricular
dsd = {
    'jo': ['UC11', 'UC21', 'UC22', 'UC31'],
    'mike': ['UC12', 'UC23', 'UC32'],
    'rob': ['UC13', 'UC14', 'UC24', 'UC33'],
    'sue': ['UC15', 'UC25', 'UC34', 'UC35']
}

# Restrições de disponibilidade dos professores
# Slots indisponíveis para cada professor (1-20: 5 dias x 4 slots por dia)
tr = {
    'mike': [13, 14, 15, 16, 17, 18, 19, 20],  # Dias 4 e 5 indisponíveis
    'rob': [1, 2, 3, 4],                       # Dia 1 indisponível
    'sue': [9, 10, 11, 12, 17, 18, 19, 20]     # Dias 3 e 5 indisponíveis
}

# Restrições de salas específicas
# UCs que requerem laboratórios ou salas especiais
rr = {
    'UC14': 'Lab01',
    'UC22': 'Lab01'
}

# Aulas online
# Indica qual lição (1 ou 2) de cada UC é ministrada online
oc = {
    'UC21': 2,
    'UC31': 2
}

# Configuração do sistema
rooms = ['RoomA', 'RoomB', 'RoomC', 'Lab01', 'Online']
teachers = ['jo', 'mike', 'rob', 'sue']
classes = ['t01', 't02', 't03']
courses = [course for courses_list in cc.values() for course in courses_list]


# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def get_teacher(course):
    """
    Retorna o professor responsável por uma unidade curricular.
    
    Args:
        course (str): Código da unidade curricular
        
    Returns:
        str: Nome do professor ou None se não encontrado
    """
    for teacher, teacher_courses in dsd.items():
        if course in teacher_courses:
            return teacher
    return None


def get_class(course):
    """
    Retorna a turma à qual uma unidade curricular pertence.
    
    Args:
        course (str): Código da unidade curricular
        
    Returns:
        str: Código da turma ou None se não encontrado
    """
    for class_name, class_courses in cc.items():
        if course in class_courses:
            return class_name
    return None


def get_day(slot):
    """
    Converte um slot temporal (1-20) para o dia da semana (1-5).
    
    Args:
        slot (int): Número do slot (1-20)
        
    Returns:
        int: Dia da semana (1=Segunda, 5=Sexta)
    """
    return (slot - 1) // 4 + 1


def get_domain(course, lesson_idx):
    """
    Calcula o domínio de valores possíveis para uma variável (UC, lição).
    Considera restrições de disponibilidade do professor, salas específicas e aulas online.
    
    Args:
        course (str): Código da unidade curricular
        lesson_idx (int): Número da lição (1 ou 2)
        
    Returns:
        list: Lista de tuplos (slot, sala) representando valores possíveis
    """
    teacher = get_teacher(course)
    unavailable_slots = tr.get(teacher, [])
    
    domain = []
    for slot in range(1, 21):
        if slot not in unavailable_slots:
            # Verifica se esta lição é online
            if course in oc and oc[course] == lesson_idx:
                domain.append((slot, 'Online'))
            # Verifica se a UC requer sala específica
            elif course in rr:
                domain.append((slot, rr[course]))
            else:
                # Adiciona todas as salas físicas disponíveis
                for room in rooms:
                    if room != 'Online':
                        domain.append((slot, room))
    return domain


# =============================================================================
# DEFINIÇÃO DO PROBLEMA CSP
# =============================================================================

# Cria instância do problema CSP
problem = Problem()

# Define variáveis e seus domínios
# Cada variável representa uma lição: (UC, número_da_lição)
variables = []
for course in courses:
    for lesson in [1, 2]:
        var = (course, lesson)
        variables.append(var)
        domain = get_domain(course, lesson)
        problem.addVariable(var, domain)


# =============================================================================
# RESTRIÇÕES HARD (OBRIGATÓRIAS) - VERSÃO OTIMIZADA
# =============================================================================
from itertools import combinations

# Restrição 1: Unicidade de (slot, sala)
# Garante que duas lições não ocorram no mesmo slot e sala física.
# (Nota: As aulas 'Online' podem partilhar o slot 'Online'.)

# Separa variáveis físicas de online
physical_vars = [v for v in variables if ('Online' not in [val[1] for val in get_domain(v[0], v[1])])]

# Aulas físicas devem ter um (slot, sala) único
problem.addConstraint(AllDifferentConstraint(), physical_vars)


# Função de restrição binária (para ser usada abaixo)
def slots_diferentes(val1, val2):
    """Verifica se o slot de duas atribuições é diferente."""
    return val1[0] != val2[0]


# Restrição 2: Conflito de professores (Otimizado)
# Um professor não pode dar duas aulas no mesmo slot
for teacher in teachers:
    teacher_vars = [(course, lesson) for course in dsd[teacher] for lesson in [1, 2]]
    
    # Adiciona uma restrição binária para CADA PAR de aulas do professor
    for var1, var2 in combinations(teacher_vars, 2):
        problem.addConstraint(slots_diferentes, (var1, var2))

# Restrição 3: Conflito de turmas (Otimizado)
# Uma turma não pode ter duas lições no mesmo slot
for class_name in classes:
    class_vars = [(course, lesson) for course in cc[class_name] for lesson in [1, 2]]

    # Adiciona uma restrição binária para CADA PAR de aulas da turma
    for var1, var2 in combinations(class_vars, 2):
        problem.addConstraint(slots_diferentes, (var1, var2))

# Restrição 4: Máximo 3 lições por dia por turma (Já está bom)
# (Esta função é N-ária, mas é menos problemática que as anteriores)
def max_lessons_per_day(*assignments):
    day_counts = {}
    for slot, room in assignments:
        day = get_day(slot)
        day_counts[day] = day_counts.get(day, 0) + 1
        if day_counts[day] > 3:
            return False
    return True

for class_name in classes:
    class_vars = [(course, lesson) for course in cc[class_name] for lesson in [1, 2]]
    problem.addConstraint(max_lessons_per_day, class_vars)


# Restrições 5 & 6: Aulas Online (Já estão boas, mas com a correção que indiquei antes)
def online_same_day(uc21_assignment, uc31_assignment):
    return get_day(uc21_assignment[0]) == get_day(uc31_assignment[0])

problem.addConstraint(online_same_day, [('UC21', 2), ('UC31', 2)])

def max_online_per_day(*assignments):
    online_by_day = {}
    for slot, room in assignments:
        # Não precisa verificar 'room == Online', pois estas vars SÓ PODEM ser Online
        day = get_day(slot)
        online_by_day[day] = online_by_day.get(day, 0) + 1
        if online_by_day[day] > 3:
            return False
    return True

online_vars = [(c, l) for c in oc for l in [1, 2] if oc[c] == l]
if online_vars:
    # APLICA SÓ ÀS VARIÁVEIS ONLINE!
    problem.addConstraint(max_online_per_day, online_vars)

print("Restrições otimizadas foram adicionadas.")




# =============================================================================
# FUNÇÕES DE AVALIAÇÃO (RESTRIÇÕES SOFT)
# =============================================================================

def evaluate_solution(solution):
    """
    Avalia a qualidade de uma solução com base em critérios soft.
    Critérios considerados:
    1. Distribuição temporal das lições de cada UC
    2. Distribuição de aulas por dias da semana
    3. Minimização do número de salas por turma
    4. Consecutividade de aulas no mesmo dia
    
    Args:
        solution (dict): Solução a ser avaliada
        
    Returns:
        int: Pontuação da solução (maior = melhor)
    """
    score = 0
    score += _evaluate_course_distribution(solution)
    score += _evaluate_class_distribution(solution)
    score += _evaluate_room_usage(solution)
    score += _evaluate_consecutive_lessons(solution)
    return score


def _evaluate_course_distribution(solution):
    """
    Avalia a distribuição temporal das lições de cada UC.
    Premia quando as duas lições de uma UC estão em dias diferentes.
    
    Args:
        solution (dict): Solução a ser avaliada
        
    Returns:
        int: Pontuação parcial (+10 por UC com lições em dias diferentes)
    """
    score = 0
    for course in courses:
        lesson1_slot = solution[(course, 1)][0]
        lesson2_slot = solution[(course, 2)][0]
        if get_day(lesson1_slot) != get_day(lesson2_slot):
            score += 10
    return score


def _evaluate_class_distribution(solution):
    """
    Avalia a distribuição de aulas por dias da semana.
    Premia turmas com aulas distribuídas por exatamente 4 dias.
    
    Args:
        solution (dict): Solução a ser avaliada
        
    Returns:
        int: Pontuação parcial (+20 por turma com aulas em 4 dias)
    """
    score = 0
    for class_name in classes:
        days_used = {get_day(solution[(course, lesson)][0])
                    for course in cc[class_name] for lesson in [1, 2]}
        if len(days_used) == 4:
            score += 20
    return score


def _evaluate_room_usage(solution):
    """
    Penaliza o uso excessivo de salas por turma.
    Incentiva a concentração de aulas em menos salas.
    
    Args:
        solution (dict): Solução a ser avaliada
        
    Returns:
        int: Pontuação parcial (-2 por sala utilizada)
    """
    score = 0
    for class_name in classes:
        rooms_used = {solution[(course, lesson)][1]
                     for course in cc[class_name] for lesson in [1, 2]}
        score -= len(rooms_used) * 2
    return score


def _evaluate_consecutive_lessons(solution):
    """
    Premia aulas consecutivas no mesmo dia.
    Evita "buracos" no horário das turmas.
    
    Args:
        solution (dict): Solução a ser avaliada
        
    Returns:
        int: Pontuação parcial (+5 por dia com aulas consecutivas)
    """
    return sum(_check_class_consecutiveness(solution, class_name)
              for class_name in classes)


def _check_class_consecutiveness(solution, class_name):
    """
    Verifica a consecutividade de aulas para uma turma específica.
    
    Args:
        solution (dict): Solução a ser avaliada
        class_name (str): Código da turma
        
    Returns:
        int: Pontuação parcial para esta turma
    """
    slots_by_day = _group_slots_by_day(solution, class_name)
    return sum(5 for slots in slots_by_day.values()
              if len(slots) > 1 and _are_consecutive(sorted(slots)))


def _group_slots_by_day(solution, class_name):
    """
    Agrupa os slots de uma turma por dia da semana.
    
    Args:
        solution (dict): Solução a ser avaliada
        class_name (str): Código da turma
        
    Returns:
        dict: Dicionário {dia: [slots]}
    """
    slots_by_day = {}
    for course in cc[class_name]:
        for lesson in [1, 2]:
            slot = solution[(course, lesson)][0]
            day = get_day(slot)
            slots_by_day.setdefault(day, []).append(slot)
    return slots_by_day


def _are_consecutive(slots):
    """
    Verifica se uma lista de slots é consecutiva.
    
    Args:
        slots (list): Lista de slots ordenada
        
    Returns:
        bool: True se todos os slots são consecutivos
    """
    for i in range(1, len(slots)):
        if slots[i] - slots[i-1] != 1:
            return False
    return True


def _display_schedule(solution):
    """
    Exibe o horário de forma formatada e organizada.
    
    Args:
        solution (dict): Solução a ser exibida
    """
    for class_name in classes:
        print(f"\nTurma {class_name}:")
        
        # Cria lista de lições com informação completa
        schedule = [(get_day(solution[(course, lesson)][0]),
                    ((solution[(course, lesson)][0] - 1) % 4) + 1,
                    course, lesson, solution[(course, lesson)][1])
                   for course in cc[class_name] for lesson in [1, 2]]
        
        # Ordena e exibe
        for day, slot_in_day, course, lesson, room in sorted(schedule):
            room_type = "[Online]" if room == 'Online' else f"[{room}]"
            print(f"  Dia {day}, Slot {slot_in_day}: {course}_L{lesson} {room_type}")



## =============================================================================
# RESOLUÇÃO DO PROBLEMA CSP (ESTRATÉGIA MELHORADA)
# =============================================================================

print("\nProcurando soluções (estratégia iterativa)...")
start_time = time.time()

solutions_found = []
best_solution = None
best_score = -float('inf')

# Define um limite de soluções a procurar para não ficar infinito
MAX_SOLUTIONS_TO_CHECK = 1000 
# Ou pode usar um limite de tempo
# TIME_LIMIT_SECONDS = 300 # 5 minutos

try:
    solution_iterator = problem.getSolutionIter()
    
    for i, solution in enumerate(solution_iterator):
        solutions_found.append(solution)
        
        current_score = evaluate_solution(solution)
        
        if current_score > best_score:
            best_score = current_score
            best_solution = solution
            print(f"  -> Nova melhor solução encontrada (Solução nº {i+1}, Score: {best_score})")

        if i + 1 >= MAX_SOLUTIONS_TO_CHECK:
            print(f"\n[AVISO] Limite de {MAX_SOLUTIONS_TO_CHECK} soluções atingido.")
            break
            
        # Descomente as 3 linhas seguintes para usar um limite de tempo
        # current_time = time.time() - start_time
        # if current_time > TIME_LIMIT_SECONDS:
        #    print(f"\n[AVISO] Limite de tempo de {TIME_LIMIT_SECONDS}s atingido.")
        #    break

    solve_time = time.time() - start_time

    print(f"\n[OK] Busca concluída em {solve_time:.3f} segundos.")
    print(f"Total de soluções analisadas: {len(solutions_found)}")

    if not best_solution:
        print(f"[ERRO] Nenhuma solução encontrada.")
        sys.exit(1)
        
except Exception as e:
    print(f"\n[ERRO] Erro durante resolução: {e}")
    traceback.print_exc()
    sys.exit(1)


# =============================================================================
# AVALIAÇÃO E APRESENTAÇÃO DOS RESULTADOS
# =============================================================================

if best_solution:
    print(f"\n{'='*60}")
    print(f"MELHOR SOLUÇÃO ENCONTRADA (Pontuação: {best_score})")
    print(f"{'='*60}")

    _display_schedule(best_solution)
    
    print(f"\nPontuação final: {best_score}")
    print("\n[OK] Execução concluída com sucesso!")
else:
    print("\n[ERRO] Nenhuma solução foi encontrada!")




# =============================================================================
# AVALIAÇÃO E APRESENTAÇÃO DOS RESULTADOS
# =============================================================================

if solution:
    print("\nAvaliando qualidade da solucao...")
    eval_start = time.time()
    
    best_solution = solution
    best_score = evaluate_solution(solution)
    
    eval_time = time.time() - eval_start
    print(f"[OK] Avaliacao concluida em {eval_time:.3f} segundos")
    print(f"Pontuacao obtida: {best_score}")

    # Apresentação dos resultados
    print(f"\n{'='*60}")
    print(f"SOLUCAO ENCONTRADA (Pontuacao: {best_score})")
    print(f"{'='*60}")

    _display_schedule(best_solution)
    
    print(f"\nPontuacao final: {best_score}")
    print("\n[OK] Execucao concluida com sucesso!")
else:
    print("\n[ERRO] Nenhuma solucao foi encontrada!")
