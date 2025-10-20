"""
MÓDULO 1: DATASET E CONFIGURAÇÃO
Definição dos dados de entrada do problema de agendamento
"""

# Mapeamento de turmas para unidades curriculares
cc = {
    't01': ['UC11', 'UC12', 'UC13', 'UC14', 'UC15'],
    't02': ['UC21', 'UC22', 'UC23', 'UC24', 'UC25'],
    't03': ['UC31', 'UC32', 'UC33', 'UC34', 'UC35']
}

# Atribuição de UCs aos professores
dsd = {
    'jo': ['UC11', 'UC21', 'UC22', 'UC31'],
    'mike': ['UC12', 'UC23', 'UC32'],
    'rob': ['UC13', 'UC14', 'UC24', 'UC33'],
    'sue': ['UC15', 'UC25', 'UC34', 'UC35']
}

# Restrições de disponibilidade dos professores
tr = {
    'mike': [13, 14, 15, 16, 17, 18, 19, 20],
    'rob': [1, 2, 3, 4],
    'sue': [9, 10, 11, 12, 17, 18, 19, 20]
}

# Restrições de salas específicas
rr = {
    'UC14': 'Lab01',
    'UC22': 'Lab01'
}

# Aulas online
oc = {
    'UC21': 2,
    'UC31': 2
}

# Configuração do sistema
rooms = ['RoomA', 'RoomB', 'RoomC', 'Lab01', 'Online']
teachers = ['jo', 'mike', 'rob', 'sue']
classes = ['t01', 't02', 't03']
courses = [course for courses_list in cc.values() for course in courses_list]