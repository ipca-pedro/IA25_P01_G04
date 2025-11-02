"""
Sistema de Agendamento de Aulas CSP - Versão Modular Otimizada

Orquestrador principal que integra todos os módulos do sistema CSP.
Este ficheiro coordena a execução sequencial de todas as fases:

1. Formulação do problema (csp_formulation)
2. Aplicação de restrições (csp_constraints)
3. Resolução hierárquica (csp_solver)
4. Avaliação e apresentação (csp_evaluation)

OTIMIZAÇÕES INTEGRADAS:
- Ordenação MRV (variáveis restritivas primeiro)
- Solver hierárquico (MinConflicts + Backtracking)

Autor: Grupo 04 - IA 2025/2026
"""

import time
import sys
from csp_formulation import create_csp_problem
from csp_constraints import apply_hard_constraints
from csp_evaluation import evaluate_solution
from dataset_loader import load_dataset_from_file, list_available_datasets


def select_dataset():
    """Permite ao utilizador selecionar um dataset"""
    datasets = list_available_datasets()
    
    if not datasets:
        print("[ERRO] Nenhum dataset encontrado na pasta 'material'")
        return None
    
    print("\n=== DATASETS DISPONÍVEIS ===")
    for i, dataset in enumerate(datasets, 1):
        print(f"{i}. {dataset}")
    
    try:
        choice = int(input(f"\nEscolha um dataset (1-{len(datasets)}): ")) - 1
        if 0 <= choice < len(datasets):
            return datasets[choice]
        else:
            print("[ERRO] Opção inválida")
            return None
    except ValueError:
        print("[ERRO] Por favor insira um número válido")
        return None

def find_initial_solution(problem):
    """Encontra primeira solução válida rapidamente"""
    from constraint import MinConflictsSolver, BacktrackingSolver
    problem.setSolver(MinConflictsSolver())
    solution = problem.getSolution()
    if not solution:
        problem.setSolver(BacktrackingSolver())
        solution = problem.getSolution()
    return solution

def timed_optimization(problem, initial_solution, dataset, time_limit=60):
    """Procura melhor solução durante time_limit segundos"""
    from constraint import MinConflictsSolver
    best_solution = initial_solution
    best_score = evaluate_solution(initial_solution, dataset)
    
    start_time = time.time()
    iterations = 0
    
    print(f"[INFO] Iniciando otimização por {time_limit}s (pontuação inicial: {best_score})")
    
    while time.time() - start_time < time_limit:
        problem.setSolver(MinConflictsSolver())
        solution = problem.getSolution()
        
        if solution:
            score = evaluate_solution(solution, dataset)
            if score > best_score:
                best_solution = solution
                best_score = score
                print(f"[MELHORIA] Nova melhor pontuação: {best_score} (iteração {iterations})")
        
        iterations += 1
        
        if iterations % 100 == 0:
            time.sleep(0.001)
    
    elapsed = time.time() - start_time
    print(f"[FINAL] Melhor pontuação: {best_score} após {iterations} iterações em {elapsed:.1f}s")
    
    return best_solution, best_score

def main(dataset_path=None):
    """
    Função principal com busca em duas fases:
    1. Encontra solução válida (hard constraints) e gera Excel
    2. Procura melhor pontuação durante 1 minuto
    """
    if dataset_path is None:
        dataset_path = select_dataset()
        if dataset_path is None:
            return
    
    print(f"\n[INFO] Carregando dataset: {dataset_path}")
    
    try:
        dataset = load_dataset_from_file(dataset_path)
        problem, variables_info = create_csp_problem(dataset)
        apply_hard_constraints(problem, variables_info, dataset)
        
        # FASE 1: Encontra solução inicial
        print("[FASE 1] Procurando solução inicial...")
        start_time = time.time()
        initial_solution = find_initial_solution(problem)
        initial_time = time.time() - start_time
        
        if not initial_solution:
            print("[ERRO] Nenhuma solução encontrada")
            return
        
        initial_score = evaluate_solution(initial_solution, dataset)
        print(f"[OK] Solução inicial encontrada em {initial_time:.3f}s (pontuação: {initial_score})")
        
        # Gera Excel da solução inicial
        from excel_export import export_to_excel
        excel_file = "Horario_Academico_Inicial.xlsx"
        export_to_excel(initial_solution, dataset, excel_file)
        
        # FASE 2: Otimização por 1 minuto
        print("\n[FASE 2] Otimizando por 1 minuto...")
        best_solution, best_score = timed_optimization(problem, initial_solution, dataset, 60)
        
        # Gera Excel da melhor solução se melhorou
        if best_score > initial_score:
            excel_file_best = "Horario_Academico_Otimizado.xlsx"
            export_to_excel(best_solution, dataset, excel_file_best)
            print(f"[OK] Melhor solução exportada para: {excel_file_best}")
        else:
            print("[INFO] Solução inicial já era ótima")
            
    except Exception as e:
        print(f"[ERRO] Falha ao processar dataset: {e}")


if __name__ == "__main__":
    # Permite especificar dataset via linha de comando
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()