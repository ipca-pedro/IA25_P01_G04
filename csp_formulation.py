"""
MÓDULO 2: FORMULAÇÃO CSP
Definição das variáveis, domínios e restrições do problema
"""

from dataset import *


def get_teacher(course):
    """Retorna o professor responsável por uma UC"""
    for teacher, teacher_courses in dsd.items():
        if course in teacher_courses:
            return teacher
    return None


def get_day(slot):
    """Converte slot (1-20) para dia (1-5)"""
    return (slot - 1) // 4 + 1


def get_domain(course, lesson_idx):
    """
    Calcula o domínio para uma variável (UC, lição).
    
    DOMÍNIO: Conjunto de valores possíveis
    - Formato: (slot_temporal, sala)
    - Considera restrições de professor e salas específicas
    """
    teacher = get_teacher(course)
    unavailable_slots = tr.get(teacher, [])
    
    domain = []
    for slot in range(1, 21):
        if slot not in unavailable_slots:
            if course in oc and oc[course] == lesson_idx:
                domain.append((slot, 'Online'))
            elif course in rr:
                domain.append((slot, rr[course]))
            else:
                for room in rooms:
                    if room != 'Online':
                        domain.append((slot, room))
    return domain


def create_variables():
    """
    Cria todas as variáveis do CSP.
    
    Returns:
        list: Lista de variáveis no formato (UC, lição)
    """
    variables = []
    for course in courses:
        for lesson in [1, 2]:
            variables.append((course, lesson))
    return variables


def analyze_formulation():
    """
    Analisa a formulação do CSP e exibe estatísticas.
    """
    variables = create_variables()
    
    print("="*60)
    print("FORMULAÇÃO CSP - AGENDAMENTO DE AULAS")
    print("="*60)
    
    print(f"\n1. VARIÁVEIS:")
    print(f"   Total: {len(variables)} variáveis")
    print(f"   Estrutura: 15 UCs × 2 lições = 30 variáveis")
    
    print(f"\n2. DOMÍNIOS:")
    total_combinations = 0
    for var in variables:
        domain = get_domain(var[0], var[1])
        total_combinations += len(domain)
    
    avg_domain = total_combinations / len(variables)
    print(f"   Média de valores por variável: {avg_domain:.1f}")
    print(f"   Espaço de busca: ~10^{len(str(total_combinations))}")
    
    print(f"\n3. RESTRIÇÕES HARD:")
    print(f"   - Unicidade de (slot, sala)")
    print(f"   - Conflitos de professores")
    print(f"   - Conflitos de turmas")
    print(f"   - Máximo 3 lições por dia")
    print(f"   - Coordenação aulas online")
    print(f"   - Limite aulas online por dia")
    
    print(f"\n4. RESTRIÇÕES SOFT:")
    print(f"   - Distribuição temporal (+10 pts/UC)")
    print(f"   - Distribuição semanal (+20 pts/turma)")
    print(f"   - Minimização salas (-2 pts/sala)")
    print(f"   - Consecutividade (+5 pts/dia)")
    
    print("="*60)
    return variables


if __name__ == "__main__":
    analyze_formulation()