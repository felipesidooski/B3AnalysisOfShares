# Sistema de Análise Financeira B3

Sistema interativo em Python para análise das maiores empresas brasileiras e estrangeiras listadas na B3.

## Características

- **Menu interativo** com navegação completa
- **Gráficos interativos** com valores ao passar o mouse 🖱️
- **Gráficos com análise dinâmica** que aguardam fechamento
- **Dados em tempo real** da B3 via yfinance
- **20 empresas** pré-selecionadas (10 brasileiras + 10 estrangeiras)
- **5 tipos de análise** por ação com visualizações avançadas

## Instalação Rápida

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar aplicação
python StartApp.py
```

## Pré-requisitos

- **Python 3.8+** (recomendado 3.9+)
- **Conexão com internet** (para dados financeiros)
- **Interface gráfica** (para exibir gráficos)

### Instalação Detalhada

Para instruções específicas do seu sistema operacional, veja: **[INSTALACAO.md](INSTALACAO.md)**

## Como usar

```bash
python StartApp.py
```

## 📊 Estrutura de Menus

```
MENU PRINCIPAL
├── 1 - Empresas Brasileiras
├── 2 - Empresas Estrangeiras
└── s - Sair

MENU EMPRESAS
├── 1-10 - Selecionar Empresa
├── r - Retornar
└── s - Sair

MENU AÇÃO
├── 1 - Resumo (tabela)
├── 2 - Volatilidade Semanal (gráfico interativo)
├── 3 - Volatilidade Mensal (gráfico interativo)  
├── 4 - Retorno Semanal (gráfico interativo)
├── 5 - Retorno Mensal (gráfico interativo)
├── r - Retornar
└── s - Sair
```

## Empresas Disponíveis

### Brasileiras
1. Petrobras (PETR4)
2. Vale (VALE3)
3. Itaú Unibanco (ITUB4)
4. Banco do Brasil (BBAS3)
5. Bradesco (BBDC4)
6. Ambev (ABEV3)
7. Magazine Luiza (MGLU3)
8. WEG (WEGE3)
9. JBS (JBSS3)
10. Suzano (SUZB3)

### Estrangeiras (BDRs)
1. Apple (AAPL34)
2. Microsoft (MSFT34)
3. Amazon (AMZO34)
4. Google (GOGL34)
5. Tesla (TSLA34)
6. Meta (FBOK34)
7. Netflix (NFLX34)
8. Nvidia (NVDC34)
9. Coca-Cola (COCA34)
10. Disney (DISB34)

## Comportamento dos Gráficos Interativos

### Gráficos Interativos**
- **Passe o mouse** sobre pontos/barras para ver valores precisos
- **Data e valor** aparecem em tooltip amarelo
- **Valores destacados** automaticamente (máximo, mínimo, final)
- **Anotações visuais** em pontos importantes
- **Interação em tempo real** - sem cliques necessários

### Características dos Gráficos
- Gráficos abrem em **janela separada**
- Sistema **aguarda fechamento** da janela
- **Feche o gráfico** para voltar ao menu
- **Interatividade total** com mouse hover
- **Valores precisos** com data/hora

## Tipos de Análise Interativa

### 1. **Resumo da Ação**
- Tabela completa com métricas principais
- Preços, volumes, retornos e volatilidade
- Valores atualizados em tempo real

### 2. **Volatilidade Semanal**
- **Interativo**: Passe o mouse para ver volatilidade por dia
- Últimos 7 dias com valores precisos
- Tooltips com data e percentual
- Marcadores em cada ponto

### 3. **Volatilidade Mensal**
- **Interativo**: Hover para ver volatilidade diária
- Últimos 30 dias com área preenchida
- Destacas automáticos de máximo e mínimo
- Tooltips com data e valor

### 4. **Retorno Semanal**
- **Interativo**: Hover sobre barras para detalhes
- Barras coloridas (verde=ganho, vermelho=perda)
- Valores sobre cada barra
- Tooltips com data e retorno exato

### 5. **Retorno Mensal**
- **Interativo**: Hover para retorno acumulado por dia
- Curva de performance completa
- Marcação de valores finais, máximos e mínimos
- Área preenchida para melhor visualização

## Como Usar a Interatividade

### **Mouse Hover** (Passar o mouse)
1. **Abra qualquer gráfico** (opções 2-5)
2. **Mova o mouse** sobre pontos/barras
3. **Veja tooltips** com valores exatos
4. **Data e valor** aparecem automaticamente
5. **Não precisa clicar** - só mover o mouse

### **Informações Mostradas**
- **Data**: Dia/mês/ano do ponto
- **Valor**: Número preciso (%, R$, etc.)
- **Posição**: Índice/coordenada
- **Destaque**: Máximos, mínimos, valores finais

## Dicas de Uso

- **Conexão com internet** obrigatória
- **Dados baixados** apenas quando necessário
- **Mouse hover** para valores precisos nos gráficos
- **Feche gráficos** para continuar navegação
- Use **'r'** para retornar, **'s'** para sair
- **Gráficos podem demorar** alguns segundos para carregar

## Arquivos do Projeto

### Principais
- `financial_analysis.py` - Sistema principal com gráficos interativos
- `exemplo_uso.py` - Executável simplificado
- `requirements.txt` - Dependências

### Documentação
- `README.md` - Este arquivo

### Gráficos (Caso não aparecam)
- **Linux**: `sudo apt install python3-tk`
- **Windows**: Reinstale Python com "tcl/tk and IDLE"
- **Mac**: `brew install python-tk`

### Interatividade não funciona
```bash
# Verificando backend matplotlib
python -c "import matplotlib; print(matplotlib.get_backend())"

