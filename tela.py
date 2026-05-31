import os
import pandas as pd
import smtplib
import sqlite3  # <-- Importado para permitir a leitura do banco na tela!
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import matplotlib.pyplot as plt
import customtkinter as ctk

# === 1. FUNÇÃO DE INSIGHTS COM BANCO DE DADOS (NOVA INTEGRAÇÃO) ===
def exibir_insights_tela():
    print("\n--- PROCESSANDO INSIGHTS DO BANCO DE DADOS ---")
    
    # Se o banco de dados não existir ainda, avisa na tela e para
    if not os.path.exists("empresa.db"):
        painel_insights.delete("1.0", ctk.END)
        painel_insights.insert("1.0", "❌ Erro: O arquivo 'empresa.db' não foi encontrado. Execute a automação primeiro!")
        return

    # Conectando ao Banco de Dados SQL
    conexao = sqlite3.connect("empresa.db")
    comando_sql = "SELECT * FROM vendas_consolidadas"
    df_vendas = pd.read_sql_query(comando_sql, conexao)
    conexao.close()

    # Cálculos de Negócios
    faturamento_total = df_vendas['Faturamento_Total'].sum()
    faturamento_por_produto = df_vendas.groupby('Produto')['Faturamento_Total'].sum()
    produto_lider = faturamento_por_produto.idxmax()
    valor_produto_lider = faturamento_por_produto.max()

    faturamento_por_regiao = df_vendas.groupby('Regiao')['Faturamento_Total'].sum()
    ranking_regioes = faturamento_por_regiao.sort_values(ascending=False)
    regiao_lider = ranking_regioes.index[0]
    valor_regiao_lider = ranking_regioes.iloc[0]

    if len(ranking_regioes) > 1:
        regiao_segundo = ranking_regioes.index[1]
        valor_regiao_segundo = ranking_regioes.iloc[1]
    else:
        regiao_segundo = "Apenas uma região ativa"
        valor_regiao_segundo = 0.0

    # Montando o Texto Dinâmico
    texto_relatorio = f"""=== RELATÓRIO EXECUTIVO GERENCIAL DE INSIGHTS ===

1. PERFORMANCE FINANCEIRA GLOBAL
O faturamento bruto consolidado atingiu a marca de R$ {faturamento_total:,.2f}.
O principal motor de receita foi o produto '{produto_lider}', gerando sozinho R$ {valor_produto_lider:,.2f}.

2. ANÁLISE GEOGRÁFICA DE VENDAS
A operação comercial registrou maior eficiência na região '{regiao_lider}' com R$ {valor_regiao_lider:,.2f}.
A região '{regiao_segundo}' ocupa a segunda posição com R$ {valor_regiao_segundo:,.2f}.

3. DIRETRIZES ESTRATÉGICAS SUGERIDAS
Ação recomendada: Para acelerar o crescimento na região '{regiao_segundo}', a diretoria deve replicar os pacotes de ofertas promocionais do produto '{produto_lider}' que consolidaram o sucesso da líder '{regiao_lider}', customizando o investimento em canais de mídia locais.
"""
    
    # Atualiza o painel visual com o novo texto gerado
    painel_insights.delete("1.0", ctk.END) # Limpa o painel anterior
    painel_insights.insert("1.0", texto_relatorio) # Insere o relatório novo
    print("🚀 Insights impressos na tela com sucesso!")


