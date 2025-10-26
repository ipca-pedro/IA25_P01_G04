"""
Solver CSP - Estratégia hierárquica otimizada

Este módulo implementa a estratégia de resolução hierárquica que combina
dois algoritmos complementares para maximizar a eficiência:

1. MinConflictsSolver (Primeira tentativa):
   - Algoritmo de busca local muito rápido
   - Ideal para encontrar soluções rapidamente
   - Pode não encontrar solução se ficar preso em mínimo local

2. BacktrackingSolver (Fallback):
   - Busca sistemática completa
   - Mais lento mas garante encontrar solução se existir
   - Usado apenas se MinConflicts falhar

ESTRATÉGIA: "Rápido primeiro, completo se necessário"
RESULTADO: Combina velocidade com garantia de completude

Autor: Grupo 04 - IA 2025/2026
"""

import time
import sys
import traceback
from constraint import MinConflictsSolver, BacktrackingSolver


def find_solution(problem):
    """
    Executa a estratégia de resolução hierárquica otimizada.
    
    Implementa uma abordagem de dois níveis que maximiza a eficiência:
    1. Tenta MinConflictsSolver primeiro (rápido, busca local)
    2. Se falhar, usa BacktrackingSolver (lento, busca completa)
    
    Esta estratégia aproveita o melhor de ambos os mundos:
    - Velocidade do MinConflicts para casos fáceis
    - Completude do Backtracking para casos difíceis
    
    Args:
        problem: Instância do problema CSP configurado com variáveis e restrições
        
    Returns:
        tuple: (solution, solve_time) onde:
            - solution: Dicionário com atribuições ou None se não encontrar
            - solve_time: Tempo de execução em segundos
    """
    print("Procurando solução com algoritmos otimizados...")
    start_time = time.time()  # Início da medição de tempo
    
    try:
        # ESTRATÉGIA 1: MinConflictsSolver (Algoritmo de busca local)
        # VANTAGENS: Muito rápido, ideal para problemas grandes
        # DESVANTAGENS: Pode ficar preso em mínimos locais
        print("Tentando MinConflictsSolver...")
        problem.setSolver(MinConflictsSolver())
        solution = problem.getSolution()
        
        if not solution:
            # ESTRATÉGIA 2: BacktrackingSolver (Busca sistemática completa)
            # VANTAGENS: Garante encontrar solução se existir
            # DESVANTAGENS: Mais lento, especialmente para problemas grandes
            print("MinConflicts falhou, tentando BacktrackingSolver...")
            problem.setSolver(BacktrackingSolver())
            solution = problem.getSolution()
        
        solve_time = time.time() - start_time  # Calcula tempo total
        
        if solution:
            # Determina qual solver foi usado baseado no tempo (heurística)
            solver_used = 'MinConflicts' if solve_time < 1 else 'Backtracking'
            print(f"[OK] Solução encontrada em {solve_time:.3f} segundos")
            print(f"Solver usado: {solver_used}")
            return solution, solve_time
        else:
            # Nenhuma solução encontrada mesmo com ambos os algoritmos
            print(f"[ERRO] Nenhuma solução encontrada em {solve_time:.3f} segundos")
            print("Possíveis causas (mesmo com otimizações):")
            print("- Restrições muito restritivas (hard constraints incompatíveis)")
            print("- Conflitos entre restrições de salas")
            print("- Disponibilidade de professores muito limitada")
            print("- Domínios reduzidos excessivamente (tentar menos preferências)")
            return None, solve_time
            
    except KeyboardInterrupt:
        # Tratamento de interrupção pelo utilizador (Ctrl+C)
        solve_time = time.time() - start_time
        print(f"\n[AVISO] Execução interrompida pelo utilizador em {solve_time:.3f}s")
        print("NOTA: Com as otimizações, o tempo normal é <1 segundo")
        return None, solve_time
        
    except Exception as e:
        # Tratamento de erros inesperados durante a resolução
        solve_time = time.time() - start_time
        print(f"\n[ERRO] Erro durante resolução otimizada: {e}")
        print(f"Tipo de erro: {type(e).__name__}")
        print("\nDEBUG - Possíveis causas:")
        print("- Conflito nas otimizações de domínio")
        print("- Incompatibilidade entre restrições pairwise")
        print("- Problema na configuração do solver")
        print("\nDetalhes técnicos:")
        traceback.print_exc()
        return None, solve_time