# Se mostrar 'Agg', reinstale matplotlib
pip install matplotlib --upgrade
```

### Erros de importação
```bash
pip install -r requirements.txt --upgrade
```

### Dados não carregam - Teste da biblioteca Yfinance.
- Verifique conexão com internet
- Teste: `python -c "import yfinance; print(yfinance.Ticker('PETR4.SA').history(period='1d'))"`


## Exemplo de Uso:

```bash
# 1. Iniciar sistema
python StartApp.py

# 2. Navegar pelos menus
Digite "1" → Empresas Brasileiras
Digite "1" → Petrobras

# 3. Ver gráfico interativo
Digite "2" → Volatilidade Semanal
[Gráfico aparece na tela]

# 4. Usar interatividade
🖱️ Passe o mouse sobre os pontos
📊 Veja tooltips com valores exatos
📅 Data e percentual aparecem automaticamente

# 5. Continuar
Feche a janela do gráfico
Digite "r" → Retornar
Digite "s" → Sair
```

## 📦 Dependências

| Biblioteca | Versão Mínima | Função |
|-----------|---------------|---------|
| pandas    | 2.0.0         | Manipulação de dados |
| numpy     | 1.24.0        | Cálculos numéricos |
| matplotlib| 3.7.0         | Gráficos interativos |
| yfinance  | 0.2.18        | Dados financeiros |
| seaborn   | 0.12.0        | Visualizações |

## 🎯 Estrutura do Código Interativo

```python
AnalisadorB3()
├── empresas_brasileiras{}           # 10 maiores empresas BR
├── empresas_estrangeiras{}          # 10 maiores BDRs
├── baixar_dados_acao()              # Download sob demanda
├── calcular_retornos()              # Métricas financeiras
├── mostrar_resumo_acoes()           # Tabela de dados
├── adicionar_interatividade()       # 🆕 Tooltips interativos
├── grafico_volatilidade_*()         # 🆕 Gráficos com hover
├── grafico_retorno_*()              # 🆕 Gráficos com valores
├── aguardar_fechamento_grafico()    # 🆕 Aguarda fechamento
└── menu_*()                         # Sistema de navegação
```

**Desenvolvido com Python + Matplotlib Interativo + yfinance + Pandas**

🚀 **Para começar**: `python StartApp.py`  
📋 **Para instalação**: pip install -r requirements.txt`  
🧪 **Para testar**: `python -c "import yfinance; print(yfinance.Ticker('PETR4.SA').history(period='1d'))"`  
🖱️ **Para interagir**: passe o mouse sobre os gráficos!
