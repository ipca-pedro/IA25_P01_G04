"""
Restrições Hard do CSP - Decomposição otimizada em restrições binárias

"""

from itertools import combinations
from csp_formulation import get_day


def no_room_conflict(val1, val2):
    """
    Restrição binária otimizada para impedir conflitos de sala física.
    
    Substitui a restrição N-ária original:
    Por uma comparação direta muito mais eficiente.
    
    Args:
        val1: Primeira atribuição (slot, sala)
        val2: Segunda atribuição (slot, sala)
        
    Returns:
        bool: True se não há conflito (valores diferentes)
    """
    return val1 != val2


def different_slots(val1, val2):
    """
    Restrição binária para garantir slots diferentes
    
    Utilizada para conflitos de professores e turmas
    Compara apenas o slot (val[0]) ignorando a sala (val[1])
    Muito mais eficiente que verificar unicidade em lista completa
    
    Args:
        val1 (tuple): Primeira atribuição (slot, sala)
        val2 (tuple): Segunda atribuição (slot, sala)
        
    Returns:
        bool: True se os slots são diferentes
    """
    return val1[0] != val2[0]


def max_lessons_per_day(*assignments):
    """
    Restrição que limita o número máximo de lições por dia para uma turma.
    
    Evita sobrecarga de estudantes com mais de 3 aulas num único dia.
    Melhora a distribuição da carga horária ao longo da semana.
    
    Args:
        *assignments: Atribuições de (slot, sala) para as variáveis da turma
        
    Returns:
        bool: True se nenhum dia excede 3 lições
    """
    day_counts = {}  # Contador de lições por dia
    for slot, room in assignments:
        day = get_day(slot)  # Converte slot para dia (1-5)
        day_counts[day] = day_counts.get(day, 0) + 1
        # Falha imediatamente se exceder 3 lições num dia
        if day_counts[day] > 3:
            return False
    return True


def online_same_day(uc21_assignment, uc31_assignment):
    """
    Restrição de coordenação para aulas online
    
    Garante que as duas aulas online (UC21_L2 e UC31_L2) ocorram
    no mesmo dia para facilitar a gestão de recursos tecnológicos
    e coordenação de suporte técnico
    
    Args:
        uc21_assignment (tuple): Atribuição (slot, sala) para UC21_L2
        uc31_assignment (tuple): Atribuição (slot, sala) para UC31_L2
        
    Returns:
        bool: True se ambas as aulas estão no mesmo dia
    """
    uc21_slot, _ = uc21_assignment
    uc31_slot, _ = uc31_assignment
    return get_day(uc21_slot) == get_day(uc31_slot)


def max_online_per_day(*assignments):
    """
    Restrição que limita o número máximo de aulas online por dia.
    Args:
        *assignments: Atribuições de (slot, sala) para variáveis online
        
    Returns:
        bool: True se nenhum dia excede 3 aulas online
    """
    online_by_day = {}  # Contador de aulas online por dia
    for slot, room in assignments:
        if room == 'Online':  # Considera apenas aulas online
            day = get_day(slot)
            online_by_day[day] = online_by_day.get(day, 0) + 1
            # Falha imediatamente se exceder 3 aulas online num dia
            if online_by_day[day] > 3:
                return False
    return True


def consecutive_lessons_constraint(*assignments):
    """
    Restrição hard de consecutividade: aulas no mesmo dia devem ser consecutivas.
    """
    # Agrupa slots por dia
    slots_by_day = {}
    for slot, room in assignments:
        day = get_day(slot)
        slots_by_day.setdefault(day, []).append(slot)
    
    # Verifica consecutividade em cada dia
    for day_slots in slots_by_day.values():
        if len(day_slots) > 1:
            day_slots.sort()
            # Converte para slots dentro do dia (1-4)
            day_slots_normalized = [((slot - 1) % 4) + 1 for slot in day_slots]
            day_slots_normalized.sort()
            
            # Verifica se são consecutivos
            for i in range(1, len(day_slots_normalized)):
                if day_slots_normalized[i] - day_slots_normalized[i-1] != 1:
                    return False  # Não consecutivos
    return True


def apply_hard_constraints(problem, variables_info, dataset):
    """
    Aplica todas as restrições hard obrigatórias ao problema CSP.
    
    Args:
        problem: Instância do problema CSP
        variables_info (dict): Dicionário com variáveis organizadas por tipo
    """
    # Extrai conjuntos de variáveis organizados por tipo
    physical_vars = variables_info['physical_vars']  # Variáveis físicas (não online)
    teacher_vars = variables_info['teacher_vars']    # Variáveis por professor
    class_vars = variables_info['class_vars']        # Variáveis por turma
    online_vars = variables_info['online_vars']      # Variáveis online
    
    # RESTRIÇÃO 1: Unicidade de (slot, sala) - DECOMPOSIÇÃO PAIRWISE 
    for var1, var2 in combinations(physical_vars, 2):
        problem.addConstraint(no_room_conflict, (var1, var2))
    
    # RESTRIÇÃO 2: Conflito de professores - DECOMPOSIÇÃO POR PROFESSOR
    for teacher_courses in teacher_vars.values():
        for var1, var2 in combinations(teacher_courses, 2):
            problem.addConstraint(different_slots, (var1, var2))
    
    # RESTRIÇÃO 3: Conflito de turmas - DECOMPOSIÇÃO POR TURMA
    for class_courses in class_vars.values():
        for var1, var2 in combinations(class_courses, 2):
            problem.addConstraint(different_slots, (var1, var2))
    
    # RESTRIÇÃO 4: Máximo 3 lições por dia por turma
    for class_name in dataset['classes']:
        class_variables = class_vars[class_name]
        problem.addConstraint(max_lessons_per_day, class_variables)
    
    # RESTRIÇÃO 5: Coordenação de aulas online
    if len(online_vars) >= 2:
        # Encontra as duas variáveis online específicas
        uc21_var = None
        uc31_var = None
        for var in online_vars:
            if var[0] == 'UC21' and var[1] == 2:
                uc21_var = var
            elif var[0] == 'UC31' and var[1] == 2:
                uc31_var = var
        
        if uc21_var and uc31_var:
            problem.addConstraint(online_same_day, [uc21_var, uc31_var])
    
    # RESTRIÇÃO 6: Limite de aulas online por dia
    if online_vars:
        problem.addConstraint(max_online_per_day, online_vars)
    
    # RESTRIÇÃO 7: Consecutividade obrigatória por turma
    for class_name in dataset['classes']:
        class_variables = class_vars[class_name]
        problem.addConstraint(consecutive_lessons_constraint, class_variables)