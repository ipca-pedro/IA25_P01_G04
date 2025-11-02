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