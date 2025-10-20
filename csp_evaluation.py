"""
MÓDULO 5: AVALIAÇÃO E APRESENTAÇÃO
Funções para avaliar qualidade das soluções e exibir resultados
"""

from dataset import *
from csp_formulation import get_day


def evaluate_solution(solution):
    """
    Avalia a qualidade de uma solução baseada em restrições soft.
    
    Args:
        solution (dict): Solução CSP a avaliar
        
    Returns:
        int: Pontuação total (maior = melhor)
    """
    score = 0
    score += _evaluate_course_distribution(solution)
    score += _evaluate_class_distribution(solution)
    score += _evaluate_room_usage(solution)
    score += _evaluate_consecutive_lessons(solution)
    return score


def _evaluate_course_distribution(solution):
    """Critério 1: Lições da mesma UC em dias diferentes (+10 pts/UC)"""
    score = 0
    for course in courses:
        lesson1_slot = solution[(course, 1)][0]
        lesson2_slot = solution[(course, 2)][0]
        if get_day(lesson1_slot) != get_day(lesson2_slot):
            score += 10
    return score


def _evaluate_class_distribution(solution):
    """Critério 2: Turmas com aulas em exatamente 4 dias (+20 pts/turma)"""
    score = 0
    for class_name in classes:
        days_used = {get_day(solution[(course, lesson)][0])
                    for course in cc[class_name] for lesson in [1, 2]}
        if len(days_used) == 4:
            score += 20
    return score


def _evaluate_room_usage(solution):
    """Critério 3: Minimização de salas por turma (-2 pts/sala)"""
    score = 0
    for class_name in classes:
        rooms_used = {solution[(course, lesson)][1]
                     for course in cc[class_name] for lesson in [1, 2]}
        score -= len(rooms_used) * 2
    return score


def _evaluate_consecutive_lessons(solution):
    """Critério 4: Aulas consecutivas no mesmo dia (+5 pts/dia)"""
    return sum(_check_class_consecutiveness(solution, class_name)
              for class_name in classes)


def _check_class_consecutiveness(solution, class_name):
    """Verifica consecutividade para uma turma"""
    slots_by_day = _group_slots_by_day(solution, class_name)
    return sum(5 for slots in slots_by_day.values()
              if len(slots) > 1 and _are_consecutive(sorted(slots)))


def _group_slots_by_day(solution, class_name):
    """Agrupa slots por dia para uma turma"""
    slots_by_day = {}
    for course in cc[class_name]:
        for lesson in [1, 2]:
            slot = solution[(course, lesson)][0]
            day = get_day(slot)
            slots_by_day.setdefault(day, []).append(slot)
    return slots_by_day


def _are_consecutive(slots):
    """Verifica se slots são consecutivos"""
    for i in range(1, len(slots)):
        if slots[i] - slots[i-1] != 1:
            return False
    return True


def display_schedule(solution):
    """
    Exibe o horário de forma organizada.
    
    Args:
        solution (dict): Solução a ser exibida
    """
    for class_name in classes:
        print(f"\nTurma {class_name}:")
        
        # Criar lista ordenada de lições
        schedule = [(get_day(solution[(course, lesson)][0]),
                    ((solution[(course, lesson)][0] - 1) % 4) + 1,
                    course, lesson, solution[(course, lesson)][1])
                   for course in cc[class_name] for lesson in [1, 2]]
        
        # Ordenar e exibir
        for day, slot_in_day, course, lesson, room in sorted(schedule):
            room_type = "[Online]" if room == 'Online' else f"[{room}]"
            print(f"  Dia {day}, Slot {slot_in_day}: {course}_L{lesson} {room_type}")


def analyze_solution(solution):
    """
    Análise detalhada da qualidade da solução.
    
    Args:
        solution (dict): Solução a analisar
    """
    print("\nANÁLISE DETALHADA DA SOLUÇÃO:")
    print("-" * 40)
    
    # Análise por critério
    score1 = _evaluate_course_distribution(solution)
    score2 = _evaluate_class_distribution(solution)
    score3 = _evaluate_room_usage(solution)
    score4 = _evaluate_consecutive_lessons(solution)
    
    print(f"Distribuição temporal: {score1} pontos")
    print(f"Distribuição semanal: {score2} pontos")
    print(f"Uso de salas: {score3} pontos")
    print(f"Consecutividade: {score4} pontos")
    print(f"TOTAL: {score1 + score2 + score3 + score4} pontos")


if __name__ == "__main__":
    print("Módulo de avaliação carregado.")
    print("Use as funções evaluate_solution() e display_schedule() para avaliar soluções.")