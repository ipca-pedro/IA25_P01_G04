"""
Formulação do Problema CSP - Criação de variáveis e domínios otimizados


1. Redução de domínios com restrições unárias (get_domain)
2. Ordenação de variáveis por MRV (Most Restrictive Variable)
3. Preferências de salas por turma para reduzir combinações

As otimizações transformam um problema com ~80^30 combinações teóricas
em um problema com ~40^30 combinações práticas, melhorando drasticamente
a performance do solver.

Autor: Grupo 04 - IA 2025/2026
"""

from constraint import Problem
from dataset import cc, dsd, tr, rr, oc, rooms, teachers, classes, courses


def get_teacher(course):
    """
    Retorna o professor responsável por uma unidade curricular.
    
    Args:
        course (str): Código da unidade curricular (ex: 'UC11', 'UC22')
        
    Returns:
        str: Nome do professor ('jo', 'mike', 'rob', 'sue') ou None se não encontrado
    """
    for teacher, teacher_courses in dsd.items():
        if course in teacher_courses:
            return teacher
    return None


def get_class(course):
    """
    Retorna a turma à qual uma unidade curricular pertence.
    
    Args:
        course (str): Código da unidade curricular (ex: 'UC11', 'UC22')
        
    Returns:
        str: Código da turma ('t01', 't02', 't03') ou None se não encontrado
    """
    for class_name, class_courses in cc.items():
        if course in class_courses:
            return class_name
    return None


def get_day(slot):
    """
    Converte um slot temporal para o dia da semana correspondente.
    
    Args:
        slot (int): Número do slot temporal (1-20)
        
    Returns:
        int: Dia da semana (1=Segunda, 2=Terça, 3=Quarta, 4=Quinta, 5=Sexta)
    """
    return (slot - 1) // 4 + 1


def get_domain(course, lesson_idx):
    """
    FUNÇÃO CRÍTICA: Calcula domínio otimizado com redução estratégica.
    
    Esta função implementa a otimização mais importante do sistema,
    reduzindo o espaço de busca de ~80 valores para ~40 valores por variável
    através da aplicação de restrições unárias durante a construção do domínio.
    
    Otimizações aplicadas:
    1. Filtragem por disponibilidade de professores
    2. Restrições de salas específicas (laboratórios)
    3. Configuração de aulas online
    4. Heurística de preferências de salas por turma
    
    Args:
        course (str): Código da unidade curricular (ex: 'UC11')
        lesson_idx (int): Número da lição (1 ou 2)
        
    Returns:
        list: Lista de tuplos (slot, sala) representando o domínio otimizado
    """
    # Obtém informações básicas da UC
    teacher = get_teacher(course)
    unavailable_slots = tr.get(teacher, [])  # Slots indisponíveis do professor
    class_name = get_class(course)  # Turma à qual a UC pertence
    
    domain = []
    # Itera sobre todos os 20 slots temporais (5 dias × 4 blocos)
    for slot in range(1, 21):
        # Filtra slots indisponíveis do professor (restrição unária)
        if slot not in unavailable_slots:
            # Verifica se esta lição específica é online (restrição unária)
            if course in oc and oc[course] == lesson_idx:
                domain.append((slot, 'Online'))
            # Verifica se a UC requer sala específica (restrição unária)
            elif course in rr:
                domain.append((slot, rr[course]))
            else:
                # OTIMIZAÇÃO CRÍTICA: Heurística de preferências de salas por turma
                # Reduz domínio de 4 salas para 2 salas por turma (redução de 50%)
                # Baseado na observação que turmas tendem a usar salas próximas
                if class_name == 't01':
                    preferred_rooms = ['RoomA', 'RoomB']  # Turma 1: salas A e B
                elif class_name == 't02':
                    preferred_rooms = ['RoomB', 'RoomC']  # Turma 2: salas B e C
                else:  # t03
                    preferred_rooms = ['RoomA', 'RoomC']  # Turma 3: salas A e C
                
                # Adiciona apenas salas preferenciais (não todas as 4 salas)
                for room in preferred_rooms:
                    domain.append((slot, room))
    return domain


def create_csp_problem():
    """
    Cria o problema CSP com otimizações de ordenação de variáveis.
    
    Implementa a heurística MRV (Most Restrictive Variable) que ordena
    as variáveis por nível de restrição, forçando o solver a resolver
    as partes mais difíceis primeiro e falhando rapidamente em
    atribuições impossíveis.
    
    Ordenação aplicada:
    1. Variáveis restritivas primeiro (labs específicos, aulas online)
    2. Variáveis regulares depois
    
    Returns:
        tuple: (problem, variables_info) onde:
            - problem: Instância do problema CSP
            - variables_info: Dicionário com variáveis organizadas por tipo
    """
    problem = Problem()
    
    # OTIMIZAÇÃO: Ordenação estratégica de variáveis (simulação da heurística MRV)
    # MRV (Minimum Remaining Values) = escolher variáveis com menor domínio primeiro
    # BENEFÍCIO: Falha rapidamente em atribuições impossíveis, reduzindo backtracking
    constrained_vars = []  # Variáveis com domínios pequenos (labs, online)
    regular_vars = []      # Variáveis com domínios normais
    
    for course in courses:
        for lesson in [1, 2]:
            var = (course, lesson)
            domain = get_domain(course, lesson)
            
            # CLASSIFICAÇÃO: Separa variáveis por nível de restrição
            # Variáveis restritivas: labs específicos (UC14→Lab01) e aulas online
            if course in rr or (course in oc and oc[course] == lesson):
                constrained_vars.append((var, domain))
            else:
                regular_vars.append((var, domain))
    
    # ESTRATÉGIA MRV: Adiciona variáveis restritivas primeiro
    # Isto força o solver a resolver as partes mais difíceis primeiro
    all_variables = []
    for var, domain in constrained_vars + regular_vars:
        all_variables.append(var)
        problem.addVariable(var, domain)
    
    # Organiza variáveis por tipo para aplicação eficiente de restrições
    # Cada tipo de restrição precisa de conjuntos específicos de variáveis
    # Variáveis físicas (excluindo online) para restrições de unicidade de sala
    physical_vars = [v for v in all_variables 
                    if not any('Online' in val[1] for val in get_domain(v[0], v[1]))]
    
    # Variáveis por professor para restrições de conflito de professores
    teacher_vars = {}
    for teacher in teachers:
        teacher_vars[teacher] = [(course, lesson) for course in dsd[teacher] for lesson in [1, 2]]
    
    # Variáveis por turma para restrições de conflito de turmas e limites diários
    class_vars = {}
    for class_name in classes:
        class_vars[class_name] = [(course, lesson) for course in cc[class_name] for lesson in [1, 2]]
    
    # Variáveis online para restrições de coordenação e limites online
    online_vars = [(course, lesson) for course in courses for lesson in [1, 2]
                   if course in oc and oc[course] == lesson]
    
    variables_info = {
        'all_variables': all_variables,
        'physical_vars': physical_vars,
        'teacher_vars': teacher_vars,
        'class_vars': class_vars,
        'online_vars': online_vars
    }
    
    # Variáveis adicionadas silenciosamente
    
    return problem, variables_info