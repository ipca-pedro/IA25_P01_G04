"""
MÓDULO 4: RESOLUÇÃO CSP
Algoritmos de busca e resolução do problema
"""

import time
import sys
import traceback
from csp_constraints import create_csp_problem


def solve_csp():
    """
    Resolve o problema CSP e retorna a solução encontrada.
    
    Returns:
        tuple: (solution, solve_time) ou (None, solve_time)
    """
    print("Iniciando resolução CSP...")
    
    # Criar problema
    problem, variables = create_csp_problem()
    
    print(f"Variáveis: {len(variables)}")
    print(f"Procurando solução...")
    
    start_time = time.time()
    
    try:
        solution = problem.getSolution()
        solve_time = time.time() - start_time
        
        if solution:
            print(f"[OK] Solução encontrada em {solve_time:.3f} segundos")
            return solution, solve_time
        else:
            print(f"[ERRO] Nenhuma solução encontrada em {solve_time:.3f} segundos")
            return None, solve_time
            
    except KeyboardInterrupt:
        print("\n[AVISO] Execução interrompida pelo utilizador")
        sys.exit(1)
    except Exception as e:
        solve_time = time.time() - start_time
        print(f"\n[ERRO] Erro durante resolução: {e}")
        print(f"Tempo decorrido: {solve_time:.3f} segundos")
        traceback.print_exc()
        return None, solve_time


def solve_and_display():
    """
    Resolve o CSP e exibe os resultados.
    """
    solution, solve_time = solve_csp()
    
    if solution:
        from csp_evaluation import evaluate_solution, display_schedule
        
        # Avaliar qualidade
        score = evaluate_solution(solution)
        
        # Exibir resultados
        print(f"\n{'='*60}")
        print(f"SOLUÇÃO ENCONTRADA (Pontuação: {score})")
        print(f"{'='*60}")
        
        display_schedule(solution)
        
        print(f"\nPontuação final: {score}")
        print(f"Tempo de execução: {solve_time:.3f} segundos")
        print("\n[OK] Execução concluída com sucesso!")
    else:
        print("\n[ERRO] Nenhuma solução foi encontrada!")


if __name__ == "__main__":
    solve_and_display()