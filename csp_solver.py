"""
Solver CSP - Estratégia hierárquica otimizada

Este módulo implementa a estratégia de resolução hierárquica que combina
dois algoritmos complementares para maximizar a eficiência:

1. MinConflictsSolver (Primeira tentativa):
   - Algoritmo de busca local
   - Ideal para encontrar soluções rapidamente
   - Pode não encontrar solução se ficar preso em mínimo local

2. BacktrackingSolver (Fallback):
   - Busca sistemática completa
   - Mais lento mas garante encontrar solução se existir
   - Usado apenas se MinConflicts falhar
"""

import time

from constraint import MinConflictsSolver, BacktrackingSolver


def find_solution(problem):
    """
    Executa a estratégia de resolução hierárquica otimizada.
    
    Implementa uma abordagem de dois níveis:
    1. Tenta MinConflictsSolver primeiro (rápido, busca local)
    2. Se falhar, usa BacktrackingSolver (lento, busca completa)
    
    Esta estratégia aproveita o melhor de ambos:
    - Velocidade do MinConflicts para casos fáceis
    - Completude do Backtracking para casos difíceis
    
    Args:
        problem: Instância do problema CSP configurado com variáveis e restrições
        
    Returns:
        tuple: (solution, solve_time) onde:
            - solution: Dicionário com atribuições ou None se não encontrar
            - solve_time: Tempo de execução em segundos
    """
    start_time = time.time()  # Início da medição de tempo
    
    try:
        # ESTRATÉGIA 1: MinConflictsSolver (Algoritmo de busca local)
        problem.setSolver(MinConflictsSolver())
        solution = problem.getSolution()
        
        if not solution:
            # ESTRATÉGIA 2: BacktrackingSolver (Busca sistemática completa)
            problem.setSolver(BacktrackingSolver())
            solution = problem.getSolution()
        
        solve_time = time.time() - start_time  # Calcula tempo total
        return solution, solve_time
            
    except KeyboardInterrupt:
        # Tratamento de interrupção pelo utilizador (Ctrl+C)
        solve_time = time.time() - start_time
        return None, solve_time
        
    except Exception as e:
        # Tratamento de erros inesperados durante a resolução
        solve_time = time.time() - start_time
        return None, solve_time


def find_optimal_solution(problem, dataset):
    """
    Busca obrigatória por solução >= 240 pts, depois procura ótima >= 336 pts
    """
    from csp_evaluation import evaluate_solution
    from excel_export import export_to_excel
    
    start_time = time.time()
    problem.setSolver(BacktrackingSolver())
    
    best_solution = None
    best_score = 0
    min_240_exported = False
    
    try:
        for solution in problem.getSolutionIter():
            score = evaluate_solution(solution, dataset)
            
            if score > best_score:
                best_solution = solution
                best_score = score
            
            # OBRIGATÓRIO: Continua até encontrar >= 240 e exportar
            if not min_240_exported and score >= 240:
                export_to_excel(solution, dataset, "horario_qualidade_minima_240.xlsx")
                print(f"[EXPORT] Qualidade mínima atingida: {score} pts")
                min_240_exported = True
                # Continua procura pela ótima
            
            # Solução ótima >= 336 - termina
            if score >= 336:
                export_to_excel(solution, dataset, "horario_soft_constraints_maximo_336.xlsx")
                print(f"[OPTIMAL] Solução ótima encontrada: {score} pts")
                solve_time = time.time() - start_time
                return solution, solve_time
    
    except KeyboardInterrupt:
        pass
    
    solve_time = time.time() - start_time
    
    # Se terminou sem encontrar >= 240, força exportação da melhor
    if not min_240_exported and best_solution:
        export_to_excel(best_solution, dataset, "horario_melhor_encontrada.xlsx")
        print(f"[EXPORT] Melhor solução encontrada: {best_score} pts")
    
    return best_solution, solve_time