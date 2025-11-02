"""
Avaliação de Soluções CSP - Restrições Soft e Formatação de Resultados

Este módulo implementa o sistema de avaliação de qualidade das soluções CSP
através de restrições soft (preferências) que não são obrigatórias mas
melhoram a qualidade prática do horário gerado.

SISTEMA DE PONTUAÇÃO (4 critérios):
1. Distribuição temporal: Lições da mesma UC em dias diferentes (+10 pts/UC)
2. Distribuição semanal: Turmas com aulas em exatamente 4 dias (+20 pts/turma)
3. Minimização de salas: Menos salas por turma (-2 pts/sala)
4. Consecutividade: Aulas consecutivas no mesmo dia (+5 pts/dia)

"""

from csp_formulation import get_day


def evaluate_solution(solution, dataset):
    """
    Sistema de avaliação principal baseado em restrições soft
    
    Avalia a qualidade prática de uma solução CSP válida através de
    4 critérios. Todas as hard constraints já estão satisfeitas
    este sistema mede quão boa é a solução na prática
    
    Args:
        solution (dict): Solução CSP {(course, lesson): (slot, room)}
        
    Returns:
        int: Pontuação total (maior = melhor qualidade)
             Faixa típica: 50-150 pontos
    """
    score = 0
    score += _evaluate_course_distribution(solution, dataset)
    score += _evaluate_class_distribution(solution, dataset)
    score += _evaluate_room_usage(solution, dataset)
    # score += _evaluate_consecutive_lessons(solution, dataset)  # Agora é hard constraint
    return score


def _evaluate_course_distribution(solution, dataset):
    """
    CRITÉRIO 1: Distribuição temporal das lições por UC.
    
    OBJETIVO: Lições da mesma UC em dias diferentes
    - Melhora assimilação do conteúdo (espaçamento temporal)
    - Evita sobrecarga de uma disciplina num só dia
    - Permite revisão entre lições
    
    PONTUAÇÃO: +10 pontos por cada UC com lições em dias distintos
    MÁXIMO POSSÍVEL: 15 UCs × 10 pts = 150 pontos
    
    Args:
        solution (dict): Solução CSP a avaliar
        
    Returns:
        int: Pontuação parcial (0-150)
    """
    score = 0
    # Verifica cada UC individualmente
    for course in dataset['courses']:
        lesson1_slot = solution[(course, 1)][0]  # Slot da lição 1
        lesson2_slot = solution[(course, 2)][0]  # Slot da lição 2
        # Premia se as lições estão em dias diferentes
        if get_day(lesson1_slot) != get_day(lesson2_slot):
            score += 10  # +10 pontos por UC bem distribuída
    return score


def _evaluate_class_distribution(solution, dataset):
    """
    CRITÉRIO 2: Distribuição semanal ideal por turma.
    
    OBJETIVO: Turmas com aulas em exatamente 4 dias
    PONTUAÇÃO: +20 pontos por turma com aulas em exatamente 4 dias
    MÁXIMO POSSÍVEL: 3 turmas × 20 pts = 60 pontos
    
    Args:
        solution (dict): Solução CSP a avaliar
        
    Returns:
        int: Pontuação parcial (0-60)
    """
    score = 0
    # Verifica cada turma individualmente
    for class_name in dataset['classes']:
        # Calcula conjunto de dias utilizados pela turma
        days_used = {get_day(solution[(course, lesson)][0])
                    for course in dataset['cc'][class_name] for lesson in [1, 2]}
        # Premia se a turma usa exatamente 4 dias (ideal)
        if len(days_used) == 4:
            score += 20  # +20 pontos por turma bem distribuída
    return score


def _evaluate_room_usage(solution, dataset):
    """
    CRITÉRIO 3: Minimização do uso de salas (penalização).
    
    OBJETIVO: Concentrar turmas em menos salas    
    PONTUAÇÃO: -2 pontos por cada sala diferente usada por turma
    MÍNIMO POSSÍVEL: 3 turmas × 2 salas × (-2) = -12 pontos (ideal)
    MÁXIMO NEGATIVO: 3 turmas × 5 salas × (-2) = -30 pontos (pior caso)
    
    Args:
        solution (dict): Solução CSP a avaliar
        
    Returns:
        int: Pontuação parcial (negativa, -12 a -30)
    """
    score = 0
    # Penaliza cada turma pelo número de salas utilizadas
    for class_name in dataset['classes']:
        # Calcula conjunto de salas utilizadas pela turma
        rooms_used = {solution[(course, lesson)][1]
                     for course in dataset['cc'][class_name] for lesson in [1, 2]}
        # Penalização: -2 pontos por sala utilizada
        score -= len(rooms_used) * 2  # Incentiva concentração em poucas salas
    return score


