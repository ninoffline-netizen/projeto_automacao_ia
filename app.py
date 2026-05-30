import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import matplotlib.pyplot as plt

print("--- INICIANDO AUTOMAÇÃO COM RELATÓRIO VISUAL ---")

# 1. CÁLCULOS COM PANDAS
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import matplotlib.pyplot as plt

print("--- INICIANDO AUTOMAÇÃO COM MÚLTIPLAS PLANILHAS ---")

# 1. NOVA LÓGICA: CONSOLIDANDO VÁRIOS ARQUIVOS
    # Criamos uma lista com os dois arquivos novos que geramos
arquivos_vendas = ["vendas_rj.xlsx", "vendas_sp.xlsx"]
lista_de_tabelas = []

print("Consolidando dados das filiais...")
for arquivo in arquivos_vendas:
    # Lendo o arquivo atual da rodada
    tabela_atual = pd.read_excel(arquivo)
    
    # Criando a coluna de Faturamento Total para este arquivo específico
    tabela_atual['Faturamento_Total'] = tabela_atual['Quantidade'] * tabela_atual['Preco_Unitario']
    
    # Guardando esta tabela pronta na nossa lista acumuladora
    lista_de_tabelas.append(tabela_atual)

# O comando mágico 'concat' junta todas as tabelas da lista em um único DataFrame mestre
df = pd.concat(lista_de_tabelas, ignore_index=True)

# A partir daqui, a matemática abaixo vai ler os dados já unificados!
faturamento_geral = df['Faturamento_Total'].sum()

faturamento_por_produto = df.groupby('Produto')['Faturamento_Total'].sum()
produto_campeao = faturamento_por_produto.idxmax()
valor_produto_campeao = faturamento_por_produto.max()

faturamento_por_regiao = df.groupby('Regiao')['Faturamento_Total'].sum()
regiao_campea = faturamento_por_regiao.idxmax()
valor_regiao_campea = faturamento_por_regiao.max()


# 2. CRIANDO O GRÁFICO VISUAL (Matplotlib)
print("Gerando gráfico de desempenho por produto...")
plt.figure(figsize=(6, 4)) # Define o tamanho da imagem

# Cria o gráfico de barras com um design moderno (cor verde)
faturamento_por_produto.plot(kind='bar', color='#2ca02c')

plt.title('Faturamento Total por Produto', fontsize=14, fontweight='bold')
plt.xlabel('Produtos', fontsize=12)
plt.ylabel('Faturamento (R$)', fontsize=12)
plt.xticks(rotation=45) # Inclina os nomes para não embolar
plt.tight_layout() # Ajusta as margens automaticamente

# Salva o gráfico como imagem na pasta do projeto
nome_grafico = "grafico_vendas.png"
plt.savefig(nome_grafico)
plt.close() # Fecha a janela interna do gráfico para liberar memória

# 3. GERANDO O RELATÓRIO EM PDF COM A IMAGEM
print("Estruturando o documento PDF...")
pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=14)

# Cabeçalho
pdf.cell(200, 10, text="=== RELATORIO GERENCIAL EXECUTIVO ===", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
pdf.cell(200, 10, text="Gerado automaticamente via Python", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
pdf.ln(10)

# Dados textuais
pdf.cell(200, 10, text=f"1. Faturamento Geral da Empresa: R$ {faturamento_geral:,.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(200, 10, text=f"2. Produto Campeao de Vendas: {produto_campeao} (R$ {valor_produto_campeao:,.2f})", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(200, 10, text=f"3. Regiao com Maior Desempenho: {regiao_campea} (R$ {valor_regiao_campea:,.2f})", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(10)

# Inserindo o gráfico gerado dentro do PDF (X, Y, Largura)
pdf.image(nome_grafico, x=25, y=80, w=160)

nome_pdf = "relatorio_final.pdf"
pdf.output(nome_pdf)

# 4. CONFIGURAÇÃO DO ENVIO DE E-MAIL (Usando IP direto)
MEU_EMAIL = "ninoffline@gmail.com"
MINHA_SENHA_APP = "gpzkwovkwinyevrd"
EMAIL_DESTINO = "ninoffline@gmail.com"

print("Conectando ao Gmail e enviando o PDF com gráfico...")

msg = MIMEMultipart()
msg['From'] = MEU_EMAIL
msg['To'] = EMAIL_DESTINO
msg['Subject'] = f"Relatório Visual de Vendas - R$ {faturamento_geral:,.2f}"

corpo_email = "Olá, segue em anexo o novo relatório executivo contendo a análise visual de desempenho."
msg.attach(MIMEText(corpo_email, 'plain'))

with open(nome_pdf, "rb") as anexo:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(anexo.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={nome_pdf}")
    msg.attach(part)

try:
    server = smtplib.SMTP("74.125.193.108", 587) # Seu IP direto que funcionou!
    server.starttls()
    server.login(MEU_EMAIL, MINHA_SENHA_APP)
    server.sendmail(MEU_EMAIL, EMAIL_DESTINO, msg.as_string())
    server.quit()
    print("\n🚀 Sucesso absoluto! O e-mail com o gráfico e o PDF foi entregue!")
except Exception as e:
    print(f"\n❌ Erro ao enviar: {e}")
