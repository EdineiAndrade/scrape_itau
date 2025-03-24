from playwright.sync_api import sync_playwright
from convert_data import convert_data
import time
import os

# Função principal para realizar o scraping
def scrape_itau(base_url):

    with sync_playwright() as p:
        print("Abrindo página web...")
        browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
        page = browser.new_page()

        page.goto(base_url)
        
        # Definição do caminho do arquivo
        caminho_arquivo = r"C:\scrape_itau\login\login.txt"

        # Leitura do arquivo
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            linha = arquivo.readline().strip()  # Lê a primeira linha e remove espaços extras
            login, senha = linha.split(",")  # Divide os valores separados por vírgula
        # Extrair links das categorias
        print("Logando...")
        page.locator('//*[@id="cpf"]').fill(login)
        time.sleep(1)
         # Espera o botão de login estar visível e clica (timeout de 2s)
        submit_button1 = page.locator('//*[@class="it-auth-id__submit"]')
        submit_button1.wait_for(timeout=2000)
        time.sleep(2)
        submit_button1.press("Enter")
        label_senha = page.locator('#password')
        label_senha.wait_for(timeout=2000)
        page.locator('#password').fill(senha)
        submit_button2 = page.locator('//*[@id="submitBtn"]')
        
        submit_button2.wait_for(timeout=2000)
        time.sleep(2)
        submit_button2.press("Enter")
        #página Inicial
        time.sleep(15)
        page.goto('https://canal360i.cloud.itau.com.br/painel/wrapper/999/microcredito')
        time.sleep(5)
      
        
        # Pressione a tecla Tab 17 vezes
        for _ in range(17):
            page.keyboard.press("Tab")
            time.sleep(.3)
        page.keyboard.press("Enter")

        for i in range(1,56):
            # tabela = page.wait_for_selector('table.ids-table.cdk-table')
            # div_tabela = page.locator('//*[@class="ids-card ids-p-6 ids-card__container"]')
            # dados = extrair_tabela_do_div(tabela)
            time.sleep(5)
            nome_arquivo_pdf = os.path.join("C:\\scrape_itau","paginas_pdf", f"pagina_{i}.pdf")
            page.pdf(
            path=nome_arquivo_pdf,
            width="1100px",  # Largura fixa (pode ser ajustada)
            height=f"{3000}px",  # Define a altura da página
            print_background=True
            )
            time.sleep(.2)
            if i == 1:
                n = 8
            elif i >5:
                n = 5
            elif i >= 52:
                n = (i-46)
            else:                
                n = i + 2
            for _ in range(n):
                page.keyboard.press("Tab")
                time.sleep(.2)
            page.keyboard.press("Enter")
            print(f"Baixada página | {i}")
        browser.close()           
       
        return "Fim do Web scraping" 
# Executar o scraping e salvar os dados
if __name__ == "__main__":
    base_url = 'https://id.itau.com.br/authorize?client_id=corban-client-id&response_type=code&scope=openid&redirect_uri=https:%2F%2Fcanal360i.cloud.itau.com.br%2Flogin%2Fcallback-ciam'  
    data = scrape_itau(base_url)
    # Executar a função
    convert_data()