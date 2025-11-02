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
from csp_evaluation import evaluate_solution, display_schedule
from csp_solver import find_solution
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

def main(dataset_path=None):
    """
    Função principal que orquestra todo o processo de agendamento CSP.
    
    Args:
        dataset_path: Caminho para o dataset (opcional, se None pede ao utilizador)
    """
    # Seleção do dataset
    if dataset_path is None:
        dataset_path = select_dataset()
        if dataset_path is None:
            return
    
    print(f"\n[INFO] Carregando dataset: {dataset_path}")
    
    try:
        # Carrega dataset dinâmico
        dataset = load_dataset_from_file(dataset_path)
        
        # Execução das fases CSP
        problem, variables_info = create_csp_problem(dataset)
        apply_hard_constraints(problem, variables_info, dataset)
        solution, solve_time = find_solution(problem)
        
        if solution:
            score = evaluate_solution(solution, dataset)
            display_schedule(solution, score, solve_time, dataset)
            
            # Busca otimizada com controlo de qualidade
            print("\n[INFO] Iniciando busca otimizada...")
            from csp_solver import find_optimal_solution
            
            # Cria novo problema para busca otimizada
            problem_opt, _ = create_csp_problem(dataset)
            apply_hard_constraints(problem_opt, variables_info, dataset)
            
            optimal_solution, optimal_time = find_optimal_solution(problem_opt, dataset)
            
            if optimal_solution:
                optimal_score = evaluate_solution(optimal_solution, dataset)
                print(f"[RESULT] Melhor solução: {optimal_score} pts em {optimal_time:.3f}s")
            else:
                print("[FALHA] Nenhuma solução ótima encontrada")
        else:
            print("[FALHA] Nenhuma solução encontrada")
            
    except Exception as e:
        print(f"[ERRO] Falha ao processar dataset: {e}")


if __name__ == "__main__":
    # Permite especificar dataset via linha de comando
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()