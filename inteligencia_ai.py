import sqlite3
import pandas as pd

print("--- INICIANDO ANALISE DE BI + MODELO DE INSIGHTS LOCAL ---")

# 1. EXTRAINDO OS DADOS DO BANCO DE DADOS SQL
conexao = sqlite3.connect("empresa.db")
comando_sql = "SELECT * FROM vendas_consolidadas"
df_vendas = pd.read_sql_query(comando_sql, conexao)
conexao.close()

# Cálculos Estruturados da IA Local
faturamento_total = df_vendas['Faturamento_Total'].sum()

faturamento_por_produto = df_vendas.groupby('Produto')['Faturamento_Total'].sum()
produto_lider = faturamento_por_produto.idxmax()
valor_produto_lider = faturamento_por_produto.max()

faturamento_por_regiao = df_vendas.groupby('Regiao')['Faturamento_Total'].sum()
ranking_regioes = faturamento_por_regiao.sort_values(ascending=False)

regiao_lider = ranking_regioes.index[0]
valor_regiao_lider = ranking_regioes.iloc[0]

# Tratamento para identificar o segundo lugar
if len(ranking_regioes) > 1:
    regiao_segundo = ranking_regioes.index[1]
    valor_regiao_segundo = ranking_regioes.iloc[1]
else:
    regiao_segundo = "Apenas uma regiao ativa"
    valor_regiao_segundo = 0.0

# 2. ENGENHARIA DE PROMPT LOCAL (Geração Dinâmica de Texto)
print("Processando dados e gerando insights de negócios...")

insights_texto = f"""=== RELATÓRIO EXECUTIVO GERENCIAL (IA LOCAL) ===
Gerado automaticamente via Python & Estruturas de Dados

1. PERFORMANCE FINANCEIRA GLOBAL
O faturamento bruto consolidado no período analisado atingiu a marca de R$ {faturamento_total:,.2f}. 
O principal motor de receita da companhia foi o produto '{produto_lider}', gerando sozinho um montante de R$ {valor_produto_lider:,.2f}.

2. ANÁLISE GEOGRÁFICA DE VENDAS
A operação comercial registrou sua maior eficiência na região '{regiao_lider}', liderando o faturamento corporativo com R$ {valor_regiao_lider:,.2f}. 
Identificamos a região '{regiao_segundo}' ocupando a segunda posição do ranking de receita com R$ {valor_regiao_segundo:,.2f}.

3. DIRETRIZES ESTRATÉGICAS SUGERIDAS
Ação recomendada para expansão: Para acelerar o crescimento na região '{regiao_segundo}', a diretoria deve replicar os pacotes de ofertas promocionais do produto '{produto_lider}' que consolidaram o sucesso da líder '{regiao_lider}', customizando o investimento em canais de mídia locais.
"""

# 3. SALVANDO O RESULTADO EM UM ARQUIVO DE TEXTO
with open("insights_ia_banco.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write(insights_texto)

print("\n=== RELATÓRIO EXECUTIVO GERENCIAL DE NEGÓCIOS ===")
print(insights_texto)
print("==================================================")
print("\n🚀 Sucesso absoluto! O relatório inteligente foi gerado e salvo em 'insights_ia_banco.txt'")
