"""
MÓDULO 3: RESTRIÇÕES CSP
Implementação das restrições hard e soft do problema
"""

from constraint import *
from dataset import *
from csp_formulation import get_day, get_teacher


def create_csp_problem():
    """
    Cria o problema CSP com todas as variáveis e restrições.
    
    Returns:
        Problem: Instância do problema CSP configurado
    """
    from csp_formulation import create_variables, get_domain
    
    problem = Problem()
    variables = create_variables()
    
    # Adicionar variáveis com domínios
    for var in variables:
        domain = get_domain(var[0], var[1])
        problem.addVariable(var, domain)
    
    # Adicionar restrições hard
    add_hard_constraints(problem, variables)
    
    return problem, variables


def add_hard_constraints(problem, variables):
    """
    Adiciona todas as restrições hard (obrigatórias) ao problema CSP.
    """
    # 1. Unicidade de (slot, sala)
    problem.addConstraint(AllDifferentConstraint(), variables)
    
    # 2. Conflitos de professores
    for teacher in teachers:
        teacher_vars = [(course, lesson) for course in dsd[teacher] for lesson in [1, 2]]
        if teacher_vars:
            problem.addConstraint(
                lambda *assignments: len(set(slot for slot, room in assignments)) == len(assignments),
                teacher_vars
            )
    
    # 3. Conflitos de turmas
    for class_name in classes:
        class_vars = [(course, lesson) for course in cc[class_name] for lesson in [1, 2]]
        problem.addConstraint(
            lambda *assignments: len(set(slot for slot, room in assignments)) == len(assignments),
            class_vars
        )
    
    # 4. Máximo 3 lições por dia por turma
    for class_name in classes:
        class_vars = [(course, lesson) for course in cc[class_name] for lesson in [1, 2]]
        problem.addConstraint(max_lessons_per_day, class_vars)
    
    # 5. Coordenação de aulas online
    problem.addConstraint(online_same_day, [('UC21', 2), ('UC31', 2)])
    
    # 6. Máximo 3 aulas online por dia
    online_vars = [(course, lesson) for course in courses for lesson in [1, 2]
                   if course in oc and oc[course] == lesson]
    if online_vars:
        problem.addConstraint(max_online_per_day, variables)


def max_lessons_per_day(*assignments):
    """Restrição: Máximo 3 lições por dia por turma"""
    day_counts = {}
    for slot, room in assignments:
        day = get_day(slot)
        day_counts[day] = day_counts.get(day, 0) + 1
        if day_counts[day] > 3:
            return False
    return True


def online_same_day(uc21_assignment, uc31_assignment):
    """Restrição: Aulas online no mesmo dia"""
    uc21_slot, _ = uc21_assignment
    uc31_slot, _ = uc31_assignment
    return get_day(uc21_slot) == get_day(uc31_slot)


def max_online_per_day(*assignments):
    """Restrição: Máximo 3 aulas online por dia"""
    online_by_day = {}
    for slot, room in assignments:
        if room == 'Online':
            day = get_day(slot)
            online_by_day[day] = online_by_day.get(day, 0) + 1
            if online_by_day[day] > 3:
                return False
    return True


if __name__ == "__main__":
    problem, variables = create_csp_problem()
    print(f"Problema CSP criado com {len(variables)} variáveis e restrições hard aplicadas.")