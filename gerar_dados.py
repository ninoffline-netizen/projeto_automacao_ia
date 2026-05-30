import pandas as pd

# Dados da Filial 1
dados_rj = {'Produto': ['Notebook', 'Smartphone'], 'Quantidade': [2, 5], 'Preco_Unitario': [4000, 1500], 'Regiao': ['Sudeste', 'Sudeste']}
pd.DataFrame(dados_rj).to_excel('vendas_rj.xlsx', index=False)

# Dados da Filial 2
dados_sp = {'Produto': ['Teclado Mecânico', 'Monitor 4K'], 'Quantidade': [10, 3], 'Preco_Unitario': [350, 2800], 'Regiao': ['Sudeste', 'Sudeste']}
pd.DataFrame(dados_sp).to_excel('vendas_sp.xlsx', index=False)

print("Planilhas 'vendas_rj.xlsx' e 'vendas_sp.xlsx' criadas para o teste!")

