"""
Versão de debug para identificar problemas nas restrições
"""

from constraint import *
import time

# Dataset simplificado
cc = {
    't01': ['UC11', 'UC12', 'UC13', 'UC14', 'UC15'],
    't02': ['UC21', 'UC22', 'UC23', 'UC24', 'UC25'],
    't03': ['UC31', 'UC32', 'UC33', 'UC34', 'UC35']
}

dsd = {
    'jo': ['UC11', 'UC21', 'UC22', 'UC31'],
    'mike': ['UC12', 'UC23', 'UC32'],
    'rob': ['UC13', 'UC14', 'UC24', 'UC33'],
    'sue': ['UC15', 'UC25', 'UC34', 'UC35']
}

# Restrições de professores REDUZIDAS para teste
tr = {
    'mike': [17, 18, 19, 20],  # Apenas dia 5 indisponível
    'rob': [1, 2, 3, 4],       # Apenas dia 1 indisponível
    'sue': [17, 18, 19, 20]    # Apenas dia 5 indisponível
}

rr = {
    'UC14': 'Lab01',
    'UC22': 'Lab01'
}

# SEM aulas online para simplificar
oc = {}

rooms = ['RoomA', 'RoomB', 'RoomC', 'Lab01']
teachers = ['jo', 'mike', 'rob', 'sue']
classes = ['t01', 't02', 't03']
courses = [course for courses_list in cc.values() for course in courses_list]

def get_teacher(course):
    for teacher, teacher_courses in dsd.items():
        if course in teacher_courses:
            return teacher
    return None

def get_day(slot):
    return (slot - 1) // 4 + 1

def get_domain(course, lesson_idx):
    teacher = get_teacher(course)
    unavailable_slots = tr.get(teacher, [])
    
    domain = []
    for slot in range(1, 21):
        if slot not in unavailable_slots:
            if course in rr:
                domain.append((slot, rr[course]))
            else:
                for room in rooms:
                    if room != 'Online':
                        domain.append((slot, room))
    return domain

# Criar problema
problem = Problem()

# Adicionar variáveis
variables = []
print("=== ANÁLISE DE DOMÍNIOS ===")
for course in courses:
    for lesson in [1, 2]:
        var = (course, lesson)
        variables.append(var)
        domain = get_domain(course, lesson)
        problem.addVariable(var, domain)
        print(f"{var}: {len(domain)} valores")

print(f"\nTotal de variáveis: {len(variables)}")

# APENAS restrições básicas
print("\n=== ADICIONANDO RESTRIÇÕES ===")

# 1. Unicidade
problem.addConstraint(AllDifferentConstraint(), variables)
print("✓ Restrição de unicidade adicionada")

# 2. Professores
for teacher in teachers:
    teacher_vars = [(course, lesson) for course in dsd[teacher] for lesson in [1, 2]]
    if teacher_vars:
        problem.addConstraint(
            lambda *assignments: len(set(slot for slot, room in assignments)) == len(assignments),
            teacher_vars
        )
        print(f"✓ Restrição de professor {teacher} adicionada ({len(teacher_vars)} variáveis)")

# 3. Turmas
for class_name in classes:
    class_vars = [(course, lesson) for course in cc[class_name] for lesson in [1, 2]]
    problem.addConstraint(
        lambda *assignments: len(set(slot for slot, room in assignments)) == len(assignments),
        class_vars
    )
    print(f"✓ Restrição de turma {class_name} adicionada ({len(class_vars)} variáveis)")

print("\n=== PROCURANDO SOLUÇÃO ===")
start_time = time.time()

try:
    solution = problem.getSolution()
    solve_time = time.time() - start_time
    
    if solution:
        print(f"✅ SOLUÇÃO ENCONTRADA em {solve_time:.3f} segundos!")
        
        # Mostrar resultado resumido
        for class_name in classes:
            print(f"\nTurma {class_name}:")
            for course in cc[class_name]:
                for lesson in [1, 2]:
                    slot, room = solution[(course, lesson)]
                    day = get_day(slot)
                    slot_in_day = ((slot - 1) % 4) + 1
                    print(f"  {course}_L{lesson}: Dia {day}, Slot {slot_in_day}, {room}")
    else:
        print("❌ NENHUMA SOLUÇÃO ENCONTRADA")
        
except Exception as e:
    print(f"❌ ERRO: {e}")

print(f"\nTempo total: {time.time() - start_time:.3f} segundos")