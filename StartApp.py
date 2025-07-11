"""
Sistema de Análise Financeira B3 - Executável Principal
Execute este arquivo para iniciar o sistema interativo
"""

from financial_analysis import AnalisadorB3

def main():
    """Função principal"""
    print("🔧 Verificando configurações...")
    
    try:
        # Testar importações
        import matplotlib.pyplot as plt
        import yfinance as yf
        import pandas as pd
        import numpy as np
        
        print("✅ Todas as bibliotecas carregadas com sucesso!")
        
        # Iniciar sistema
        print("🚀 Iniciando Sistema de Análise Financeira B3...")
        analisador = AnalisadorB3()
        analisador.executar()
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("📥 Instale as dependências com: pip install -r requirements.txt")
        input("Pressione Enter para sair...")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
"""
Exemplo simples de uso do Analisador Financeiro
Execute este arquivo após instalar as dependências
"""

from financial_analysis import AnalisadorFinanceiro

print("🚀 Análise Rápida - Minhas Ações")
print("="*40)

# Escolha suas ações favoritas (adicione .SA para ações brasileiras)
minhas_acoes = [
    'PETR4.SA',  # Petrobras
    'VALE3.SA',  # Vale 
    'ITUB4.SA',  # Itaú
]

print("📥 Configurando análise...")

# SOLUÇÃO PARA GRÁFICOS: Forçar salvamento como PNG
print("⚙️  Configurando para salvar gráficos como PNG...")
analisador = AnalisadorFinanceiro(minhas_acoes, periodo='1y', salvar_graficos=True)

try:
    # Baixar dados e fazer análise básica
    print("📊 Baixando dados...")
    precos = analisador.baixar_dados()
    
    print("🔢 Calculando métricas...")
    analisador.calcular_retornos()
    analisador.calcular_medias_moveis()
    analisador.calcular_volatilidade()
    analisador.calcular_correlacoes()

    # Ver resumo
    print("\n📊 RESUMO DAS AÇÕES:")
    print("-" * 40)
    resumo = analisador.estatisticas_resumo()
    print(resumo)

    # === GERAR GRÁFICOS ===
    print(f"\n📈 Gerando gráficos...")
    print("💾 Todos os gráficos serão salvos na pasta 'graficos_financeiros'")
    
    # Gráficos principais
    print("📊 1/5 - Retornos Acumulados...")
    analisador.plotar_retornos_acumulados()
    
    print("🔗 2/5 - Matriz de Correlação...")
    analisador.plotar_correlacao()
    
    print("⚖️ 3/5 - Risco vs Retorno...")
    analisador.analise_risco_retorno()
    
    print("📊 4/5 - Volatilidade...")
    analisador.plotar_volatilidade()
    
    print("📈 5/5 - Preços e Médias Móveis (PETR4)...")
    analisador.plotar_precos_e_medias('PETR4')

    print("\n✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
    print("="*50)
    print("📁 Verifique a pasta 'graficos_financeiros' para ver os gráficos")
    print("📊 Arquivos PNG criados:")
    print("   • retornos_acumulados.png")
    print("   • correlacao.png") 
    print("   • risco_retorno.png")
    print("   • volatilidade.png")
    print("   • precos_medias_PETR4.png")

except Exception as e:
    print(f"\n❌ ERRO: {e}")
    print("\n🔧 SOLUÇÕES:")
    print("1. Verifique sua conexão com a internet")
    print("2. Execute: pip install -r requirements.txt")
    print("3. Execute: python solucao_graficos.py")

print(f"\n💡 PRÓXIMOS PASSOS:")
print("• Abra os arquivos PNG para ver os gráficos")
print("• Modifique as ações em 'minhas_acoes'")
print("• Teste diferentes períodos ('6mo', '2y', '5y')")
print("• Execute 'python solucao_graficos.py' se tiver problemas")