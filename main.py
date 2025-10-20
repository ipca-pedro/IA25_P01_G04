"""
SISTEMA DE AGENDAMENTO DE AULAS - CSP
Arquivo principal que integra todos os módulos

Módulos:
1. dataset.py - Dados de entrada
2. csp_formulation.py - Formulação do CSP
3. csp_constraints.py - Restrições
4. csp_solver.py - Resolução
5. csp_evaluation.py - Avaliação

Uso:
    python main.py
"""

import sys
from csp_formulation import analyze_formulation
from csp_solver import solve_and_display


def main():
    """
    Função principal que executa o sistema completo.
    """
    print("="*80)
    print("SISTEMA DE AGENDAMENTO DE AULAS USANDO CSP")
    print("Grupo 04 - Inteligência Artificial 2024/2025 - IPCA")
    print("="*80)
    
    try:
        # Opção do utilizador
        print("\nEscolha uma opção:")
        print("1. Analisar formulação CSP (FASE 1)")
        print("2. Resolver problema completo (FASE 2)")
        print("3. Executar tudo")
        
        choice = input("\nOpção (1/2/3): ").strip()
        
        if choice == "1":
            print("\n" + "="*60)
            print("EXECUTANDO FASE 1: ANÁLISE DA FORMULAÇÃO")
            print("="*60)
            analyze_formulation()
            
        elif choice == "2":
            print("\n" + "="*60)
            print("EXECUTANDO FASE 2: RESOLUÇÃO DO PROBLEMA")
            print("="*60)
            solve_and_display()
            
        elif choice == "3":
            print("\n" + "="*60)
            print("EXECUTANDO FASE 1: ANÁLISE DA FORMULAÇÃO")
            print("="*60)
            analyze_formulation()
            
            input("\nPressione Enter para continuar para a Fase 2...")
            
            print("\n" + "="*60)
            print("EXECUTANDO FASE 2: RESOLUÇÃO DO PROBLEMA")
            print("="*60)
            solve_and_display()
            
        else:
            print("Opção inválida!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nExecução interrompida pelo utilizador.")
        sys.exit(0)
    except Exception as e:
        print(f"\nErro na execução: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()