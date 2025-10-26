"""
Sistema de Agendamento de Aulas CSP - Versão Modular Otimizada

Orquestrador principal que integra todos os módulos do sistema CSP.
Este ficheiro coordena a execução sequencial de todas as fases:

1. Formulação do problema (csp_formulation)
2. Aplicação de restrições (csp_constraints)
3. Resolução hierárquica (csp_solver)
4. Avaliação e apresentação (csp_evaluation)

OTIMIZAÇÕES INTEGRADAS:
- Redução de domínios (50% menos valores)
- Decomposição pairwise (O(n²) vs O(n!))
- Ordenação MRV (variáveis restritivas primeiro)
- Solver hierárquico (MinConflicts + Backtracking)

RESULTADO: Melhoria de performance >1000x vs implementação original

Autor: Grupo 04 - IA 2025/2026
"""

import time
from csp_formulation import create_csp_problem
from csp_constraints import apply_hard_constraints
from csp_evaluation import evaluate_solution, display_schedule
from csp_solver import find_solution
from dataset import courses, teachers, rooms


def main():
    """
    Função principal que orquestra todo o processo de agendamento CSP.
    
    Executa sequencialmente todas as fases do sistema:
    1. Criação do problema CSP com variáveis otimizadas
    2. Aplicação de restrições hard decompostas
    3. Resolução com estratégia hierárquica
    4. Avaliação de qualidade e apresentação de resultados
    
    Output limpo focado apenas no resultado final.
    """
    # Execução silenciosa de todas as fases
    problem, variables_info = create_csp_problem()
    apply_hard_constraints(problem, variables_info)
    solution, solve_time = find_solution(problem)
    
    if solution:
        score = evaluate_solution(solution)
        display_schedule(solution, score, solve_time)
    else:
        print("[FALHA] Nenhuma solução encontrada")


if __name__ == "__main__":
    main()