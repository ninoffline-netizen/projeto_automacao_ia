import requests
from bs4 import BeautifulSoup
import pandas as pd

print("--- INICIANDO ROBO DE CAPTURA BLINDADO (WEB SCRAPING) ---")

url = "https://httpbin.org"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Acessando o laboratorio de dados...")
resposta = requests.get(url, headers=headers)

if resposta.status_code == 200:
    # Lemos o HTML do site
    site_html = BeautifulSoup(resposta.text, "lxml")
    
    print("Extraindo o conteudo textual de forma direta...")
    # Captura todo o texto visível da página, eliminando códigos e tags em branco
    texto_puro_site = site_html.get_text(separator=" ", strip=True)
    
    # Pegamos apenas os primeiros 150 caracteres para o relatório não ficar gigante
    resumo_texto = texto_puro_site[:150] + "..."
    
    print("\n[DADOS CAPTURADOS COM SUCESSO!]")
    print(f"Conteudo Extraido: {resumo_texto}")
    
    # SALVANDO OS DADOS DIRETO NO EXCEL COM PANDAS
    dados_coletados = {
        'Plataforma_Origem': ['HTTPBin Laboratorio'],
        'Status_Conexao': ['Sucesso (200)'],
        'Texto_Internet': [resumo_texto]
    }
    
    df_web = pd.DataFrame(dados_coletados)
    df_web.to_excel("dados_capturados_internet.xlsx", index=False)
    
    print("\n📊 Sucesso absoluto! A planilha 'dados_capturados_internet.xlsx' foi gerada na sua pasta!")

else:
    print(f"\n❌ Falha critica de conexao. Código do servidor: {resposta.status_code}")
