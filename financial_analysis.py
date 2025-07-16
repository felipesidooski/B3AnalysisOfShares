"""
Sistema de Análise Financeira B3 - Menu Interativo
Análise das maiores empresas brasileiras e estrangeiras da B3
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates
import seaborn as sns
import yfinance as yf
from datetime import datetime, timedelta
import warnings
import sys
import os

warnings.filterwarnings('ignore')

# Configurar matplotlib para exibir gráficos na tela
matplotlib.use('TkAgg')  # Backend mais compatível
plt.ion()  # Modo interativo ativado

# Configurações para gráficos
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

class AnalisadorB3:
    def __init__(self):
        """Inicializa o analisador da B3"""
        
        # 10 maiores empresas brasileiras na B3
        self.empresas_brasileiras = {
            1: ("Petrobras", "PETR4.SA"),
            2: ("Vale", "VALE3.SA"),
            3: ("Itaú Unibanco", "ITUB4.SA"),
            4: ("Banco do Brasil", "BBAS3.SA"),
            5: ("Bradesco", "BBDC4.SA"),
            6: ("Ambev", "ABEV3.SA"),
            7: ("Magazine Luiza", "MGLU3.SA"),
            8: ("WEG", "WEGE3.SA"),
            9: ("JBS", "JBSS3.SA"),
            10: ("Suzano", "SUZB3.SA")
        }
        
        # 10 maiores empresas estrangeiras na B3 (BDRs)
        self.empresas_estrangeiras = {
            1: ("Apple", "AAPL34.SA"),
            2: ("Microsoft", "MSFT34.SA"),
            3: ("Amazon", "AMZO34.SA"),
            4: ("Google/Alphabet", "GOGL34.SA"),
            5: ("Tesla", "TSLA34.SA"),
            6: ("Meta/Facebook", "FBOK34.SA"),
            7: ("Netflix", "NFLX34.SA"),
            8: ("Nvidia", "NVDC34.SA"),
            9: ("Coca-Cola", "COCA34.SA"),
            10: ("Disney", "DISB34.SA")
        }
        
        self.acao_atual = None
        self.dados_acao = None
        self.nome_empresa = None
    
    def limpar_tela(self):
        """Limpa a tela do console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def aguardar_fechamento_grafico(self):
        """Aguarda o usuário fechar o gráfico para continuar"""
        print("\n Gráfico interativo exibido na tela!")
        print("  Passe o mouse sobre os pontos para ver os valores")
        print("  Feche a janela do gráfico para continuar...")
        
        # Aguarda todas as figuras serem fechadas
        while plt.get_fignums():
            plt.pause(0.1)
        
        print("✅ Gráfico fechado. Continuando...")
    
    def adicionar_interatividade(self, ax, dados, formato_valor=":.2f", prefixo="", sufixo=""):
        """Adiciona interatividade ao gráfico para mostrar valores com o mouse"""
        
        def on_hover(event):
            if event.inaxes == ax:
                # Remover anotações anteriores
                for child in ax.get_children():
                    if hasattr(child, 'get_text') and child.get_text().startswith('📊'):
                        child.remove()
                
                # Encontrar ponto mais próximo
                if hasattr(event, 'xdata') and hasattr(event, 'ydata'):
                    if event.xdata is not None and event.ydata is not None:
                        try:
                            # Para dados com índice datetime
                            if hasattr(dados, 'index') and hasattr(dados.index, 'to_pydatetime'):
                                # Converter coordenada x para data
                                x_date = matplotlib.dates.num2date(event.xdata)
                                
                                # Encontrar índice mais próximo
                                diferencias = abs(dados.index - x_date)
                                idx_proximo = diferencias.argmin()
                                
                                valor = dados.iloc[idx_proximo]
                                data = dados.index[idx_proximo]
                                
                                # Criar anotação
                                texto = f"📊 {data.strftime('%d/%m/%Y')}\n{prefixo}{valor:{formato_valor}}{sufixo}"
                                ax.annotate(texto, 
                                          xy=(matplotlib.dates.date2num(data), valor),
                                          xytext=(10, 10), 
                                          textcoords='offset points',
                                          bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.8),
                                          arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'),
                                          fontsize=9)
                                
                            # Para dados simples (listas)
                            else:
                                # Encontrar índice mais próximo baseado na posição x
                                if len(dados) > 0:
                                    idx = int(round(event.xdata))
                                    if 0 <= idx < len(dados):
                                        valor = dados[idx] if hasattr(dados, '__getitem__') else dados.iloc[idx]
                                        texto = f"📊 Índice: {idx}\n{prefixo}{valor:{formato_valor}}{sufixo}"
                                        ax.annotate(texto,
                                                  xy=(idx, valor),
                                                  xytext=(10, 10),
                                                  textcoords='offset points',
                                                  bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.8),
                                                  arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'),
                                                  fontsize=9)
                        except:
                            pass
                        
                        plt.draw()
        
        # Conectar evento de movimento do mouse
        plt.connect('motion_notify_event', on_hover)
    
    def baixar_dados_acao(self, codigo_acao, nome_empresa):
        """Baixa dados de uma ação específica"""
        print(f"\n📥 Baixando dados de {nome_empresa} ({codigo_acao})...")
        
        try:
            ticker = yf.Ticker(codigo_acao)
            # Baixar 6 meses de dados para ter informações suficientes
            dados = ticker.history(period='6mo')
            
            if len(dados) == 0:
                print(f"❌ Nenhum dado encontrado para {codigo_acao}")
                return False
            
            self.acao_atual = codigo_acao
            self.dados_acao = dados
            self.nome_empresa = nome_empresa
            
            print(f"Dados baixados: {len(dados)} registros")
            return True
            
        except Exception as e:
            print(f"Erro ao baixar dados: {e}")
            return False
    
    def calcular_retornos(self):
        """Calcula retornos diários e semanais"""
        if self.dados_acao is None:
            return None, None
            
        retornos_diarios = self.dados_acao['Close'].pct_change().dropna() * 100
        retornos_semanais = self.dados_acao['Close'].resample('W').last().pct_change().dropna() * 100
        
        return retornos_diarios, retornos_semanais
    
    def calcular_volatilidade(self, janela=7):
        """Calcula volatilidade móvel"""
        if self.dados_acao is None:
            return None
            
        retornos_diarios, _ = self.calcular_retornos()
        volatilidade = retornos_diarios.rolling(janela).std()
        
        return volatilidade
    
    def mostrar_resumo_acoes(self):
        """Opção 1: Mostra resumo da ação atual"""
        if self.dados_acao is None:
            print("Nenhuma ação carregada!")
            return
        
        print(f"\nRESUMO - {self.nome_empresa} ({self.acao_atual})")
        print("="*60)
        
        # Dados básicos
        ultimo_preco = self.dados_acao['Close'].iloc[-1]
        primeiro_preco = self.dados_acao['Close'].iloc[0]
        variacao_periodo = ((ultimo_preco - primeiro_preco) / primeiro_preco) * 100
        
        # Retornos
        retornos_diarios, retornos_semanais = self.calcular_retornos()
        
        # Volatilidade
        volatilidade_semanal = self.calcular_volatilidade(7)
        volatilidade_mensal = self.calcular_volatilidade(30)
        
        # Criar tabela resumo
        resumo = {
            'Métrica': [
                'Preço Atual (R$)',
                'Preço Inicial (R$)',
                'Variação no Período (%)',
                'Maior Preço (R$)',
                'Menor Preço (R$)',
                'Volume Médio Diário',
                'Retorno Médio Diário (%)',
                'Retorno Médio Semanal (%)',
                'Volatilidade Semanal (%)',
                'Volatilidade Mensal (%)',
                'Último Volume'
            ],
            'Valor': [
                f"{ultimo_preco:.2f}",
                f"{primeiro_preco:.2f}",
                f"{variacao_periodo:.2f}",
                f"{self.dados_acao['High'].max():.2f}",
                f"{self.dados_acao['Low'].min():.2f}",
                f"{self.dados_acao['Volume'].mean():.0f}",
                f"{retornos_diarios.mean():.2f}",
                f"{retornos_semanais.mean():.2f}",
                f"{volatilidade_semanal.iloc[-1]:.2f}" if not volatilidade_semanal.empty else "N/A",
                f"{volatilidade_mensal.iloc[-1]:.2f}" if not volatilidade_mensal.empty else "N/A",
                f"{self.dados_acao['Volume'].iloc[-1]:.0f}"
            ]
        }
        
        df_resumo = pd.DataFrame(resumo)
        print(df_resumo.to_string(index=False))
        print("="*60)
    
    def grafico_volatilidade_semana(self):
        """Opção 2: Gráfico de volatilidade da última semana"""
        if self.dados_acao is None:
            print("Nenhuma ação carregada!")
            return
        
        volatilidade = self.calcular_volatilidade(7)
        
        # Últimos 7 dias
        volatilidade_semana = volatilidade.tail(7)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        line = ax.plot(volatilidade_semana.index, volatilidade_semana.values, 
                      marker='o', linewidth=2, markersize=8, color='red', alpha=0.8)
        
        # Adicionar interatividade
        self.adicionar_interatividade(ax, volatilidade_semana, formato_valor=":.2f", sufixo="%")
        
        ax.set_title(f'Volatilidade - Última Semana\n{self.nome_empresa} ({self.acao_atual})', 
                    fontsize=14, pad=20)
        ax.set_xlabel('Data')
        ax.set_ylabel('Volatilidade (%)')
        ax.grid(True, alpha=0.3)
        
        # Melhorar formatação das datas
        fig.autofmt_xdate()
        
        # Adicionar valores nos pontos
        for i, (data, valor) in enumerate(volatilidade_semana.items()):
            ax.annotate(f'{valor:.1f}%', 
                       (data, valor),
                       textcoords="offset points",
                       xytext=(0,10),
                       ha='center',
                       fontsize=8,
                       alpha=0.7)
        
        plt.tight_layout()
        plt.show()
        self.aguardar_fechamento_grafico()
    
    def grafico_volatilidade_mes(self):
        """Opção 3: Gráfico de volatilidade do último mês"""
        if self.dados_acao is None:
            print("Nenhuma ação carregada!")
            return
        
        volatilidade = self.calcular_volatilidade(7)
        
        # Últimos 30 dias
        volatilidade_mes = volatilidade.tail(30)
        
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.plot(volatilidade_mes.index, volatilidade_mes.values, 
               linewidth=2, color='orange')
        ax.fill_between(volatilidade_mes.index, volatilidade_mes.values, 
                       alpha=0.3, color='orange')
        
        # Adicionar interatividade
        self.adicionar_interatividade(ax, volatilidade_mes, formato_valor=":.2f", sufixo="%")
        
        ax.set_title(f'Volatilidade - Último Mês\n{self.nome_empresa} ({self.acao_atual})', 
                    fontsize=14, pad=20)
        ax.set_xlabel('Data')
        ax.set_ylabel('Volatilidade (%)')
        ax.grid(True, alpha=0.3)
        
        # Melhorar formatação das datas
        fig.autofmt_xdate()
        
        # Destacar valores máximo e mínimo
        val_max = volatilidade_mes.max()
        val_min = volatilidade_mes.min()
        data_max = volatilidade_mes.idxmax()
        data_min = volatilidade_mes.idxmin()
        
        ax.annotate(f'Máx: {val_max:.2f}%', 
                   xy=(data_max, val_max),
                   xytext=(10, 10),
                   textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.3', fc='red', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', color='red'))
        
        ax.annotate(f'Mín: {val_min:.2f}%', 
                   xy=(data_min, val_min),
                   xytext=(10, -20),
                   textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.3', fc='green', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', color='green'))
        
        plt.tight_layout()
        plt.show()
        self.aguardar_fechamento_grafico()
    
    def grafico_retorno_semanal(self):
        """Opção 4: Gráfico de retorno semanal"""
        if self.dados_acao is None:
            print("Nenhuma ação carregada!")
            return
        
        retornos_diarios, retornos_semanais = self.calcular_retornos()
        
        # Últimas 4 semanas de retornos diários
        retornos_4_semanas = retornos_diarios.tail(28)
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Cores para barras (verde para positivo, vermelho para negativo)
        cores = ['green' if x >= 0 else 'red' for x in retornos_4_semanas]
        
        bars = ax.bar(range(len(retornos_4_semanas)), retornos_4_semanas.values, 
                     color=cores, alpha=0.7, edgecolor='black', linewidth=0.5)
        
        # Adicionar valores nas barras
        for i, (bar, valor) in enumerate(zip(bars, retornos_4_semanas.values)):
            altura = bar.get_height()
            ax.annotate(f'{valor:.1f}%',
                       xy=(bar.get_x() + bar.get_width()/2, altura),
                       xytext=(0, 3 if altura >= 0 else -15),
                       textcoords='offset points',
                       ha='center', va='bottom' if altura >= 0 else 'top',
                       fontsize=7, rotation=90 if abs(altura) > 3 else 0)
        
        # Adicionar interatividade para barras
        def on_hover_bars(event):
            if event.inaxes == ax and event.xdata is not None:
                idx = int(round(event.xdata))
                if 0 <= idx < len(retornos_4_semanas):
                    # Remover anotações anteriores
                    for child in ax.get_children():
                        if hasattr(child, 'get_text') and child.get_text().startswith('📊'):
                            child.remove()
                    
                    valor = retornos_4_semanas.iloc[idx]
                    data = retornos_4_semanas.index[idx]
                    
                    ax.annotate(f'📊 {data.strftime("%d/%m/%Y")}\nRetorno: {valor:.2f}%',
                              xy=(idx, valor),
                              xytext=(10, 10),
                              textcoords='offset points',
                              bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.8),
                              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'),
                              fontsize=9)
                    plt.draw()
        
        plt.connect('motion_notify_event', on_hover_bars)
        
        ax.set_title(f'Retornos Diários - Últimas 4 Semanas\n{self.nome_empresa} ({self.acao_atual})', 
                    fontsize=14, pad=20)
        ax.set_xlabel('Dias')
        ax.set_ylabel('Retorno (%)')
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Configurar eixo x com algumas datas
        step = max(1, len(retornos_4_semanas) // 10)
        indices = list(range(0, len(retornos_4_semanas), step))
        labels = [retornos_4_semanas.index[i].strftime('%d/%m') for i in indices]
        ax.set_xticks(indices)
        ax.set_xticklabels(labels, rotation=45)
        
        plt.tight_layout()
        plt.show()
        self.aguardar_fechamento_grafico()
    
    def grafico_retorno_mensal(self):
        """Opção 5: Gráfico de retorno mensal"""
        if self.dados_acao is None:
            print("Nenhuma ação carregada!")
            return
        
        # Calcular retorno acumulado do período
        precos = self.dados_acao['Close']
        retorno_acumulado = (precos / precos.iloc[0] - 1) * 100
        
        fig, ax = plt.subplots(figsize=(14, 8))
        line = ax.plot(retorno_acumulado.index, retorno_acumulado.values, 
                      linewidth=3, color='blue', marker='o', markersize=3, alpha=0.8)
        ax.fill_between(retorno_acumulado.index, retorno_acumulado.values, 
                       alpha=0.2, color='blue')
        
        # Adicionar interatividade
        self.adicionar_interatividade(ax, retorno_acumulado, formato_valor=":.2f", sufixo="%")
        
        ax.set_title(f'Retorno Acumulado - Período Completo\n{self.nome_empresa} ({self.acao_atual})', 
                    fontsize=14, pad=20)
        ax.set_xlabel('Data')
        ax.set_ylabel('Retorno Acumulado (%)')
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax.grid(True, alpha=0.3)
        
        # Melhorar formatação das datas
        fig.autofmt_xdate()
        
        # Destacar valores importantes
        retorno_final = retorno_acumulado.iloc[-1]
        retorno_max = retorno_acumulado.max()
        retorno_min = retorno_acumulado.min()
        
        data_final = retorno_acumulado.index[-1]
        data_max = retorno_acumulado.idxmax()
        data_min = retorno_acumulado.idxmin()
        
        # Anotações de valores importantes
        ax.annotate(f'Final: {retorno_final:.2f}%', 
                   xy=(data_final, retorno_final),
                   xytext=(-50, 20),
                   textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.3', fc='blue', alpha=0.7, edgecolor='white'),
                   arrowprops=dict(arrowstyle='->', color='blue'),
                   color='white', fontweight='bold')
        
        if retorno_max != retorno_final:
            ax.annotate(f'Máx: {retorno_max:.2f}%', 
                       xy=(data_max, retorno_max),
                       xytext=(10, 10),
                       textcoords='offset points',
                       bbox=dict(boxstyle='round,pad=0.3', fc='green', alpha=0.7),
                       arrowprops=dict(arrowstyle='->', color='green'))
        
        if retorno_min != retorno_final:
            ax.annotate(f'Mín: {retorno_min:.2f}%', 
                       xy=(data_min, retorno_min),
                       xytext=(10, -20),
                       textcoords='offset points',
                       bbox=dict(boxstyle='round,pad=0.3', fc='red', alpha=0.7),
                       arrowprops=dict(arrowstyle='->', color='red'))
        
        plt.tight_layout()
        plt.show()
        self.aguardar_fechamento_grafico()
    
    def menu_acao(self):
        """Menu específico de uma ação"""
        while True:
            self.limpar_tela()
            print("="*60)
            print(f"📈 MENU AÇÃO: {self.nome_empresa} ({self.acao_atual})")
            print("="*60)
            print("1 - Resumo de informações das ações (tabela)")
            print("2 - Gráfico de volatilidade da última semana")
            print("3 - Gráfico de volatilidade do último mês")
            print("4 - Gráfico de retorno semanal")
            print("5 - Gráfico de retorno mensal")
            print("r - Retornar ao menu anterior")
            print("s - Sair/fechar aplicação")
            print("="*60)
            
            opcao = input("Escolha uma opção: ").lower().strip()
            
            if opcao == '1':
                self.mostrar_resumo_acoes()
                input("\n📊 Pressione Enter para continuar...")
                
            elif opcao == '2':
                self.grafico_volatilidade_semana()
                
            elif opcao == '3':
                self.grafico_volatilidade_mes()
                
            elif opcao == '4':
                self.grafico_retorno_semanal()
                
            elif opcao == '5':
                self.grafico_retorno_mensal()
                
            elif opcao == 'r':
                return
                
            elif opcao == 's':
                print("Encerrando aplicação...")
                sys.exit()
                
            else:
                print("Opção inválida!")
                input("Pressione Enter para continuar...")
    
    def menu_empresas(self, tipo='brasileiras'):
        """Menu das 10 maiores empresas (brasileiras ou estrangeiras)"""
        empresas = self.empresas_brasileiras if tipo == 'brasileiras' else self.empresas_estrangeiras
        titulo = "BRASILEIRAS" if tipo == 'brasileiras' else "ESTRANGEIRAS"
        
        while True:
            self.limpar_tela()
            print("="*60)
            print(f"🏢 10 MAIORES EMPRESAS {titulo} LISTADAS NA B3")
            print("="*60)
            
            for num, (nome, codigo) in empresas.items():
                print(f"{num:2d} - {nome} ({codigo})")
            
            print("r  - Retornar ao menu principal")
            print("s  - Sair/fechar aplicação")
            print("="*60)
            
            opcao = input("👉 Escolha uma opção: ").lower().strip()
            
            if opcao in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
                num_opcao = int(opcao)
                nome_empresa, codigo_acao = empresas[num_opcao]
                
                if self.baixar_dados_acao(codigo_acao, nome_empresa):
                    self.menu_acao()
                else:
                    input("Erro ao carregar dados. Pressione Enter para continuar...")
                    
            elif opcao == 'r':
                return
                
            elif opcao == 's':
                print("Encerrando aplicação...")
                sys.exit()
                
            else:
                print("Opção inválida!")
                input("Pressione Enter para continuar...")
    
    def menu_principal(self):
        """Menu principal da aplicação"""
        while True:
            self.limpar_tela()
            print("="*60)
            print("SISTEMA DE ANÁLISE FINANCEIRA B3")
            print("="*60)
            print("1 - Listar as 10 maiores empresas brasileiras listadas na B3")
            print("2 - Listar as 10 maiores empresas estrangeiras listadas na B3")  
            print("s - Sair/fechar aplicação")
            print("="*60)
            
            opcao = input("Escolha uma opção: ").lower().strip()
            
            if opcao == '1':
                self.menu_empresas('brasileiras')
                
            elif opcao == '2':
                self.menu_empresas('estrangeiras')
                
            elif opcao == 's':
                print("👋 Encerrando aplicação...")
                sys.exit()
                
            else:
                print("Opção inválida!")
                input("Pressione Enter para continuar...")
    
    def executar(self):
        """Executa o sistema"""
        try:
            print("Iniciando Sistema de Análise Financeira B3...")
            print("Configurando interface gráfica...")
            
            # Teste rápido do matplotlib
            plt.figure(figsize=(1,1))
            plt.close()
            
            print("Interface gráfica configurada com sucesso!")
            input("Pressione Enter para continuar...")
            
            self.menu_principal()
            
        except KeyboardInterrupt:
            print("\nAplicação interrompida pelo usuário.")
            sys.exit()
        except Exception as e:
            print(f"Erro inesperado: {e}")
            input("Pressione Enter para sair...")
            sys.exit()

# Executar aplicação
if __name__ == "__main__":
    analisador = AnalisadorB3()
    analisador.executar()