# === 2. FUNÇÃO DA AUTOMAÇÃO COMERCIAL (IGUAL À ANTERIOR) ===
def executar_automacao():
    print("\n--- INICIANDO PROCESSO ATRAVÉS DA INTERFACE ---")
    email_destino_usuario = campo_email.get()
    senha_app_usuario = campo_senha.get()
    
    if not email_destino_usuario or not senha_app_usuario:
        painel_insights.delete("1.0", ctk.END)
        painel_insights.insert("1.0", "❌ Erro: Preencha o e-mail e a senha antes de gerar o relatório!")
        return
        
    pasta_origem = "dados_filiais"
    lista_de_tabelas = []

    # Se a pasta de dados não existir, tenta ler da pasta 'arquivados'
    pasta_leitura = pasta_origem if os.path.exists(pasta_origem) and os.listdir(pasta_origem) else "arquivados"

    for nome_arquivo in os.listdir(pasta_leitura):
        if nome_arquivo.endswith('.xlsx'):
            caminho_completo = os.path.join(pasta_leitura, nome_arquivo)
            tabela_atual = pd.read_excel(caminho_completo)
            tabela_atual['Faturamento_Total'] = tabela_atual['Quantidade'] * tabela_atual['Preco_Unitario']
            lista_de_tabelas.append(tabela_atual)

    df = pd.concat(lista_de_tabelas, ignore_index=True)

    # Salvando no banco de dados SQLite automaticamente ao rodar a automação
    conexao = sqlite3.connect("empresa.db")
    df.to_sql(name="vendas_consolidadas", con=conexao, if_exists="replace", index=False)
    conexao.close()

    faturamento_geral = df['Faturamento_Total'].sum()
    faturamento_por_produto = df.groupby('Produto')['Faturamento_Total'].sum()
    produto_campeao = faturamento_por_produto.idxmax()
    faturamento_por_regiao = df.groupby('Regiao')['Faturamento_Total'].sum()
    faturamento_por_regiao_ordenado = faturamento_por_regiao.sort_values(ascending=False)
    regiao_campea = faturamento_por_regiao_ordenado.index[0]
    
    if len(faturamento_por_regiao_ordenado) > 1:
        regiao_destaque = faturamento_por_regiao_ordenado.index[1]
    else:
        regiao_destaque = "N/A"

    plt.figure(figsize=(6, 2.5))
    faturamento_por_produto.plot(kind='bar', color='#2ca02c')
    plt.title('Faturamento Total por Produto', fontsize=11, fontweight='bold')
    plt.tight_layout()
    nome_grafico_produto = "grafico_produtos.png"
    plt.savefig(nome_grafico_produto)
    plt.close()

    plt.figure(figsize=(6, 2.5))
    faturamento_por_regiao.plot(kind='bar', color='#1f77b4')
    plt.title('Faturamento Total por Região', fontsize=11, fontweight='bold')
    plt.tight_layout()
    nome_grafico_regiao = "grafico_regioes.png"
    plt.savefig(nome_grafico_regiao)
    plt.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=14)
    pdf.cell(200, 10, text="=== RELATORIO GERENCIAL EXECUTIVO ===", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(5)
    pdf.cell(200, 10, text=f"1. Faturamento Geral da Empresa: R$ {faturamento_geral:,.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(200, 10, text=f"2. Produto Campeao de Vendas: {produto_campeao}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(200, 10, text=f"3. Regiao Lider: {regiao_campea}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(200, 10, text=f"4. Regiao Destaque (2o Lugar): {regiao_destaque}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.image(nome_grafico_produto, x=25, y=85, w=160)
    pdf.image(nome_grafico_regiao, x=25, y=165, w=160)
    nome_pdf = "relatorio_final.pdf"
    pdf.output(nome_pdf)

    msg = MIMEMultipart()
    msg['From'] = "ninoffline@gmail.com"
    msg['To'] = email_destino_usuario
    msg['Subject'] = f"Relatorio Comercial Automatizado - R$ {faturamento_geral:,.2f}"
    corpo_email = "Olá, segue em anexo o relatório executivo gerado através da interface gráfica."
    msg.attach(MIMEText(corpo_email, 'plain'))

    with open(nome_pdf, "rb") as anexo:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(anexo.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={nome_pdf}")
        msg.attach(part)

    try:
        server = smtplib.SMTP("74.125.193.108", 587)
        server.starttls()
        server.login("ninoffline@gmail.com", senha_app_usuario)
        server.sendmail("ninoffline@gmail.com", email_destino_usuario, msg.as_string())
        server.quit()
        painel_insights.delete("1.0", ctk.END)
        painel_insights.insert("1.0", "🚀 Sucesso absoluto! Relatório enviado por e-mail e salvo no banco de dados!")
    except Exception as e:
        painel_insights.delete("1.0", ctk.END)
        painel_insights.insert("1.0", f"❌ Erro ao enviar: {e}")


# === 3. CONSTRUÇÃO DA INTERFACE GRÁFICA ATUALIZADA ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Plataforma Integrada de Business Intelligence")
janela.geometry("600x650") # Aumentamos um pouco o tamanho para acomodar o painel de texto

titulo = ctk.CTkLabel(janela, text="Painel Executivo de BI & Automação", font=("Helvetica", 22, "bold"))
titulo.pack(pady=15)

# Campos de Entrada
label_email = ctk.CTkLabel(janela, text="E-mail de Destino:", font=("Helvetica", 12))
label_email.pack(pady=2)
campo_email = ctk.CTkEntry(janela, placeholder_text="Ex: diretor@empresa.com", width=400)
campo_email.pack(pady=5)

label_senha = ctk.CTkLabel(janela, text="Senha de App do Gmail (16 letras):", font=("Helvetica", 12))
label_senha.pack(pady=2)
campo_senha = ctk.CTkEntry(janela, placeholder_text="Digite sua senha de app aqui", width=400, show="*")
campo_senha.pack(pady=5)

# Botão 1: Executar o processo padrão de e-mail e PDF
botao_executar = ctk.CTkButton(janela, text="🚀 Gerar Relatório & Enviar E-mail", font=("Helvetica", 13, "bold"), width=250, height=35, command=executar_automacao)
botao_executar.pack(pady=10)

# Botão 2: NOVO BOTÃO para buscar e exibir os insights na tela na hora
botao_insights = ctk.CTkButton(janela, text="📊 Ler Banco de Dados & Exibir Insights", font=("Helvetica", 13, "bold"), width=250, height=35, fg_color="#2ca02c", hover_color="#217a21", command=exibir_insights_tela)
botao_insights.pack(pady=5)

# Painel de Texto: Onde os relatórios e erros serão exibidos de forma elegante
label_painel = ctk.CTkLabel(janela, text="Terminal de Relatórios Visuais:", font=("Helvetica", 12, "bold"))
label_painel.pack(pady=(15, 2))

painel_insights = ctk.CTkTextbox(janela, width=450, height=200, font=("Helvetica", 11))
painel_insights.pack(pady=5)
painel_insights.insert("1.0", "Aguardando comandos... Clique em um dos botões acima.")

janela.mainloop()
