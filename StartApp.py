"""
Sistema de Análise Financeira B3 - Executável Principal
Execute este arquivo para iniciar o sistema interativo
"""

from financial_analysis import AnalisadorB3
import os

def main():
    """Função principal"""    
    try:
        # Testar importações
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Verificando configurações...")
        import matplotlib.pyplot as plt
        import yfinance as yf
        import pandas as pd
        import numpy as np
        
        print("Todas as bibliotecas carregadas com sucesso!")
        
        # Iniciar sistema
        print("🚀 Iniciando Sistema de Análise Financeira B3...")
        analisador = AnalisadorB3()
        analisador.executar()
        
    except ImportError as e:
        print(f"Erro de importação: {e}")
        print("Instale as dependências com: pip install -r requirements.txt")
        input("Pressione Enter para sair...")
    except Exception as e:
        print(f"Erro inesperado: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