def _evaluate_consecutive_lessons(solution, dataset):
    """
    CRITÉRIO 4: Consecutividade de aulas (compactação).
    
    OBJETIVO: Aulas consecutivas no mesmo dia
    PONTUAÇÃO: +5 pontos por cada dia com aulas consecutivas
    MÁXIMO POSSÍVEL: Variável (depende da distribuição)
    
    Args:
        solution (dict): Solução CSP a avaliar
        
    Returns:
        int: Pontuação parcial (0+)
    """
    # Removido - consecutividade agora é hard constraint
    return 0


def _check_class_consecutiveness(solution, class_name, dataset):
    """
    Verifica a consecutividade de aulas para uma turma específica.
    
    Analisa cada dia individualmente para determinar se as aulas
    da turma nesse dia são consecutivas (sem "janelas").
    
    Args:
        solution (dict): Solução a ser avaliada
        class_name (str): Código da turma ('t01', 't02', 't03')
        
    Returns:
        int: Pontuação parcial para esta turma
    """
    slots_by_day = _group_slots_by_day(solution, class_name, dataset)
    # Premia cada dia com aulas consecutivas
    return sum(5 for slots in slots_by_day.values()
              if len(slots) > 1 and _are_consecutive(sorted(slots)))


def _group_slots_by_day(solution, class_name, dataset):
    """
    Agrupa os slots de uma turma por dia da semana.
    
    Organiza as aulas de uma turma por dia para facilitar
    a análise de consecutividade.
    
    Args:
        solution (dict): Solução a ser avaliada
        class_name (str): Código da turma
        
    Returns:
        dict: Dicionário {dia: [slots]} com slots agrupados por dia
    """
    slots_by_day = {}  # Dicionário para agrupar por dia
    # Itera sobre todas as lições da turma
    for course in dataset['cc'][class_name]:
        for lesson in [1, 2]:
            slot = solution[(course, lesson)][0]  # Obtém slot da lição
            day = get_day(slot)  # Converte slot para dia
            # Adiciona slot à lista do dia correspondente
            slots_by_day.setdefault(day, []).append(slot)
    return slots_by_day


def _are_consecutive(slots):
    """
    Verifica se uma lista de slots é consecutiva.
    
    Determina se não existem "janelas" (slots vazios) entre
    as aulas de uma turma num determinado dia.
    
    Args:
        slots (list): Lista de slots ordenada
        
    Returns:
        bool: True se todos os slots são consecutivos
    """
    # Verifica se cada slot é imediatamente seguido pelo próximo
    for i in range(1, len(slots)):
        if slots[i] - slots[i-1] != 1:  # Se não são consecutivos
            return False  # Existe "janela" entre aulas
    return True  # Todos os slots são consecutivos


def display_schedule(solution, score, solve_time, dataset):
    """
    Exibe o horário final de forma limpa e focada.
    
    Apresenta apenas o sumário de sucesso e o horário organizado por turma,
    sem cabeçalhos verbosos ou análises detalhadas.
    
    Args:
        solution (dict): Solução CSP {(course, lesson): (slot, room)}
        score (int): Pontuação de qualidade calculada
        solve_time (float): Tempo de execução em segundos
    """
    # Sumário de sucesso numa linha
    print(f"[OK] Solução encontrada (Pontuação: {score}) em {solve_time:.3f}s")
    
    # Horário organizado por turma
    for class_name in dataset['classes']:
        print(f"\nTurma {class_name}:")
        
        # Cria lista de lições com informação completa para ordenação
        schedule = [(get_day(solution[(course, lesson)][0]),  # Dia da semana
                    ((solution[(course, lesson)][0] - 1) % 4) + 1,  # Slot no dia
                    course, lesson, solution[(course, lesson)][1])  # UC, lição, sala
                   for course in dataset['cc'][class_name] for lesson in [1, 2]]
        
        # Ordena cronologicamente e exibe
        for day, slot_in_day, course, lesson, room in sorted(schedule):
            room_type = "[Online]" if room == 'Online' else f"[{room}]"
            print(f"  Dia {day}, Slot {slot_in_day}: {course}_L{lesson} {room_type}")