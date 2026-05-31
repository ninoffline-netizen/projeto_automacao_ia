import os
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import matplotlib.pyplot as plt
import customtkinter as ctk

# 1. FUNÇÃO DA AUTOMAÇÃO COMERCIAL (O pacote de comandos do robô)
def executar_automacao():
    print("--- INICIANDO PROCESSO ATRAVÉS DA INTERFACE ---")
    
    # CAPTURA DE DADOS DA TELA: Pegamos o texto digitado nas caixas visuais!
    email_destino_usuario = campo_email.get()
    senha_app_usuario = campo_senha.get()
    
    # Se o usuário esquecer de preencher, avisamos no terminal e paramos
    if not email_destino_usuario or not senha_app_usuario:
        print("\n❌ Erro: Por favor, preencha o e-mail e a senha na janela visual!")
        return
        
    pasta_origem = "dados_filiais"
    lista_de_tabelas = []

    # Varrendo a pasta automaticamente
    for nome_arquivo in os.listdir(pasta_origem):
        if nome_arquivo.endswith('.xlsx'):
            caminho_completo = os.path.join(pasta_origem, nome_arquivo)
            tabela_atual = pd.read_excel(caminho_completo)
            tabela_atual['Faturamento_Total'] = tabela_atual['Quantidade'] * tabela_atual['Preco_Unitario']
            lista_de_tabelas.append(tabela_atual)

    df = pd.concat(lista_de_tabelas, ignore_index=True)

    # Cálculos Gerais
    faturamento_geral = df['Faturamento_Total'].sum()
    faturamento_por_produto = df.groupby('Produto')['Faturamento_Total'].sum()
    produto_campeao = faturamento_por_produto.idxmax()
    valor_produto_campeao = faturamento_por_produto.max()

    faturamento_por_regiao = df.groupby('Regiao')['Faturamento_Total'].sum()
    faturamento_por_regiao_ordenado = faturamento_por_regiao.sort_values(ascending=False)
    regiao_campea = faturamento_por_regiao_ordenado.index[0]
    valor_regiao_campea = faturamento_por_regiao_ordenado.iloc[0]

    if len(faturamento_por_regiao_ordenado) > 1:
        regiao_destaque = faturamento_por_regiao_ordenado.index[1]
        valor_regiao_destaque = faturamento_por_regiao_ordenado.iloc[1]
    else:
        regiao_destaque = "N/A"
        valor_regiao_destaque = 0.0

    # Gerando Gráficos
    plt.figure(figsize=(6, 3))
    faturamento_por_produto.plot(kind='bar', color='#2ca02c')
    plt.title('Faturamento Total por Produto', fontsize=11, fontweight='bold')
    plt.tight_layout()
    nome_grafico_produto = "grafico_produtos.png"
    plt.savefig(nome_grafico_produto)
    plt.close()

    plt.figure(figsize=(6, 3))
    faturamento_por_regiao.plot(kind='bar', color='#1f77b4')
    plt.title('Faturamento Total por Região', fontsize=11, fontweight='bold')
    plt.tight_layout()
    nome_grafico_regiao = "grafico_regioes.png"
    plt.savefig(nome_grafico_regiao)
    plt.close()

    # Criando o PDF
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

    # Configuração de e-mail usando os dados capturados da tela
    MEU_EMAIL = "ninoffline@gmail.com"
    
    msg = MIMEMultipart()
    msg['From'] = MEU_EMAIL
    msg['To'] = email_destino_usuario
    msg['Subject'] = f"Relatorio Comercial Automatizado - R$ {faturamento_geral:,.2f}"
    
    corpo_email = "Olá, segue em anexo o relatório executivo gerado através da interface gráfica do nosso sistema."
    msg.attach(MIMEText(corpo_email, 'plain'))

    with open(nome_pdf, "rb") as anexo:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(anexo.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={nome_pdf}")
        msg.attach(part)

    try:
        # Usando o IP direto estável da Google
        server = smtplib.SMTP("74.125.193.108", 587)
        server.starttls()
        server.login(MEU_EMAIL, senha_app_usuario)
        server.sendmail(MEU_EMAIL, email_destino_usuario, msg.as_string())
        server.quit()
        print("\n🚀 Sucesso absoluto! O e-mail foi disparado via interface gráfica!")
    except Exception as e:
        print(f"\n❌ Erro ao enviar: {e}")


# 2. CONSTRUÇÃO DA INTERFACE GRÁFICA (Igual à aula anterior, mas com o botão conectado)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Sistema Automatizado de BI - Executivo")
janela.geometry("500x400")

titulo = ctk.CTkLabel(janela, text="Painel de Automação Comercial", font=("Helvetica", 20, "bold"))
titulo.pack(pady=20)

label_email = ctk.CTkLabel(janela, text="E-mail de Destino:", font=("Helvetica", 12))
label_email.pack(pady=5)
campo_email = ctk.CTkEntry(janela, placeholder_text="Ex: diretor@empresa.com", width=350)
campo_email.pack(pady=5)

label_senha = ctk.CTkLabel(janela, text="Senha de App do Gmail (16 letras):", font=("Helvetica", 12))
label_senha.pack(pady=5)
campo_senha = ctk.CTkEntry(janela, placeholder_text="Digite sua senha de app aqui", width=350, show="*")
campo_senha.pack(pady=5)

# MUDANÇA CONECTORA: Adicionamos o comando 'command=executar_automacao' para ligar o botão à nossa função!
botao_executar = ctk.CTkButton(janela, text="Gerar Relatório & Enviar E-mail", font=("Helvetica", 14, "bold"), width=200, height=40, command=executar_automacao)
botao_executar.pack(pady=30)

janela.mainloop()
